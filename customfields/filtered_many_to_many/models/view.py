from copy import copy
from typing import Any, Dict, Tuple, Type

from django.db import models


def clone_field_without_related_name(
    field: models.Field,
) -> models.Field:
    """Creates a clone of the given field, without a related_name."""

    if isinstance(field, models.fields.related.RelatedField):

        # ugly hack to prevent "models not ready" error
        if field.swappable:
            field = copy(field)
            field.swappable = False

        _name, _path, args, kwargs = field.deconstruct()
        kwargs.pop('related_name', None)

        return type(field)(*args, **kwargs)

    else:
        return field.clone()


class QuerySetViewModelMeta(models.base.ModelBase):
    def __new__(
        cls,
        name: str,
        bases: Tuple[Type],
        attrs: Dict[str, Any]
    ) -> "QuerySetViewModelMeta":
        super_new = super().__new__

        attr_meta = attrs.get('Meta', None)

        # Ensure initialization is only performed if Meta has a queryset
        if not hasattr(attr_meta, "queryset"):
            return super_new(cls, name, bases, attrs)

        queryset = attr_meta.queryset
        del attr_meta.queryset

        attr_meta.managed = False

        # clone original model's attributes
        for field in queryset.model._meta.fields:
            if field.name not in attrs:
                attrs[field.name] = clone_field_without_related_name(field)

        result = super_new(cls, name, bases, attrs)

        result_meta = result._meta
        result_meta.queryset = queryset

        return result


class QuerySetViewModel(models.Model, metaclass=QuerySetViewModelMeta):
    class Meta:
        abstract = True

