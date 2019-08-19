from migrate_sql.config import SQLItem

from filtered_many_to_many.models.view import (
    PersonPetsNonDeletedView,
    QuerySetViewModel,
)


def create_queryset_view_sql_item(model: QuerySetViewModel) -> SQLItem:
    """Creates the SQL for the view based on the given QuerySetViewModel"""

    view_name = model._meta.db_table

    query_sql, query_params = model._meta.queryset.query.sql_with_params()

    return SQLItem(
        name=f'make_{view_name}',
        sql=[
            (
                f'CREATE VIEW {view_name} AS {query_sql};',
                query_params,
            ),
        ],
        reverse_sql=[
            (
                f'DROP VIEW IF EXISTS {view_name};',
                None,
            ),
        ],
    )


sql_items = [
    create_queryset_view_sql_item(PersonPetsNonDeletedView),
]
