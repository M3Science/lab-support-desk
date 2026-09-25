import pytest

from support_desk.db import build
from support_desk.reports import kpis, run_all


@pytest.fixture(scope="session")
def conn(tmp_path_factory):
    c = build(tmp_path_factory.mktemp("db") / "test.db")
    yield c
    c.close()


@pytest.fixture(scope="session")
def reports(conn):
    return run_all(conn)


@pytest.fixture(scope="session")
def k(conn):
    return kpis(conn)
