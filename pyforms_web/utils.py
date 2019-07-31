from django.db.models.constants import LOOKUP_SEP
from django.db import models
from django.utils.encoding import force_text
from django.core.exceptions import FieldDoesNotExist


def make_lambda_func(func, **kwargs):
    """ Auxiliar function for passing parameters to functions """
    return lambda: func(**kwargs)


def get_lookup_field(model, lookup):

    # will return first non relational field's verbose_name in lookup
    parts = lookup.split(LOOKUP_SEP)
    for i, part in enumerate(parts):
        f = model._meta.get_field(part)
        if (len(parts) - 1) == i:
            return f
        elif hasattr(f, 'is_relation') and f.is_relation:
            model = f.related_model
    return f


def get_lookup_value(obj, lookup):
    """
    Return the value of a lookup over an object
    """
    value = None
    if obj is not None:
        for fieldname in lookup.split(LOOKUP_SEP):
            if obj is None:
                return None
            try:
                # works for fields with choices defines
                obj = getattr(obj, 'get_%s_display' % fieldname)
            except AttributeError:
                obj = getattr(obj, fieldname, None)
        else:
            value = obj
    return value


def get_lookup_verbose_name(model, lookup):
    # will return first non relational field's verbose_name in lookup

    parts = lookup.split(LOOKUP_SEP)
    field = None
    for i, part in enumerate(parts):
        last_loop = i == (len(parts) - 1)
        try:
            field = model._meta.get_field(part)

            if field.is_relation:

                if last_loop:
                    if not hasattr(field, 'verbose_name'):
                        return force_text(field.related_model._meta.verbose_name)
                    elif field._verbose_name is None:
                        return force_text(field.verbose_name).capitalize()
                    else:
                        return force_text(field.verbose_name)

                else:
                    model = field.related_model
                    continue

        except FieldDoesNotExist:

            field = getattr(model, part)

            # check if is a function
            if callable(field) and not isinstance(field, models.Model):

                if hasattr(field, 'short_description'):
                    return field.short_description
                else:
                    return part.title()

            else:
                return part.title()

        if field._verbose_name is None:
            return force_text(field.verbose_name).capitalize()
        else:
            return force_text(field.verbose_name)
