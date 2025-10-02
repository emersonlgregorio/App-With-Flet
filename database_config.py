from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base


class DatabaseConfig:
    def __init__(self):
        # Para desenvolvimento, usar SQLite
        self.database_url = "sqlite:///infostore_dev.db"
        self.engine = None
        self.SessionLocal = None
        
    def create_engine_and_session(self):
        """Cria engine e session factory para SQLite"""
        self.engine = create_engine(
            self.database_url,
            echo=False,  # Mude para True para ver as queries SQL
            connect_args={"check_same_thread": False}  # Necessário para SQLite
        )
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False,
                                        bind=self.engine)
        return self.engine, self.SessionLocal
    
    def create_tables(self):
        """Cria todas as tabelas no banco de dados"""
        if self.engine is None:
            self.create_engine_and_session()
        Base.metadata.create_all(bind=self.engine)
    
    def get_session(self):
        """Retorna uma sessão do banco de dados"""
        if self.SessionLocal is None:
            self.create_engine_and_session()
        return self.SessionLocal()
    
    def close_engine(self):
        """Fecha a conexão com o banco"""
        if self.engine:
            self.engine.dispose()


# Instância global da configuração
db_config = DatabaseConfig()
