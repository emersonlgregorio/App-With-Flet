#!/usr/bin/env python3
"""
Script de configuração do ambiente de desenvolvimento
Atualiza dependências e inicializa o banco SQLite
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description):
    """Executa um comando e mostra o resultado"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        print(f"✅ {description} concluído!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro em {description}:")
        print(f"   {e.stderr}")
        return False


def main():
    """Função principal de configuração"""
    print("🚀 Configurando ambiente de desenvolvimento...")
    print("=" * 50)
    
    # Verificar se estamos no ambiente virtual
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  AVISO: Parece que você não está em um ambiente virtual!")
        print("   Execute: source .venv/bin/activate")
        print("   E depois execute este script novamente.")
        return False
    
    print(f"✅ Ambiente virtual ativo: {sys.prefix}")
    
    # Atualizar pip
    if not run_command("pip install --upgrade pip", "Atualizando pip"):
        return False
    
    # Instalar dependências
    if not run_command("pip install -r requirements.txt", "Instalando dependências"):
        return False
    
    # Verificar instalação do Flet
    try:
        import flet
        version = getattr(flet, '__version__', 'versão não disponível')
        print(f"✅ Flet instalado: {version}")
    except ImportError:
        print("❌ Flet não foi instalado corretamente!")
        return False
    
    # Verificar instalação do SQLAlchemy
    try:
        import sqlalchemy
        print(f"✅ SQLAlchemy instalado: versão {sqlalchemy.__version__}")
    except ImportError:
        print("❌ SQLAlchemy não foi instalado corretamente!")
        return False
    
    # Inicializar banco de dados
    print("\n🗄️  Inicializando banco de dados...")
    try:
        from init_db import create_sample_data
        from database_config import db_config
        
        # Criar tabelas
        db_config.create_tables()
        print("✅ Tabelas criadas!")
        
        # Criar dados de exemplo
        create_sample_data()
        
    except Exception as e:
        print(f"❌ Erro ao inicializar banco: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 Configuração concluída com sucesso!")
    print("\n📋 Próximos passos:")
    print("   1. Execute: python main.py")
    print("   2. Use: admin / admin123 para fazer login")
    print("   3. Explore as funcionalidades do sistema!")
    print("\n💡 Dicas:")
    print("   - O banco SQLite está em: infostore_dev.db")
    print("   - Para resetar o banco, delete o arquivo e execute novamente")
    print("   - Todas as dependências estão atualizadas para versões estáveis")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
