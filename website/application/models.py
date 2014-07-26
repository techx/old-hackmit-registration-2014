from contextlib import contextmanager
from flask.ext.sqlalchemy import SQLAlchemy

from .errors import ServerError

db = SQLAlchemy()

@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = db.session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

@contextmanager
def db_safety():
    try:
        with session_scope() as session:
            yield session
    except Exception as e:
        raise ServerError()

