from sqlalchemy import create_engine, MetaData, Table, event, DDL
from contextlib import contextmanager


class SQLConnection:

    def __init__(self, options):
        protocol = options.get("DB_PROTOCOL", "postgresql+psycopg2")
        user = options.get("DB_USER", None)
        password = options.get("DB_PASSWORD", None)
        host = options.get("DB_HOST", "localhost")
        db_name = options.get("DB_NAME", None)
        echo = options.get("ECHO", False)
        isolation_level = options.get("ISOLATION_LEVEL", "READ COMMITTED")

        db_url = "{}://".format(protocol)
        if user is not None:
            db_url += user
        if password is not None:
            db_url += ":{}".format(password)
        db_url += "@{}".format(host)
        db_url += "/{}".format(db_name)

        self._metadata = MetaData()
        self._engine = create_engine(db_url, echo=echo, isolation_level=isolation_level)

    @contextmanager
    def session(self):
        session = SQLSession(self)
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        else:
            session.commit()

    def add_table(self, name, db_name, columns):
        table = Table(db_name, self._metadata, *columns)
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
        with self.session() as session:
            for attr in self.__dict__.values():
                if isinstance(attr, Table):
                    self.truncate_table(session, attr)

    def truncate_table(self, session, table):
        session.conn.execute("TRUNCATE TABLE {} CASCADE".format(table.name))

    def insert_into_table(self, session, insert):
        result = session.conn.execute(insert)
        return result.inserted_primary_key[0]
        # inserted_row = result.last_inserted_params()
        # inserted_row["id"] = result.inserted_primary_key[0]
        # return inserted_row

    def select_single_row(self, session, result_class, select):
        result = session.conn.execute(select)
        result_data = result.first()
        if result_data:
            return result_class(result_data)
        else:
            return None

    def select_rows(self, session, result_class, select):
        result = session.conn.execute(select)
        return [result_class(row) for row in result]

    def update_table(self, session, update):
        result = session.conn.execute(update)
        return result.rowcount

    def delete_from_table(self, session, delete):
        result = session.conn.execute(delete)
        return result.rowcount


class SQLSession:

    def __init__(self, connection):
        self.conn = connection._engine.connect()
        self.trans = self.conn.begin()

    def commit(self):
        self.trans.commit()
        self.conn.close()

    def rollback(self):
        self.trans.rollback()
        self.conn.close()

