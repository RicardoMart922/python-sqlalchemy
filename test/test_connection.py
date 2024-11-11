import pytest
from source.infra.config.connection import DBConnectionHandler


class TestConnection:
    def test_create_session(self):
        """Teste para verificar se a sessão é criada corretamente dentro do contexto"""
        with DBConnectionHandler() as db_handler:
            # Verifica se a sessão foi criada
            assert db_handler.session is not None
            # Verifica se a sessão está ativa
            assert db_handler.session.is_active is True

    def test_engine_creation(self):
        """Teste para verificar se a engine do banco de dados foi criada"""
        db_handler = DBConnectionHandler()
        engine = db_handler.get_engine()
        # Verifica se a engine foi criada corretamente
        assert engine is not None
        assert str(engine.url) == 'sqlite:///:memory:'
