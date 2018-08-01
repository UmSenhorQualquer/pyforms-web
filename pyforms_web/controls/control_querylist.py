from pyforms_web.controls.control_base import ControlBase
from django.apps import apps

from django.core.exceptions import FieldDoesNotExist

from django.utils.dateparse import parse_datetime
from django.db.models import Q
import simplejson, datetime
from django.utils import timezone
from django.conf import settings
from django.db import models
from datetime import timedelta
from calendar import monthrange
from django.utils import timezone
import locale

from pyforms_web.utils import get_lookup_verbose_name, get_lookup_value, get_lookup_field
from django.db.models.fields.files import FieldFile

class ControlQueryList(ControlBase):

    def __init__(self, *args, **kwargs):
        self.rows_per_page      = kwargs.get('rows_per_page', 10)
        self.n_pages            = kwargs.get('n_pages', 5)
        self._current_page      = 1

        self.list_display       = kwargs.get('list_display', [])
        self.list_filter        = kwargs.get('list_filter', [])
        self.search_fields      = kwargs.get('search_fields', [])

        self.search_field_key   = None
        self.filter_by          = []
        self.sort_by            = []
        self._selected_row_id   = -1 #row selected by the mouse

        # these informations is needed to serialize the control to the drive
        self._app   = None
        self._model = None
        self._query = None
        self._update_list = True #used to update the list to the client
        ####################################################################

        super(ControlQueryList, self).__init__(*args, **kwargs)


    def init_form(self): return "new ControlQueryList('{0}', {1})".format( self._name, simplejson.dumps(self.serialize(init_form=True)) )

    def item_selection_changed_client_event(self):
        self.mark_to_update_client()
        self.item_selection_changed_event()

    def item_selection_changed_event(self): pass

    def __get_pages_2_show(self, queryset):
        if not queryset: return []

        total_rows      = queryset.count()
        total_n_pages   = (total_rows / self.rows_per_page) + (0 if (total_rows % self.rows_per_page)==0 else 1)
        start_page      = self._current_page - self.n_pages/2
        end_page        = self._current_page + self.n_pages/2

        if start_page<1:
            diff        = 1 - start_page
            start_page  = 1
            end_page    += diff
        if end_page>total_n_pages:
            end_page = total_n_pages
            if ( end_page-(self.n_pages) )>=1: start_page = (end_page-(self.n_pages-1))

        return [int(start_page-1) if int(start_page)>1 else -1] + list(range(int(start_page), int(end_page)+1)) + [ int(end_page+1) if int(end_page)<int(total_n_pages) else -1]



    

    @property
    def selected_row_id(self): return self._selected_row_id
    @selected_row_id.setter
    def selected_row_id(self, value): 
        self._selected_row_id = value
    
    @property
    def value(self):
        if self._app and self._model and self._query:
            # reconstruct the query ################################
            model       = apps.get_model(self._app, self._model)
            qs          = model.objects.all()
            qs.query    = self._query
            for f in self.filter_by: qs = qs.filter(**f)

            if self.search_field_key and len(self.search_field_key)>0:
                search_filter = None
                for s in self.search_fields:
                    q = Q(**{s: self.search_field_key})
                    search_filter = (search_filter | q) if search_filter else q
                qs = qs.filter(search_filter)

            return qs.distinct()
        else:
            return None

    @value.setter
    def value(self, value):
        
        if self._query!=value.query: 
            if value is not None:
                if len(value.query.order_by)==0 and value.model._meta.ordering:
                    value = value.order_by(*value.model._meta.ordering)

                self._model = value.model._meta.label.split('.')[-1]
                self._query = value.query
                self._app   = value.model._meta.app_label
                self._selected_row_id = -1
                self._current_page = 1

            self.mark_to_update_client()
            self.changed_event()

        

    def serialize(self, init_form=False):
        data            = ControlBase.serialize(self)
        queryset        = self.value
    
        rows            = []
        
        if self._update_list and queryset:
            row_start = self.rows_per_page*(self._current_page-1)
            row_end   = self.rows_per_page*(self._current_page)
            model     = queryset.model

            if len(self.sort_by)>0:
                for sort in self.sort_by:
                    direction = '-' if sort['desc'] else ''
                    queryset = queryset.order_by( direction+sort['column'] )
    
            # if no order by exists add one, to avoid the values to be show randomly in the list
            order_by = list(queryset.query.order_by)
            if 'pk' not in order_by or '-pk' not in order_by:
                order_by.append('-pk')
                queryset = queryset.order_by( *order_by )
            
            rows = self.queryset_to_list(queryset, self.list_display, row_start, row_end)

            if init_form:
                filters_list = self.serialize_filters(self.list_filter, queryset)
                data.update({ 'filters_list': filters_list });
                
        if init_form and self.list_display:
            #configure the headers titles
            headers         = []
            for column_name in self.list_display:
                label = get_lookup_verbose_name(queryset.model, column_name)
                
                headers.append({
                    'label':  label,
                    'column': column_name
                })
            data.update({ 'horizontal_headers':   headers, });
                
        
        if len(self.search_fields)>0:
            data.update({'search_field_key': self.search_field_key if self.search_field_key is not None else ''})
    
        total_rows = queryset.count()
        total_n_pages   = (total_rows / self.rows_per_page) + (0 if (total_rows % self.rows_per_page)==0 else 1)

        data.update({
            'filter_by':       self.filter_by,
            'sort_by':         self.sort_by,
            'pages':           {'current_page': self._current_page, 'pages_list':self.__get_pages_2_show(queryset) },
            'pages_total':     total_n_pages,
            'value':           '',
            'values':          rows,
            'values_total':    total_rows,
            'selected_row_id': self._selected_row_id
        })

        return data

        
    def page_changed_event(self): 
        self._selected_row_id = -1
        self.mark_to_update_client()

    def sort_changed_event(self): 
        self._selected_row_id = -1
        self.mark_to_update_client()

    def filter_changed_event(self):
        self._selected_row_id = -1
        self._current_page    = 1
        self.mark_to_update_client()

    #####################################################################
    #####################################################################

    def format_list_column(self, col_value): 

        if col_value is None: return ''       

        if isinstance(col_value, datetime.datetime ):
            if not col_value: return ''
            col_value = timezone.localtime(col_value)
            return col_value.strftime('%Y-%m-%d %H:%M')
        elif isinstance(col_value, datetime.date ):
            if not col_value: return ''
            return col_value.strftime('%Y-%m-%d')
        elif isinstance(col_value, bool ):
            return '<i class="check circle green icon"></i>' if col_value else '<i class="minus circle red icon"></i>'
        elif isinstance(col_value, int ):
            return locale.format("%d", col_value, grouping=True)
        elif isinstance(col_value, float ):
            return locale.format("%f", col_value, grouping=True)
        elif isinstance(col_value, int ):
            return locale.format("%d", col_value, grouping=True)
        elif isinstance(col_value, FieldFile ):
            return '<a href="{0}" target="_blank" click="return false;" >{1}</a>'.format(col_value.url, col_value.name)
        elif isinstance(col_value, models.Model ):
            return col_value.__str__()
        elif callable(col_value):
            v = col_value()

            if hasattr(col_value, 'boolean') and getattr(col_value, 'boolean'):
                v = '<i class="check circle green icon"></i>' if v else '<i class="minus circle red icon"></i>'

            return '' if v is None else str(v)
        else:
            return col_value

    def format_filter_column(self, col_value):
        

        if isinstance(col_value, datetime.datetime ):
            if not col_value: return ''
            col_value = timezone.localtime(col_value)
            return col_value.strftime('%Y-%m-%d %H:%M')
        elif isinstance(col_value, datetime.date ):
            if not col_value: return ''
            return col_value.strftime('%Y-%m-%d')
        elif isinstance(col_value, bool ):
            return '<i class="check circle green icon"></i>' if col_value else '<i class="minus circle red icon"></i>'
        elif isinstance(col_value, models.Model ):
            return col_value.__str__()
        elif callable(col_value):
            return str(col_value())
        else:
            return col_value

    
    
    def queryset_to_list(self, queryset, list_display, first_row, last_row):
        if not list_display:
            return [ [m.pk, str(m)] for m in queryset[first_row:last_row] ]
        else:
            queryset = queryset.distinct()
            queryset = queryset.order_by(*queryset.query.order_by)

            rows = []
            for o in queryset[first_row:last_row]:
                row = [o.pk] + [self.format_list_column(get_lookup_value(o, col)) for col in list_display] 
                rows.append(row)
            
            return rows


    def get_datetimefield_options(self, column_name):
        column_filter = "{0}__gte".format(column_name)

        now             = timezone.now()
        today_begin     = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end       = now.replace(hour=23, minute=59, second=59, microsecond=999)
        next_4_months   = today_end + timedelta(days=4*30)

        month_begin     = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        month_end       = now.replace(day=monthrange(now.year, now.month)[1], hour=23, minute=59, second=59, microsecond=999)
        
        return {
            'items': [
                ("{0}__gte={1}&{0}__lte={2}".format(column_name, today_begin.isoformat(), today_end.isoformat()),      'Today'),
                ("{0}__gte={1}&{0}__lte={2}".format(column_name, month_begin.isoformat(), month_end.isoformat()),      'This month'),
                ("{0}__gte={1}&{0}__lte={2}".format(column_name, today_begin.isoformat(), next_4_months.isoformat()),  'Next 4 months'), 
                ("{0}__year={1}".format(column_name, now.year), 'This year')
            ]
        }


    def deserialize(self, properties):
        self._label   = properties.get('label','')
        self._help    = properties.get('help','')
        self._visible = properties.get('visible',True)
        
        self.search_field_key   = properties.get('search_field_key', None)
        self.sort_by            = properties.get('sort_by', [])
        self.filter_by          = properties.get('filter_by',[])
        self._current_page      = int(properties['pages']['current_page'])
        self._selected_row_id   = properties.get('selected_row_id', -1)

    def serialize_filters(self, list_filter, queryset):
        filters_list = []
        model = queryset.model

        #configure the filters
        for column_name in list_filter:
            field = get_lookup_field(model, column_name)
            
            if field is None: continue

        
            field_type       = 'combo'
            field_properties = {
                'field_type': 'combo',
                'label':    get_lookup_verbose_name(model, column_name),
                'column':   column_name
            }

            if isinstance(field, models.BooleanField):
                field_properties.update({
                    'items': [ ("{0}=true".format(column_name), 'True'), ("{0}=false".format(column_name), 'False')]
                })
            
            if isinstance(field, models.Field) and field.choices:
                field_properties.update({
                    'items': [ ("{0}={1}".format(column_name, c[0]),c[1]) for c in field.choices]
                })
            
            elif isinstance(field, (models.DateField, models.DateTimeField) ):
                field_properties.update(self.get_datetimefield_options(column_name))
            
            elif field.is_relation:
                objects = field.related_model.objects.all()

                limit_choices = field.get_limit_choices_to()
                if limit_choices: 
                    objects = objects.filter(**limit_choices)

                filter_values = [(column_name+'='+str(o.pk), o.__str__() ) for o in objects]
                field_properties.update({'items': filter_values})
                
            else:
                column_values = queryset.values_list(column_name, flat=True).distinct().order_by(column_name)
                filter_values = [(column_name+'='+str(column_value), column_value) for column_value in column_values]
                field_properties.update({'items': filter_values})

            filters_list.append(field_properties)

        return filters_list