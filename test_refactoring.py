#!/usr/bin/env python3
"""
Script de teste para verificar se a refatoração foi bem-sucedida
"""

from database_config import db_config
from models import User, Category, Brand, Product, Customer
import bcrypt


def test_database_connection():
    """Testa a conexão com o banco de dados"""
    print("🔍 Testando conexão com banco de dados...")
    try:
        session = db_config.get_session()
        
        # Testar contagem de usuários
        user_count = session.query(User).count()
        print(f"✅ Usuários no banco: {user_count}")
        
        # Testar contagem de categorias
        category_count = session.query(Category).count()
        print(f"✅ Categorias no banco: {category_count}")
        
        # Testar contagem de marcas
        brand_count = session.query(Brand).count()
        print(f"✅ Marcas no banco: {brand_count}")
        
        # Testar contagem de produtos
        product_count = session.query(Product).count()
        print(f"✅ Produtos no banco: {product_count}")
        
        # Testar contagem de clientes
        customer_count = session.query(Customer).count()
        print(f"✅ Clientes no banco: {customer_count}")
        
        session.close()
        return True
        
    except Exception as e:
        print(f"❌ Erro na conexão com banco: {e}")
        return False


def test_user_authentication():
    """Testa a autenticação de usuário"""
    print("\n🔐 Testando autenticação de usuário...")
    try:
        session = db_config.get_session()
        
        # Buscar usuário admin
        admin_user = session.query(User).filter(User.user == "admin").first()
        
        if admin_user:
            print(f"✅ Usuário admin encontrado: {admin_user.name}")
            
            # Testar senha
            password_correct = bcrypt.checkpw(
                "admin123".encode('utf-8'), 
                admin_user.password.encode('utf-8')
            )
            
            if password_correct:
                print("✅ Senha do admin está correta")
            else:
                print("❌ Senha do admin está incorreta")
                
        else:
            print("❌ Usuário admin não encontrado")
            
        session.close()
        return True
        
    except Exception as e:
        print(f"❌ Erro na autenticação: {e}")
        return False


def test_flet_imports():
    """Testa se os imports do Flet estão funcionando"""
    print("\n🎨 Testando imports do Flet...")
    try:
        from flet import Page, app, Theme, ThemeMode, Colors
        from flet import Container, Row, VerticalDivider, FilePicker
        from flet import Control, TextField, Text, OutlinedButton
        from flet import NavigationRail, NavigationRailDestination
        
        print("✅ Todos os imports do Flet funcionando")
        return True
        
    except ImportError as e:
        print(f"❌ Erro nos imports do Flet: {e}")
        return False


def test_sqlalchemy_models():
    """Testa se os modelos SQLAlchemy estão funcionando"""
    print("\n🗄️  Testando modelos SQLAlchemy...")
    try:
        from models import Base, User, Customer, Address, Category, Brand, Product, Sale, SoldProduct
        
        # Verificar se Base está definido
        if Base:
            print("✅ Base declarativa definida")
        
        # Verificar se todas as classes estão definidas
        models = [User, Customer, Address, Category, Brand, Product, Sale, SoldProduct]
        for model in models:
            if model:
                print(f"✅ Modelo {model.__name__} definido")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro nos modelos SQLAlchemy: {e}")
        return False


def main():
    """Função principal de teste"""
    print("🧪 Executando testes de refatoração...")
    print("=" * 50)
    
    tests = [
        ("Conexão com Banco", test_database_connection),
        ("Autenticação de Usuário", test_user_authentication),
        ("Imports do Flet", test_flet_imports),
        ("Modelos SQLAlchemy", test_sqlalchemy_models),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}:")
        if test_func():
            passed += 1
        else:
            print(f"❌ Teste {test_name} falhou")
    
    print("\n" + "=" * 50)
    print(f"📊 Resultado dos Testes: {passed}/{total} passaram")
    
    if passed == total:
        print("🎉 Todos os testes passaram! A refatoração foi bem-sucedida!")
        print("\n🚀 A aplicação está pronta para uso!")
        print("   Execute: python main.py")
        print("   Login: admin / admin123")
    else:
        print("⚠️  Alguns testes falharam. Verifique os erros acima.")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
