#!/usr/bin/env python3
"""
Script para inicializar o banco SQLite com dados de exemplo
"""

from datetime import date
import bcrypt
from database_config import db_config
from models import User, Category, Brand, Product, Customer, Address


def create_sample_data():
    """Cria dados de exemplo no banco"""
    session = db_config.get_session()
    
    try:
        # Verificar se já existe usuário admin
        existing_admin = session.query(User).filter(User.user == "admin").first()
        if existing_admin:
            print("👤 Usuário admin já existe!")
            return
        
        # Criar usuário administrador
        admin_password = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt())
        admin_user = User(
            name="Administrador",
            user="admin",
            password=admin_password.decode('utf-8'),
            date=date.today(),
            acesso="Admin"
        )
        session.add(admin_user)
        
        # Criar categorias
        categories = ["Eletrônicos", "Roupas", "Livros", "Casa e Jardim"]
        for cat_name in categories:
            category = Category(category=cat_name)
            session.add(category)
        
        # Criar marcas
        brands = ["Samsung", "Apple", "Nike", "Adidas", "Saraiva"]
        for brand_name in brands:
            brand = Brand(brand=brand_name)
            session.add(brand)
        
        session.commit()
        
        # Criar produtos
        products_data = [
            ("Smartphone Galaxy", "Eletrônicos", "Samsung", 50, 10, 100, "Produto novo", 800.0, 1200.0, 33.33),
            ("iPhone 15", "Eletrônicos", "Apple", 30, 5, 50, "Última geração", 1500.0, 2000.0, 25.0),
            ("Tênis Air Max", "Roupas", "Nike", 25, 5, 50, "Esportivo", 200.0, 350.0, 42.86),
            ("Livro Python", "Livros", "Saraiva", 100, 20, 200, "Programação", 50.0, 80.0, 37.5),
        ]
        
        for prod_data in products_data:
            # Buscar categoria e marca
            category = session.query(Category).filter(Category.category == prod_data[1]).first()
            brand = session.query(Brand).filter(Brand.brand == prod_data[2]).first()
            
            if category and brand:
                product = Product(
                    descr=prod_data[0],
                    idcategory=category.idcategory,
                    idbrand=brand.idbrand,
                    stock=prod_data[3],
                    minstock=prod_data[4],
                    maxstock=prod_data[5],
                    observ=prod_data[6],
                    costs=prod_data[7],
                    sellprice=prod_data[8],
                    margin=prod_data[9]
                )
                session.add(product)
        
        # Criar cliente de exemplo
        customer = Customer(
            name="João Silva",
            cpf_cnpj="123.456.789-00",
            tel="(11) 99999-9999",
            email="joao@email.com",
            observ="Cliente VIP",
            date=date.today()
        )
        session.add(customer)
        session.commit()
        
        # Criar endereço do cliente
        address = Address(
            cod_customer="123.456.789-00",
            ender="Rua das Flores, 123",
            cidade="São Paulo",
            uf="SP",
            CEP="01234-567"
        )
        session.add(address)
        
        session.commit()
        print("✅ Dados de exemplo criados com sucesso!")
        print("👤 Usuário: admin / Senha: admin123")
        
    except Exception as e:
        session.rollback()
        print(f"❌ Erro ao criar dados de exemplo: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    print("🚀 Inicializando banco SQLite com dados de exemplo...")
    
    # Criar tabelas
    db_config.create_tables()
    print("✅ Tabelas criadas com sucesso!")
    
    # Criar dados de exemplo
    create_sample_data()
    
    print("🎉 Inicialização concluída!")
