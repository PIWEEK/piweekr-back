from sqlalchemy import create_engine, MetaData, Table, event, DDL
from sqlalchemy import Column, Integer, String, Date, DateTime, Float, ForeignKey, Boolean, Text
from sqlalchemy.sql import select, insert, update, delete, func
from sqlalchemy_utils.types.arrow import ArrowType
from contextlib import contextmanager

from .relationships import Context
from .converter import to_plain, from_plain


class SQLContext(Context):

    def __init__(self, repository):
        super().__init__()
        self.conn = repository._engine.connect()
        self.trans = self.conn.begin()

    def commit(self):
        self.trans.commit()
        self.conn.close()

    def rollback(self):
        self.trans.rollback()
        self.conn.close()


class SQLADTRepository:

    def __init__(self, options):
        db_url = _build_db_url(options)
        echo = options.get("ECHO", False)
        isolation_level = options.get("ISOLATION_LEVEL", "READ COMMITTED")

        self._metadata = MetaData()
        self._engine = create_engine(db_url, echo=echo, isolation_level=isolation_level)

    @contextmanager
    def context(self):
        context = SQLContext(self)
        try:
            yield context
        except Exception:
            context.rollback()
            raise
        else:
            context.commit()

    def add_adt_table(self, the_class, name, manual_columns = {}):
        columns = [
            manual_columns[name] if name in manual_columns else _field_to_column(name, f)
            for name, f in the_class._fields.items()
        ]
        table = Table(name, self._metadata, *columns)
        setattr(self, name, table)

    def add_table(self, name, columns):
        table = Table(name, self._metadata, *columns)
        setattr(self, name, table)

    def add_ddl(self, code):
        # Set an event to execute the ddl code after engine initialization.
        # See http://docs.sqlalchemy.org/en/latest/core/ddl.html
        event.listen(
            self._metadata,
            "after_create",
            DDL(code),
        )

    def create_all_tables(self):
        self._metadata.create_all(self._engine)

    def truncate_all_tables(self):
        return self.conn.truncate_all_tables()

    def truncate_all_tables(self):
        with self.context() as context:
            for attr in self.__dict__.values():
                if isinstance(attr, Table):
                    self.truncate_table(context, attr)

    def truncate_table(self, context, table):
        context.conn.execute("TRUNCATE TABLE {} CASCADE".format(table.name))

    def insert_adt(self, context, table, instance):
        values = to_plain(instance)
        del values["id"]
        result = context.conn.execute(
            insert(table).values(values)
        )
        inserted_id = result.inserted_primary_key[0]
        instance.attach(inserted_id)
        return instance

    def update_adt(self, context, table, instance):
        values = to_plain(instance)
        result = context.conn.execute(
            update(table).values(values).where(table.c.id == instance.id)
        )
        return result.rowcount

    def delete_adt(self, context, table, instance):
        result = context.conn.execute(
            delete(table).where(table.c.id == instance.id)
        )
        return result.rowcount

    def retrieve_single_adt(self, context, the_class, select):
        rows = context.conn.execute(select)
        row = rows.first()
        return the_class(**row) if row else None

    def retrieve_adts(self, context, the_class, select):
        rows = context.conn.execute(select)
        return [the_class(**row) for row in rows]

    def retrieve_joined_adts(self, context, main_class, classes, select):
        rows = context.conn.execute(select)

        adts = []
        for row in rows:
            for name, the_class in classes.items():
                data = {}
                for key, value in row.items():
                    if key.startswith(name):
                        data[key[len(name)+1:]] = value
                instance = the_class(**data)
                context.add(instance)
                if the_class == main_class:
                    if not instance.id in [adt.id for adt in adts]:
                        adts.append(instance)

        return adts

    def retrieve_single_joined_adt(self, context, main_class, classes, select):
        adts = self.retrieve_joined_adts(context, main_class, classes, select)
        return adts[0] if len(adts) > 0 else None


def _build_db_url(options):
    protocol = options.get("DB_PROTOCOL", "postgresql+psycopg2")
    user = options.get("DB_USER", None)
    password = options.get("DB_PASSWORD", None)
    host = options.get("DB_HOST", "localhost")
    db_name = options.get("DB_NAME", None)

    db_url = "{}://".format(protocol)
    if user is not None:
        db_url += user
    if password is not None:
        db_url += ":{}".format(password)
    db_url += "@{}".format(host)
    db_url += "/{}".format(db_name)

    return db_url


def _field_to_column(name, field):
    import datetime
    from arrow import arrow
    if field.type == str:
        column_type = String
    elif field.type == int:
        column_type = Integer
    elif field.type == float:
        column_type = Float
    elif field.type == datetime.date:
        column_type = Date
    elif field.type == datetime.datetime:
        column_type = DateTime
    elif field.type == arrow.Arrow:
        column_type = ArrowType
    elif field.type == bool:
        column_type = Boolean
    else:
        raise ValueError("Cannot generate column for field type {}".format(field.type))
    is_pk = (name == "id")
    return Column(name, column_type, primary_key = is_pk)

