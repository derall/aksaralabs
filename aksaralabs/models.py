from sqlalchemy import (
    Column, Integer, String, DateTime, Text, Boolean, ForeignKey, PickleType,
    Index, Float, LargeBinary)
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from aksaralabs.utils.log.logging_mixin import LoggingMixin

class Connection(Base, LoggingMixin):
    """
    Placeholder to store information about different database instances
    connection information. The idea here is that scripts use references to
    database instances (conn_id) instead of hard coding hostname, logins and
    passwords when using operators or hooks.
    """
    __tablename__ = "connection"

    id = Column(Integer(), primary_key=True)
    conn_id = Column(String(ID_LEN))
    conn_type = Column(String(500))
    host = Column(String(500))
    schema = Column(String(500))
    login = Column(String(500))
    _password = Column('password', String(5000))
    port = Column(Integer())
    is_encrypted = Column(Boolean, unique=False, default=False)
    is_extra_encrypted = Column(Boolean, unique=False, default=False)
    _extra = Column('extra', String(5000))

    _types = [
        ('jdbc', 'Jdbc Connection',),
        ('mysql', 'MySQL',),
        ('postgres', 'Postgres',),
        ('oracle', 'Oracle',),
        ('sqlite', 'Sqlite',),
        ('mssql', 'Microsoft SQL Server'),
    ]

    def __init__(
            self, conn_id=None, conn_type=None,
            host=None, login=None, password=None,
            schema=None, port=None, extra=None,
            uri=None):
        self.conn_id = conn_id
        if uri:
            self.parse_from_uri(uri)
        else:
            self.conn_type = conn_type
            self.host = host
            self.login = login
            self.password = password
            self.schema = schema
            self.port = port
            self.extra = extra