import pytest
from database import Database

@pytest.fixture
def test_db():
    """Fixture para la base de datos de pruebas"""
    db = Database(":memory:")  # Usa una base de datos en memoria
    yield db
    db.close()