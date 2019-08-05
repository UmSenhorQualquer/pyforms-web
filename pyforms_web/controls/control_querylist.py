import locale, csv, itertools, simplejson, datetime

from decimal import Decimal
from django.db import models
from django.apps import apps
from django.db.models import Q
from django.utils import timezone
from django.utils.html import strip_tags
from django.http import HttpResponse
from django.db.models.fields.files import FieldFile
from pyforms_web.web.middleware import PyFormsMiddleware
from pyforms_web.controls.control_base import ControlBase
from pyforms_web.utils import get_lookup_verbose_name, get_lookup_value, get_lookup_field


class ControlQueryList(ControlBase):

    def __init__(self, *args, **kwargs):
        self.rows_per_page      = kwargs.get('rows_per_page', 10)
        self.n_pages            = kwargs.get('n_pages', 5)
        self._current_page      = 1

        self.headers            = kwargs.get('headers', None)
        self.list_display       = kwargs.get('list_display', [])
        self.list_filter        = kwargs.get('list_filter', [])
        self.search_fields      = kwargs.get('search_fields', [])
        self.export_csv         = kwargs.get('export_csv', False)
        self.export_csv_columns = kwargs.get('export_csv_columns', self.list_display)
        self.export_csv_headers = kwargs.get('export_csv_headers', {})
        self._columns_size      = kwargs.get('columns_size', None)
        self._columns_align     = kwargs.get('columns_align', None)
        self.item_selection_changed_event = kwargs.get('item_selection_changed_event', self.item_selection_changed_event)

        self.filter_event = kwargs.get('filter_event', self.filter_event)
        self.page_event = kwargs.get('page_event', self.page_event)
        self.sort_event = kwargs.get('sort_event', self.sort_event)

        self.search_field_key   = None
        self.filter_by          = []
        self.sort_by            = []
        self._selected_row_id   = -1 #row selected by the mouse

        self.custom_filter_labels = {}

        # these informations is needed to serialize the control to the drive
        self._app   = None
        self._model = None
        self._query = None
        self._update_list = True #used to update the list to the client
        ####################################################################

        super(ControlQueryList, self).__init__(*args, **kwargs)


    def init_form(self): return "new ControlQueryList('{0}', {1})".format( self._name, simplejson.dumps(self.serialize(init_form=True)) )

    def item_selection_changed_client_event(self):
        self.mark_to_update_client()  # what are the implications of enabling this???
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


    def export_csv_event(self):
        """
        Event called to export the queryset to excel
        """
        self.parent.execute_js( """window.open('/pyforms/export-csv/{0}/{1}/');""".format(self.parent.uid, self.name) )

    def export_csv_http_response(self):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="{0}.csv"'.format(timezone.now().isoformat())
        writer = csv.writer(response, delimiter=";")

        queryset = self.value

        headers = []
        for column_name in self.export_csv_columns:
            try:
                header = self.export_csv_headers[column_name]
            except KeyError:
                header = get_lookup_verbose_name(queryset.model, column_name)
            headers.append(header)
        writer.writerow(headers)

        for o in queryset:
            row = [
                strip_tags(self.format_list_column(get_lookup_value(o, col), raw=True))
                for col in self.export_csv_columns
            ] 
            writer.writerow(row)
            
        return response 

    @property
    def export_csv_columns(self):
        """
        Sets and gets the list of columns to be used in the cvs export
        By default it will assume the self.list_display value
        """
        return self._export_csv_columns
    @export_csv_columns.setter
    def export_csv_columns(self, value):
        self._export_csv_columns = value


    @property
    def export_csv(self):
        """
        Flag to activate or deactivate the csv export button
        """
        return self._export_csv
    @export_csv.setter
    def export_csv(self, value):
        self._export_csv = value
    

    @property
    def selected_row_id(self): return self._selected_row_id
    @selected_row_id.setter
    def selected_row_id(self, value): 
        self._selected_row_id = value

    @property
    def columns_size(self): return self._columns_size

    @columns_size.setter
    def columns_size(self, value):
        self.mark_to_update_client()
        self._columns_size = value

    @property
    def columns_align(self): return self._columns_align

    @columns_align.setter
    def columns_align(self, value):
        self.mark_to_update_client()
        self._columns_align = value
    
    @property
    def value(self):
        if self._app and self._model and self._query:
            # reconstruct the query ################################
            model       = apps.get_model(self._app, self._model)
            qs          = model.objects.all()
            qs.query    = self._query

            # apply filters
            for f in self.filter_by: 
                qs = qs.filter(**f)

            # apply search keys
            if self.search_field_key and len(self.search_field_key)>0:
                search_filter = None
                for s in self.search_fields:
                    keys_filter = None
                    for key in self.search_field_key.split():
                        q = Q(**{s: key})
                        keys_filter = (keys_filter & q) if keys_filter else q
                    search_filter = (search_filter | keys_filter) if search_filter else keys_filter
                qs = qs.filter(search_filter)

            # apply orders by
            if len(self.sort_by)>0:
                for sort in self.sort_by:
                    direction = '-' if sort['desc'] else ''
                    qs = qs.order_by( direction+sort['column'] )
            
            # if no order by exists add one, to avoid the values to be show randomly in the list
            order_by = list(qs.query.order_by)
            if 'pk' not in order_by or '-pk' not in order_by:
                order_by.append('-pk')
                qs = qs.order_by( *order_by )

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
        data     = ControlBase.serialize(self)
        queryset = self.value
    
        rows = []
        
        if self._update_list and queryset:
            row_start = self.rows_per_page*(self._current_page-1)
            row_end   = self.rows_per_page*(self._current_page)

            rows = self.queryset_to_list(queryset, self.list_display, row_start, row_end)

            if init_form:
                filters_list = self.serialize_filters(self.list_filter, queryset)
                data.update({ 'filters_list': filters_list });

        if init_form and self.list_display and (queryset or self.headers):
            #configure the headers titles
            headers = []


            if self.headers is None:
                for column_name in self.list_display:
                    label = get_lookup_verbose_name(queryset.model, column_name)
                    headers.append({
                        'label':  label,
                        'column': column_name
                    })
            else:
                for label, column_name in itertools.zip_longest(self.headers, self.list_display):
                    headers.append({
                        'label':  label,
                        'column': column_name
                    })
            data.update({ 'horizontal_headers':   headers, });
                
        
        if len(self.search_fields)>0:
            data.update({'search_field_key': self.search_field_key if self.search_field_key is not None else ''})
        

        total_rows = queryset.count() if queryset else 0
        total_n_pages   = (total_rows / self.rows_per_page) + (0 if (total_rows % self.rows_per_page)==0 else 1)

        data.update({
            'columns_align':   self.columns_align,
            'columns_size':    self.columns_size,
            'export_csv':      self.export_csv,
            'filter_by':       self.filter_by,
            'sort_by':         self.sort_by,
            'pages':           {'current_page': self._current_page, 'pages_list':self.__get_pages_2_show(queryset) },
            'pages_total':     total_n_pages,
            'value':           rows,
            'values_total':    total_rows,
            'selected_row_id': self._selected_row_id
        })

        return data

        
    def page_changed_event(self):
        self.page_event()
        self._selected_row_id = -1
        self.mark_to_update_client()

    def sort_changed_event(self):
        self.sort_event()
        self._selected_row_id = -1
        self.mark_to_update_client()

    def filter_changed_event(self):
        self.filter_event()
        self._selected_row_id = -1
        self._current_page    = 1
        self.mark_to_update_client()


    def filter_event(self):pass
    def page_event(self):pass
    def sort_event(self):pass

    #####################################################################
    #####################################################################

    def format_list_column(self, col_value, raw=False): 

        if col_value is None:
            return ''

        if type(col_value).__name__ == "ManyRelatedManager":
            # format a ManyToManyField for LIST_DISPLAY
            # TODO should we limit when there are a lot of objects?
            # or should the user remove that column from LIST_DISPLAY?
            objects = [str(obj) for obj in col_value.all()]
            if raw:
                return ", ".join(objects)
            else:
                return "<br>".join(objects)

        if callable(col_value):
            col_value = col_value()

        if isinstance(col_value, datetime.datetime):
            if not col_value: return ''
            col_value = timezone.localtime(col_value)
            return col_value.strftime('%Y-%m-%d %H:%M')
        elif isinstance(col_value, datetime.date):
            if not col_value: return ''
            return col_value.strftime('%Y-%m-%d')
        elif isinstance(col_value, bool):
            if raw:
                return str(col_value)
            else:
                return '<i class="check circle green icon"></i>' if col_value else '<i class="minus circle red icon"></i>'
        elif isinstance(col_value, int):
            return locale.format("%d", col_value, grouping=True)
        elif isinstance(col_value, float):
            return locale.format("%f", col_value, grouping=True)
        elif isinstance(col_value, Decimal):
            return '{0:n}'.format(col_value)
        elif type(col_value).__name__ == 'Money':
            # support django-money MoneyField
            if raw:
                return str(col_value)
            else:
                return '<div style="text-align: right; margin-right: .5rem;">%s</div>' % col_value
        elif isinstance(col_value, FieldFile):
            if raw:
                return str(col_value.name)
            try:
                return '<a href="{0}" target="_blank" click="return false;" >{1}</a>'.format(col_value.url, col_value.name)
            except ValueError:
                return ''
        elif isinstance(col_value, models.Model):
            return col_value.__str__()
        elif callable(col_value):
            v = col_value()

            if hasattr(col_value, 'boolean') and getattr(col_value, 'boolean'):
                if not raw:
                    v = '<i class="check circle green icon"></i>' if v else '<i class="minus circle red icon"></i>'

            return '' if v is None else str(v)
        else:
            return col_value

    def format_filter_column(self, col_value):
        

        if isinstance(col_value, datetime.datetime):
            if not col_value: return ''
            col_value = timezone.localtime(col_value)
            return col_value.strftime('%Y-%m-%d %H:%M')
        elif isinstance(col_value, datetime.date):
            if not col_value: return ''
            return col_value.strftime('%Y-%m-%d')
        elif isinstance(col_value, bool):
            return '<i class="check circle green icon"></i>' if col_value else '<i class="minus circle red icon"></i>'
        elif isinstance(col_value, models.Model):
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
            #queryset = queryset.order_by(*queryset.query.order_by)

            rows = []
            for o in queryset[first_row:last_row]:
                row = [o.pk] + [self.format_list_column(get_lookup_value(o, col)) for col in list_display] 
                rows.append(row)
            
            return rows

    """
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
                ("{0}__gte={1}&{0}__lte={2}".format(column_name, today_begin.strftime('%Y-%m-%d'), today_end.strftime('%Y-%m-%d')),      'Today'),
                ("{0}__gte={1}&{0}__lte={2}".format(column_name, month_begin.strftime('%Y-%m-%d'), month_end.strftime('%Y-%m-%d')),      'This month'),
                ("{0}__gte={1}&{0}__lte={2}".format(column_name, today_begin.strftime('%Y-%m-%d'), next_4_months.strftime('%Y-%m-%d')),  'Next 4 months'), 
                ("{0}__year={1}".format(column_name, now.year), 'This year')
            ]
        }
    """

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
            order_by    = column_name
            column_name = column_name[1:] if column_name.startswith('-') else column_name
            field = get_lookup_field(model, column_name)
            
            if field is None: continue

            field_properties = {
                'field_type': 'combo',
                'label': self.custom_filter_labels.get(
                    column_name,
                    get_lookup_verbose_name(model, column_name),
                ),
                'column':   column_name
            }

            if isinstance(field, models.BooleanField):
                field_properties.update({
                    'items': [ ("{0}=true".format(column_name), 'Yes'), ("{0}=false".format(column_name), 'No')]
                })

            elif isinstance(field, models.Field) and field.choices:
                field_properties.update({
                    'items': [ ("{0}={1}".format(column_name, c[0]),c[1]) for c in field.choices]
                })
            
            elif isinstance(field, (models.DateField, models.DateTimeField) ):
                #field_properties.update(self.get_datetimefield_options(column_name))
                
                field_properties.update({
                    'field_type': 'date-range'
                })

            elif field.is_relation:
                objects = field.related_model.objects.all()

                # Apply the field limits choice ##################################
                limit_choices = field.get_limit_choices_to()
                if limit_choices:
                    objects = objects.filter(**limit_choices).distinct()
                ##################################################################

                # Check if the parent window has a function to filter the related fields
                if hasattr(self.parent, 'get_related_field_queryset'):
                    objects = self.parent.get_related_field_queryset(
                        PyFormsMiddleware.get_request(), queryset, field, objects
                    )
                
                filter_values = [(column_name+'='+str(o.pk), o.__str__() ) for o in objects]
                field_properties.update({'items': filter_values})
                
            else:
                column_values = queryset.values_list(column_name, flat=True).distinct().order_by(order_by)
                filter_values = [(column_name+'='+str(column_value), column_value) for column_value in column_values]
                field_properties.update({'items': filter_values})

            filters_list.append(field_properties)

        return filters_list