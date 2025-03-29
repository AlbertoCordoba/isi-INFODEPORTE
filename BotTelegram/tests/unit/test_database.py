import pytest
from sqlite3 import IntegrityError

def test_add_user(test_db):
    """Prueba añadir usuario nuevo y duplicado"""
    # Caso exitoso
    test_db.add_user(123, "user1", "Ana", "Pérez")
    assert test_db.is_user_subscribed(123, "nba") is False  # Verifica existencia

    # Caso duplicado (no debe fallar)
    test_db.add_user(123, "user1_updated", "Ana María", "Pérez")
    cursor = test_db.cursor.execute("SELECT username FROM users WHERE chat_id=123")
    assert cursor.fetchone()[0] == "user1_updated"  # Verifica actualización

def test_subscribe_user(test_db):
    """Prueba suscripciones válidas e inválidas"""
    test_db.add_user(123, "user1", "Ana", "Pérez")
    
    # Suscripción exitosa
    test_db.subscribe_user(123, "nhl")
    assert test_db.is_user_subscribed(123, "nhl") is True

    # Suscripción duplicada (no debe fallar)
    test_db.subscribe_user(123, "nhl")
    subs = test_db.get_user_subscriptions(123)
    assert subs.count("nhl") == 1  # No duplicados

    # Suscripción a usuario inexistente
    with pytest.raises(ValueError):
        test_db.subscribe_user(999, "nhl")  # UserID no existe

def test_unsubscribe_user(test_db):
    """Prueba desuscripciones"""
    test_db.add_user(123, "user1", "Ana", "Pérez")
    test_db.subscribe_user(123, "nhl")
    
    # Desuscripción exitosa
    test_db.unsubscribe_user(123, "nhl")
    assert test_db.is_user_subscribed(123, "nhl") is False

    # Desuscripción de deporte no suscrito (no debe fallar)
    test_db.unsubscribe_user(123, "nba")  # No estaba suscrito

def test_get_user_subscriptions(test_db):
    """Prueba obtención de suscripciones"""
    test_db.add_user(123, "user1", "Ana", "Pérez")
    test_db.subscribe_user(123, "nhl")
    test_db.subscribe_user(123, "nba")
    
    assert set(test_db.get_user_subscriptions(123)) == {"nhl", "nba"}
    assert test_db.get_user_subscriptions(999) == []  # Usuario inexistente

def test_get_all_subscriptions(test_db):
    """Prueba listado global de suscripciones"""
    test_db.add_user(123, "user1", "Ana", "Pérez")
    test_db.add_user(456, "user2", "Carlos", "López")
    test_db.subscribe_user(123, "nhl")
    test_db.subscribe_user(456, "nba")
    
    subs = test_db.get_all_subscriptions()
    assert len(subs) == 2
    assert ("Ana", "nhl") in [(u[1], u[2]) for u in subs]

