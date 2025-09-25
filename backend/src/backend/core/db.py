# Standard library imports
import os
from contextlib import contextmanager
from typing import Iterator
import dotenv
from contextlib import contextmanager
# Third-party imports
import psycopg
from sqlalchemy import MetaData, create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session, registry
from sqlalchemy.ext.automap import automap_base


dotenv.load_dotenv()

_BaseCache = {}

engine: Engine

# -------- Small helper --------
def dev_mode_activated() -> bool:
    """DEV_SQLITE=1 enables SQLite; anything else disables it."""
    v = os.getenv("DEV_SQLITE", "").strip().lower()
    return v in {"1", "true", "yes", "y"}


def get_connection():
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    username = os.getenv("DB_USERNAME", "postgres")
    password = os.getenv("DB_PASSWORD", "postgres")
    database = os.getenv("DB_NAME", "postgres")
    return psycopg.connect(
        f"host={host} dbname={database} user={username} password={password} port={port}"
    )


# def get_engine_old():
#     """Create a SQLAlchemy engine using environment variables.
#     Environment Variables:
#         DB_HOST: Database host (default: localhost)
#         DB_PORT: Database port (default: 5432)
#         DB_USERNAME: Database username (default: postgres)
#         DB_PASSWORD: Database password (default: postgres)
#         DB_NAME: Database name (default: postgres)

#     Returns:
#         sqlalchemy.Engine: The SQLAlchemy engine instance.
#     """
#     host = os.getenv("DB_HOST", "localhost")
#     port = os.getenv("DB_PORT", "5432")
#     username = os.getenv("DB_USERNAME", "postgres")
#     password = os.getenv("DB_PASSWORD", "postgres")
#     database = os.getenv("DB_NAME", "postgres")
#     if dev_mode_activated():
#         # Use SQLite in dev mode
#         url = "sqlite:///./dev.db"
#         return create_engine(url, echo=True, connect_args={"check_same_thread": False})
#     else:
#         # SQLAlchemy connection string for psycopg3
#         url = f"postgresql+psycopg://{username}:{password}@{host}:{port}/{database}"
#         return create_engine(url, echo=True)  # echo=True logs SQL statements


# -------- Engine creation --------
def get_engine() -> Engine:
    """
    Postgres in normal mode; SQLite in dev mode.
    ECHO_SQL=1 to see SQL. Tweak pools safely.
    """
    echo = os.getenv("ECHO_SQL", "").strip() in {"1", "true", "yes"}
    if dev_mode_activated():
        url = "sqlite:///:memory:" # sqlite:///:memory: for purely in memory db OR "sqlite:///./dev.db" for file
        return create_engine(
            url,
            echo=echo,
            future=True,
            connect_args={"check_same_thread": False},
        )
    else:
        host = os.getenv("DB_HOST", "localhost")
        port = os.getenv("DB_PORT", "5432")
        user = os.getenv("DB_USERNAME", "postgres")
        pw = os.getenv("DB_PASSWORD", "postgres")
        db = os.getenv("DB_NAME", "postgres")
        url = f"postgresql+psycopg://{user}:{pw}@{host}:{port}/{db}"
        return create_engine(
            url,
            echo=echo,
            future=True,
            pool_pre_ping=True,       # drops dead conns
            pool_recycle=1800,        # refresh every 30 min
        )
    
engine = get_engine()

# -------- Session factory (no globals leaked) --------
def make_session_factory(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False, future=True)



# Optional raw psycopg for health/COPY
def get_psycopg_connection():
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    user = os.getenv("DB_USERNAME", "postgres")
    pw = os.getenv("DB_PASSWORD", "postgres")
    db = os.getenv("DB_NAME", "postgres")
    return psycopg.connect(f"host={host} dbname={db} user={user} password={pw} port={port}")

# -------- Minimal context/dependency --------
@contextmanager
def session_scope(SessionLocal: sessionmaker[Session]) -> Iterator[Session]:
    s = SessionLocal()
    try:
        yield s          # do work
        s.commit()
    except Exception:
        s.rollback()
        raise
    finally:
        s.close()

# FastAPI dependency example (sync)
def get_session_dep():
    """
    Yields a SQLAlchemy session for use in dependency-injected contexts (such as FastAPI routes).

    Example:
        func(session: Session = Depends(get_session_dep), ...)

    This generator function creates a new session, yields it for use, commits the transaction if no exceptions occur,
    rolls back on error, and always closes the session. It is designed to be used as a dependency in frameworks
    that support generator-based dependencies, ensuring proper transaction handling and resource cleanup.
    """
    # Removed engine creation to avoid global state issues and improve performance
    SessionLocal = make_session_factory(engine)
    s = SessionLocal()
    try:
        yield s
        s.commit()
    except Exception:
        s.rollback()
        raise
    finally:
        s.close()


@contextmanager
def get_session():
    """
    Context manager for creating a SQLAlchemy session outside FastAPI.

    Example:
        with get_session() as session:
            session.query(...)

    Behavior:
        - Opens a new session at block entry.
        - Yields the session to the caller.
        - Commits automatically on normal exit.
        - Rolls back if an exception occurs.
        - Always closes the session at the end.
    """
    SessionLocal = make_session_factory(engine)
    s = SessionLocal()
    try:
        yield s
        s.commit()  
    except Exception:
        s.rollback()
        raise
    finally:
        s.close()



def get_base( reload: bool = False):
    """
    Returns an automap Base bound to the given engine.
    If reload=True, rebuilds the base (useful after schema changes).
    """
    global _BaseCache

    if not reload and engine in _BaseCache:
        return _BaseCache[engine]

    Base = automap_base()
    Base.prepare(autoload_with=engine)  # SQLAlchemy >=1.4
    _BaseCache[engine] = Base
    return Base



if __name__ == "__main__":
    print(dev_mode_activated())
    # Smoke test
    engine = get_engine()
    SessionLocal = make_session_factory(engine)
    with session_scope(SessionLocal) as s:
        s.execute(text('SELECT 1'))
    print("OK")
