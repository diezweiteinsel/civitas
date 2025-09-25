import pytest
from sqlalchemy import create_engine, text

from backend import db


def test_dev_mode_flag(monkeypatch):
    # ensure default (unset) is false
    monkeypatch.delenv("DEV_SQLITE", raising=False)
    assert not db.dev_mode_activated()

    # truthy values should enable dev mode
    monkeypatch.setenv("DEV_SQLITE", "1")
    assert db.dev_mode_activated()
    monkeypatch.setenv("DEV_SQLITE", "true")
    assert db.dev_mode_activated()


def test_get_engine_sqlite(monkeypatch):
    # force dev sqlite mode
    monkeypatch.setenv("DEV_SQLITE", "1")
    engine = db.get_engine()
    # should be a sqlite engine and be able to execute a simple statement
    assert engine.dialect.name == "sqlite"
    with engine.connect() as conn:
        r = conn.execute(text("SELECT 1")).scalar()
    assert int(r) == 1


def test_make_session_factory_and_session_scope_commits():
    # create an in-memory engine for isolation
    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}, future=True
    )
    SessionLocal = db.make_session_factory(engine)

    # create a table and insert inside session_scope (should commit)
    with engine.begin() as conn:
        conn.execute(text("CREATE TABLE test_tbl (id INTEGER PRIMARY KEY, name TEXT)"))

    with db.session_scope(SessionLocal) as s:
        s.execute(text("INSERT INTO test_tbl (name) VALUES ('alice')"))

    # verify the row was committed
    with engine.connect() as conn:
        r = conn.execute(text("SELECT count(*) FROM test_tbl")).scalar()
    assert int(r) == 1


def test_get_session_dep_generator_commits_and_closes(monkeypatch):
    # Provide an in-memory engine and patch get_engine so get_session_dep uses it
    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}, future=True
    )
    monkeypatch.setattr(db, "engine", engine)

    gen = db.get_session_dep()
    s = next(gen)  # obtains the yielded session
    assert hasattr(s, "execute")

    # create table and insert using the yielded session
    s.execute(text("CREATE TABLE t (id INTEGER PRIMARY KEY, name TEXT)"))
    s.execute(text("INSERT INTO t (name) VALUES ('bob')"))

    # advance generator to let it commit and finalize
    with pytest.raises(StopIteration):
        next(gen)

    # verify committed
    with engine.connect() as conn:
        r = conn.execute(text("SELECT count(*) FROM t")).scalar()
    assert int(r) == 1
