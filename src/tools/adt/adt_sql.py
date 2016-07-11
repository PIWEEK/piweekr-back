from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, Boolean, Text
from contextlib import contextmanager

from tools.sql.sql_connection import SQLConnection
from sqlalchemy.sql import select, insert, update, delete, func

from .relationships import Context
from .converter import to_plain, from_plain


class SQLContext(Context):
    def __init__(self, session):
        super().__init__()
        self.session = session


class SQLADTRepository:

    def __init__(self, options):
        self.conn = SQLConnection(options)

    @contextmanager
    def context(self):
        try:
            with self.conn.session() as session:
                context = SQLContext(session)
                yield context
        except Exception:
            raise
        else:
            pass

    def add_adt_table(self, the_class, name, columns = None):
        if not columns:
            columns = [self._field_to_column(name, f) for name, f in the_class._fields.items()]
        self.conn.add_table(name, name, columns)
        setattr(self, name, getattr(self.conn, name))

    def _field_to_column(self, name, field):
        import datetime
        if field.type == str:
            column_type = String
        elif field.type == int:
            column_type = Integer
        elif field.type == float:
            column_type = Float
        elif field.type == datetime.date:
            column_type = Date
        elif field.type == bool:
            column_type = Boolean
        else:
            raise ValueError("Cannot generate column for field type {}".format(field.type))
        is_pk = (name == "id")
        return Column(name, column_type, primary_key = is_pk)

    def create_all_tables(self):
        return self.conn.create_all_tables()

    def insert_adt(self, context, table, instance):
        values = to_plain(instance)
        del values["id"]
        inserted_id = self.conn.insert_into_table(
            context.session,
            insert(table).values(values)
        )
        instance.attach(inserted_id)
        return instance

    def retrieve_single_adt(self, context, the_class, select):
        data = self.conn.select_single_row(
            context.session,
            dict,
            select,
        )
        return from_plain(the_class, data)

    def retrieve_adts(self, context, the_class, select):
        rows = self.conn.select_rows(
            context.session,
            dict,
            select
        )
        return [the_class(**row) for row in rows]

    def retrieve_joined_adts(self, context, classes, select):
        rows = self.conn.select_rows(
            context.session,
            dict,
            select
        )

        adts = []
        for row in rows:
            for i, (name, the_class) in enumerate(classes.items()):
                data = {}
                for key, value in row.items():
                    if key.startswith(name):
                        data[key[len(name)+1:]] = value
                instance = the_class(**data)
                context.add(instance)
                if i == 0:
                    if not instance.id in [adt.id for adt in adts]:
                        adts.append(instance)

        return adts
