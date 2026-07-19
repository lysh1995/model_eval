"""Storage as a service. MySQL is the designed DB; SQLite is the zero-dependency runnable
backend. Same schema, two drivers -- see db.ddl() and schema.sql."""
from .db import Store, ddl, TABLES
