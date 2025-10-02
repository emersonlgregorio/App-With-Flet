import os
import json
from cryptography.fernet import Fernet

from CreateConfig import CreateConfig
from database_config import db_config

class Config:
    def __init__(self, route) -> None:
        self.route = route
        self.host = None
        self.user = None
        self.passwd = None
        self.database = None
        self.port = None

        self.user_name = None
        self.permission = None

        self.company_name = "NOME DA SUA EMPRESA"
        self.company_adress = "Endereço completo da sua Empresa aqui"
        self.company_tel = "Telefone da sua Empresa aqui"
        self.company_email = "E-mail da sua Empresa aqui"

    def read_file(self):
        """Lê arquivo de configuração criptografado"""
        with open("data.bin", "rb") as file:
            readed_key = file.readline().rstrip()
            readed_data = file.read()
        return readed_data, readed_key

    def decrypt_data(self, encrypted_data, key):
        """Descriptografa dados"""
        fernet = Fernet(key)
        return fernet.decrypt(encrypted_data).decode()

    def set_config_data(self, data):
        """Define dados de configuração"""
        self.host = data["host"]
        self.user = data["user"]
        self.passwd = data["passwd"]
        self.database = data["database"]
        self.port = data["port"]

    def set_permissions(self, name, permission):
        """Define permissões do usuário"""
        self.route.config.user_name = name
        self.route.config.permission = permission
        
        self.route.menu.nnrail.destinations[2].visible = (
            self.route.config.permission == "Admin"
        )
        self.route.menu.nnrail.update()

    def open_config_db(self):
        """Abre diálogo de configuração do banco"""
        dialog = CreateConfig(self.route)
        self.route.page.dialog = dialog
        dialog.open = True
        self.route.page.update()

    def initialize(self):
        """Inicializa configuração - para desenvolvimento usa SQLite diretamente"""
        # Para desenvolvimento, usar SQLite diretamente
        if not os.path.exists("infostore_dev.db"):
            # Criar banco SQLite e tabelas
            db_config.create_tables()
            print("Banco SQLite criado com sucesso!")
        
        # Para compatibilidade, definir valores padrão
        self.host = "localhost"
        self.user = "sqlite"
        self.passwd = ""
        self.database = "infostore_dev.db"
        self.port = 0
        
        # Se existe arquivo de configuração, usar ele (para produção)
        if os.path.exists("data.bin"):
            try:
                readed_data, readed_key = self.read_file()
                decrypted_data = self.decrypt_data(readed_data, readed_key)
                config_dict = json.loads(decrypted_data)
                self.set_config_data(config_dict)
            except Exception as e:
                print(f"Erro ao ler configuração: {e}")
                # Continuar com SQLite em caso de erro
            

    