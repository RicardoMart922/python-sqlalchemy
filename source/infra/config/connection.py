from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

class DBConnectionHandler:
    """Classe para gerenciar a conexão e sessão com o banco de dados usando SQLAlchemy."""

    def __init__(self) -> None:
        self.__connection_string = 'sqlite:///:memory:'
        self.__engine = self.__create_database_engine()
        self.__Session = sessionmaker(bind=self.__engine)  # Criação do sessionmaker uma vez
        self.session: Session | None = None

    def __create_database_engine(self) -> create_engine:
        """Cria a engine de conexão com o banco de dados."""
        return create_engine(self.__connection_string)

    def get_engine(self) -> create_engine:
        """Retorna a engine do banco de dados."""
        return self.__engine

    def __enter__(self) -> "DBConnectionHandler":
        """Inicializa a sessão quando a classe é usada em um gerenciador de contexto."""
        self.session = self.__Session()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Fecha a sessão ao sair do contexto, tratando qualquer exceção."""
        if self.session:
            try:
                self.session.close()
                self.session = None
            except Exception as e:
                print(f"Erro ao fechar a sessão: {e}")

