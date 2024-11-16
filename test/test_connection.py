import pytest
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
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

    def test_create_database_engine(self):
        """Testa se a engine do banco de dados é criada corretamente."""
        db_handler = DBConnectionHandler()
        engine = db_handler.get_engine()
        assert isinstance(engine, Engine), "A engine deve ser uma instância de sqlalchemy.engine.Engine."

    def test_session_initially_none(self):
        """Testa se a sessão é inicialmente None."""
        db_handler = DBConnectionHandler()
        assert db_handler.session is None, "A sessão deve ser None ao inicializar a classe."

    def test_session_created_in_context(self):
        """Testa se a sessão é criada corretamente no gerenciador de contexto."""
        db_handler = DBConnectionHandler()
        with db_handler as handler:
            assert isinstance(handler.session, Session), "A sessão deve ser uma instância de sqlalchemy.orm.Session."
        assert handler.session is None, "A sessão deve ser None após sair do contexto."

    def test_session_closes_correctly(self):
        """Testa se a sessão é fechada corretamente ao sair do contexto."""
        db_handler = DBConnectionHandler()
        with db_handler as handler:
            session_id = id(handler.session)
            assert isinstance(handler.session, Session), "A sessão deve ser criada no contexto."
        # Após o contexto, a sessão deve ser None
        assert handler.session is None, "A sessão deve ser None após sair do contexto."
        # Garantir que a sessão foi fechada e não é a mesma
        with db_handler as handler:
            assert id(handler.session) != session_id, "A sessão deve ser recriada para um novo contexto."

    def test_engine_reusability(self):
        """Testa se a engine é reutilizada em múltiplas instâncias."""
        db_handler1 = DBConnectionHandler()
        db_handler2 = DBConnectionHandler()
        assert str(db_handler1.get_engine()) == str(db_handler2.get_engine()), "A mesma engine deve ser reutilizada."