from typing import Any, Dict, List, Tuple, Type

from django.db import models


class FilteredManyToManyField(models.ManyToManyField):
    """
    Provide a many-to-many relation by using an intermediary model that
    holds two ForeignKey fields pointed at the two sides of the relation.

    FilteredManyToManyField will only be related to those models for which
    the intermediary model matches the given ``filter`` Q.

    Unless a ``through`` model was provided, FilteredManyToManyField will use
    the create_many_to_many_intermediary_model factory to automatically
    generate the intermediary model.
    """

    def __init__(
        self,
        to: Type[models.Model],
        filter: Dict[str, Any],  # TODO: also support Q, once django>=2.0
        **kwargs,
    ) -> None:
        self.filter = filter

        super().__init__(to, **kwargs)

    def deconstruct(self) -> Tuple[
        str,
        str,
        List[Any],
        Dict[str, Any],
    ]:
        """
        Returns enough information to recreate the field as a 4-tuple:

         * The name of the field on the model,
           if contribute_to_class has been run
         * The import path of the field, including the class:
           django.db.models.IntegerField
           This should be the most portable version,
           so less specific may be better.
         * A list of positional arguments
         * A dict of keyword arguments

        Note that the positional or keyword arguments must contain values of
        the following types (including inner values of collection types):

         * None, bool, str, unicode, int, long, float, complex
         * set, frozenset, list, tuple, dict
         * UUID
         * datetime.datetime (naive), datetime.date
         * top-level classes, top-level functions
           (will be referenced by their full import path)
         * Storage instances - these have their own deconstruct() method

        This is because the values here must be serialized into a text format
        (possibly new Python code, possibly JSON) and these are the only types
        with encoding handlers defined.

        There's no need to return the exact way the field was instantiated
        this time, just ensure that the resulting field is the same - prefer
        keyword arguments over positional ones, and omit parameters with their
        default values.
        """

        name, path, args, kwargs = super().deconstruct()

        kwargs['filter'] = self.filter

        return name, path, args, kwargs
