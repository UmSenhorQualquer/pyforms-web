from django.db.models.constants import LOOKUP_SEP
from django.utils.encoding import force_text

def make_lambda_func(func, **kwargs):
    """ Auxiliar function for passing parameters to functions """
    return lambda: func(**kwargs)


def get_lookup_field(model, lookup):
    # will return first non relational field's verbose_name in lookup
    parts = lookup.split(LOOKUP_SEP)
    for i, part in enumerate(parts):
        try:
            f = model._meta.get_field(part)
        except FieldDoesNotExist:
            f = None
            # check if field is related
            """for f in model._meta.related_objects:
                if f.get_accessor_name() == part:
                    break
            else:
                raise ValueError("Invalid lookup string")

        if f.is_relation:
            model = f.related_model
            if (len(parts)-1)==i:
                return model
            else:
                continue
            """

        return f


def get_lookup_value(o, lookup):
    """
    Return the value of a lookup over an object
    """
    if o is None: return None
    val = o
    for fieldname in lookup.split(LOOKUP_SEP):
        if val is None: break
        val = getattr(val, fieldname)
    return val

        

def get_lookup_verbose_name(model, lookup):
    # will return first non relational field's verbose_name in lookup
    parts = lookup.split(LOOKUP_SEP)
    field = None
    for i, part in enumerate(parts):
        try:
            field = model._meta.get_field(part)
        except FieldDoesNotExist:

            f = getattr(model, part)
            if callable(f):
                if hasattr(f, 'short_description'):
                    return f.short_description.title()
                else:
                    return part.title()
            else:
                # check if field is related
                for f in model._meta.related_objects:
                    if f.get_accessor_name() == part:
                        field = f
                        break

        if not hasattr(field, 'verbose_name'):
            if field.is_relation:
                if (len(parts)-1)==i:
                    return force_text(field.related_model._meta.verbose_name)
                else:
                    continue
        
        return force_text(field.verbose_name).title()