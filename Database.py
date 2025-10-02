from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc
from datetime import date, timedelta
import bcrypt
from typing import List, Optional, Tuple, Any

from models import User, Customer, Address, Category, Brand, Product, Sale, SoldProduct
from database_config import db_config

class UserDatabase:
    def __init__(self, route) -> None:
        self.route = route
        self.session: Session = db_config.get_session()

    def close(self):
        """Fecha a sessão do banco de dados"""
        if self.session:
            self.session.close()

    def register_user(self, fullDataSet):
        """Registra um novo usuário"""
        try:
            user = User(
                name=fullDataSet[0],
                user=fullDataSet[1],
                password=fullDataSet[2],
                date=fullDataSet[3],
                acesso=fullDataSet[4]
            )
            self.session.add(user)
            self.session.commit()
            return 'success'
        except Exception as e:
            self.session.rollback()
            return str(e)
        
    def select_all_users(self):
        """Seleciona todos os usuários"""
        try:
            users = self.session.query(User.idUser, User.name, User.user, User.acesso).order_by(User.name).all()
            return users
        except Exception:
            return None
        
    def select_one_user(self, id):
        """Seleciona um usuário por ID"""
        try:
            user = self.session.query(User).filter(User.idUser == int(id)).first()
            return user
        except Exception:
            return None

    def delete_user(self, id):
        """Deleta um usuário por ID"""
        try:
            print(f"🔍 Database: Tentando excluir usuário ID: {id}")
            user = self.session.query(User).filter(User.idUser == id).first()
            print(f"🔍 Database: Usuário encontrado: {user}")
            if user:
                print(f"🔍 Database: Usuário encontrado - Nome: {user.name}, ID: {user.idUser}")
                self.session.delete(user)
                print(f"🔍 Database: Usuário marcado para exclusão")
                self.session.commit()
                print(f"🔍 Database: Commit realizado com sucesso")
                return 'success'
            print(f"🔍 Database: Usuário não encontrado")
            return 'User not found'
        except Exception as e:
            print(f"🔍 Database: Erro ao excluir usuário: {str(e)}")
            self.session.rollback()
            return str(e)
        
    def update_user(self, fullDataSet):
        """Atualiza um usuário"""
        try:
            user = self.session.query(User).filter(User.idUser == fullDataSet[0]).first()
            if user:
                user.name = fullDataSet[1]
                user.user = fullDataSet[2]
                user.password = fullDataSet[3]
                user.date = fullDataSet[4]
                user.acesso = fullDataSet[5]
                self.session.commit()
                return 'success'
            return 'User not found'
        except Exception as e:
            self.session.rollback()
            return str(e)
       
    def verify_pass(self, password, saved_hash):
        """Verifica a senha usando bcrypt"""
        return bcrypt.checkpw(password.encode('utf-8'), saved_hash.encode('utf-8'))
    
    def login_verify(self, data):
        """Verifica login do usuário"""
        try:
            user = self.session.query(User).filter(User.user == data[0]).first()
            if user and self.verify_pass(data[1], user.password):
                return user.name.upper(), user.acesso
            return None, None
        except Exception:
            return None, None
        
    def find_user(self, text):
        """Busca usuários por texto"""
        try:
            pattern = f"%{text}%"
            users = self.session.query(User.idUser, User.name, User.user, User.acesso).filter(
                or_(
                    User.idUser.like(pattern),
                    User.name.like(pattern),
                    User.user.like(pattern)
                )
            ).all()
            return users
        except Exception:
            return None
        
    def select_users_count(self):
        """Conta o número de usuários"""
        try:
            count = self.session.query(func.count(User.idUser)).scalar()
            return str(count)
        except Exception:
            return "0"

class CustomerDatabase:
    def __init__(self, route) -> None:
        self.route = route
        self.session: Session = db_config.get_session()

    def close(self):
        """Fecha a sessão do banco de dados"""
        if self.session:
            self.session.close()

    def register_customer(self, fullDataSet):
        """Registra um novo cliente"""
        try:
            customer = Customer(
                name=fullDataSet[0],
                cpf_cnpj=fullDataSet[1],
                tel=fullDataSet[2],
                email=fullDataSet[3],
                observ=fullDataSet[4],
                date=fullDataSet[5]
            )
            self.session.add(customer)
            self.session.commit()
            return 'success'
        except Exception as e:
            self.session.rollback()
            return str(e)
        
    def register_adress(self, fullDataSet):
        """Registra um endereço para um cliente"""
        try:
            address = Address(
                cod_customer=fullDataSet[0],
                ender=fullDataSet[1],
                cidade=fullDataSet[2],
                uf=fullDataSet[3],
                CEP=fullDataSet[4]
            )
            self.session.add(address)
            self.session.commit()
            return 'success'
        except Exception as e:
            self.session.rollback()
            return str(e)

    def select_customers(self):
        """Seleciona todos os clientes"""
        try:
            customers = self.session.query(
                Customer.idcustomers, Customer.name, Customer.cpf_cnpj, Customer.tel
            ).order_by(Customer.name).all()
            return customers
        except Exception:
            return None
        
    def select_one_customer(self, cpf_cnpj):
        """Seleciona um cliente por CPF/CNPJ"""
        try:
            customer = self.session.query(Customer).filter(Customer.cpf_cnpj == cpf_cnpj).first()
            if customer:
                return [(customer.idcustomers, customer.name, customer.cpf_cnpj, 
                        customer.tel, customer.email, customer.observ, customer.date)]
            return None
        except Exception:
            return None
    
    def select_adresses(self, cpf_cnpj):
        """Seleciona endereços de um cliente"""
        try:
            addresses = self.session.query(
                Address.ender, Address.cidade, Address.uf, Address.CEP
            ).filter(Address.cod_customer == cpf_cnpj).order_by(Address.cidade).all()
            return addresses
        except Exception:
            return None

    def update_customer(self, data_customer):
        """Atualiza dados de um cliente"""
        try:
            customer = self.session.query(Customer).filter(Customer.idcustomers == data_customer[0]).first()
            if customer:
                # Remove endereços antigos
                self.session.query(Address).filter(Address.cod_customer == customer.cpf_cnpj).delete()
                
                # Atualiza dados do cliente
                customer.name = data_customer[1]
                customer.cpf_cnpj = data_customer[2]
                customer.tel = data_customer[3]
                customer.email = data_customer[4]
                customer.observ = data_customer[5]
                
                self.session.commit()
                return 'success'
            return 'Customer not found'
        except Exception as e:
            self.session.rollback()
            return str(e)
        
    def delete_customer(self, cpf_cnpj):
        """Deleta um cliente e seus endereços"""
        try:
            customer = self.session.query(Customer).filter(Customer.cpf_cnpj == cpf_cnpj).first()
            if customer:
                self.session.delete(customer)  # Cascade vai deletar os endereços
                self.session.commit()
                return 'success'
            return 'Customer not found'
        except Exception as e:
            self.session.rollback()
            return str(e)

    def find_customer(self, text):
        """Busca clientes por texto"""
        try:
            pattern = f"%{text}%"
            customers = self.session.query(
                Customer.idcustomers, Customer.name, Customer.cpf_cnpj, Customer.tel
            ).filter(
                or_(
                    Customer.idcustomers.like(pattern),
                    Customer.name.like(pattern),
                    Customer.cpf_cnpj.like(pattern),
                    Customer.tel.like(pattern)
                )
            ).all()
            return customers
        except Exception as e:
            return str(e)

class ProductsDatabase:
    def __init__(self, route) -> None:
        self.route = route
        self.session: Session = db_config.get_session()

    def close(self):
        """Fecha a sessão do banco de dados"""
        if self.session:
            self.session.close()
        
    def register_category(self, category):
        """Registra uma nova categoria"""
        try:
            new_category = Category(category=category)
            self.session.add(new_category)
            self.session.commit()
            return 'success'
        except Exception as e:
            self.session.rollback()
            return str(e)
        
    def register_brand(self, brand):
        """Registra uma nova marca"""
        try:
            new_brand = Brand(brand=brand)
            self.session.add(new_brand)
            self.session.commit()
            return 'success'
        except Exception as e:
            self.session.rollback()
            return str(e)

    def select_category(self):
        """Seleciona todas as categorias"""
        try:
            categories = self.session.query(Category).order_by(Category.category).all()
            return categories
        except Exception:
            return None

    def select_brand(self):
        """Seleciona todas as marcas"""
        try:
            brands = self.session.query(Brand).order_by(Brand.brand).all()
            return brands
        except Exception:
            return None

    def delete_category(self, idcategory):
        """Deleta uma categoria"""
        try:
            category = self.session.query(Category).filter(Category.idcategory == idcategory).first()
            if category:
                self.session.delete(category)
                self.session.commit()
                return 'success'
            return 'Category not found'
        except Exception as e:
            self.session.rollback()
            return str(e)
        
    def delete_brand(self, idbrand):
        """Deleta uma marca"""
        try:
            brand = self.session.query(Brand).filter(Brand.idbrand == idbrand).first()
            if brand:
                self.session.delete(brand)
                self.session.commit()
                return 'success'
            return 'Brand not found'
        except Exception as e:
            self.session.rollback()
            return str(e)

    def register_products(self, fulldataset):
        """Registra um novo produto"""
        try:
            # Busca IDs da categoria e marca
            category = self.session.query(Category).filter(Category.category == fulldataset[1]).first()
            brand = self.session.query(Brand).filter(Brand.brand == fulldataset[2]).first()
            
            if not category or not brand:
                return 'Category or brand not found'
            
            product = Product(
                descr=fulldataset[0],
                idcategory=category.idcategory,
                idbrand=brand.idbrand,
                stock=fulldataset[3],
                minstock=fulldataset[4],
                maxstock=fulldataset[5],
                observ=fulldataset[6],
                costs=fulldataset[7],
                sellprice=fulldataset[8],
                margin=fulldataset[9]
            )
            self.session.add(product)
            self.session.commit()
            return 'success'
        except Exception as e:
            self.session.rollback()
            return str(e)

    def select_products(self):
        """Seleciona todos os produtos com joins"""
        try:
            products = self.session.query(
                Product.idproducts,
                Product.descr,
                Category.category,
                Brand.brand,
                Product.sellprice,
                Product.stock,
                Product.minstock
            ).join(Category).join(Brand).order_by(Product.descr).all()
            
            # Formatar resultado para compatibilidade com o código existente
            formatted_products = []
            for p in products:
                formatted_products.append((
                    str(p.idproducts),
                    p.descr,
                    p.category,
                    p.brand,
                    f"{p.sellprice:.2f}",
                    p.stock,
                    p.minstock
                ))
            return formatted_products
        except Exception as e:
            return str(e)
    
    def select_products_full(self, idproducts):
        """Seleciona um produto completo por ID"""
        try:
            product = self.session.query(
                Product.idproducts,
                Product.descr,
                Category.category,
                Brand.brand,
                Product.stock,
                Product.minstock,
                Product.maxstock,
                Product.observ,
                Product.costs,
                Product.sellprice,
                Product.margin
            ).join(Category).join(Brand).filter(Product.idproducts == idproducts).first()
            
            if product:
                return (
                    str(product.idproducts),
                    product.descr,
                    product.category,
                    product.brand,
                    str(product.stock),
                    str(product.minstock),
                    str(product.maxstock),
                    product.observ,
                    str(product.costs),
                    str(product.sellprice),
                    str(product.margin)
                )
            return None
        except Exception as e:
            print(e)
            return None

    def update_products(self, data_products):
        """Atualiza um produto"""
        try:
            product = self.session.query(Product).filter(Product.idproducts == data_products[0]).first()
            if product:
                # Busca categoria e marca
                category = self.session.query(Category).filter(Category.category == data_products[2]).first()
                brand = self.session.query(Brand).filter(Brand.brand == data_products[3]).first()
                
                if category and brand:
                    product.descr = data_products[1]
                    product.idcategory = category.idcategory
                    product.idbrand = brand.idbrand
                    product.stock = data_products[4]
                    product.minstock = data_products[5]
                    product.maxstock = data_products[6]
                    product.observ = data_products[7]
                    product.costs = data_products[8]
                    product.sellprice = data_products[9]
                    product.margin = data_products[10]
                    
                    self.session.commit()
                    return 'success'
                return 'Category or brand not found'
            return 'Product not found'
        except Exception as e:
            self.session.rollback()
            return str(e)

    def delete_products(self, id_product):
        """Deleta um produto"""
        try:
            product = self.session.query(Product).filter(Product.idproducts == id_product).first()
            if product:
                self.session.delete(product)
                self.session.commit()
                return 'success'
            return 'Product not found'
        except Exception as e:
            self.session.rollback()
            return str(e)

    def find_product(self, text):
        """Busca produtos por texto"""
        try:
            pattern = f"%{text}%"
            products = self.session.query(
                Product.idproducts,
                Product.descr,
                Category.category,
                Brand.brand,
                Product.sellprice,
                Product.stock,
                Product.minstock
            ).join(Category).join(Brand).filter(
                or_(
                    Product.idproducts.like(pattern),
                    Product.descr.like(pattern),
                    Product.sellprice.like(pattern),
                    Category.category.like(pattern),
                    Brand.brand.like(pattern)
                )
            ).order_by(Product.descr).all()
            
            formatted_products = []
            for p in products:
                formatted_products.append((
                    str(p.idproducts),
                    p.descr,
                    p.category,
                    p.brand,
                    f"{p.sellprice:.2f}",
                    p.stock,
                    p.minstock
                ))
            return formatted_products
        except Exception as e:
            return str(e)

    def find_product_by_code(self, id):
        """Busca produto por código"""
        try:
            product = self.session.query(
                Product.idproducts,
                Product.descr,
                Product.idcategory,
                Product.idbrand,
                Product.sellprice,
                Product.costs,
                Product.stock,
                Brand.brand
            ).join(Brand).filter(Product.idproducts == id).first()
            return product
        except Exception as e:
            return str(e)

    def find_product_by_description(self, descr):
        """Busca produto por descrição"""
        try:
            pattern = f"%{descr}%"
            product = self.session.query(
                Product.idproducts,
                Product.descr,
                Product.idcategory,
                Product.idbrand,
                Product.sellprice,
                Product.costs,
                Product.stock,
                Brand.brand
            ).join(Brand).filter(Product.descr.like(pattern)).first()
            return product
        except Exception as e:
            return str(e)
    
    def update_stock(self, data):
        """Atualiza estoque de um produto"""
        try:
            product = self.session.query(Product).filter(Product.idproducts == data[0]).first()
            if product:
                product.stock += data[1]
                self.session.commit()
                return "success"
            return "Product not found"
        except Exception as e:
            self.session.rollback()
            return str(e)
        
    def select_low_stock(self):
        """Seleciona produtos com estoque baixo"""
        try:
            products = self.session.query(
                Product.idproducts,
                Product.descr,
                Category.category,
                Brand.brand,
                Product.sellprice,
                Product.stock,
                Product.minstock
            ).join(Category).join(Brand).filter(Product.stock <= Product.minstock).order_by(Product.descr).all()
            
            formatted_products = []
            for p in products:
                formatted_products.append((
                    str(p.idproducts),
                    p.descr,
                    p.category,
                    p.brand,
                    f"{p.sellprice:.2f}",
                    p.stock,
                    p.minstock
                ))
            return formatted_products
        except Exception:
            return None

class SalesDatabase:
    def __init__(self, route) -> None:
        self.route = route
        self.session: Session = db_config.get_session()
    
    def close(self):
        """Fecha a sessão do banco de dados"""
        if self.session:
            self.session.close()

    def register_sale(self, fulldataset):
        """Registra uma nova venda"""
        try:
            sale = Sale(
                idcustomer=fulldataset[0],
                date=fulldataset[1],
                total=fulldataset[2]
            )
            self.session.add(sale)
            self.session.commit()
            
            # Retorna o ID da venda criada
            return "success", sale.idsale
        except Exception as e:
            self.session.rollback()
            return None, str(e)

    def register_sold_products(self, fulldataset):
        """Registra produtos vendidos"""
        try:
            sold_product = SoldProduct(
                idsale=fulldataset[0],
                idproduct=fulldataset[1],
                quantity=fulldataset[2],
                unitprice=fulldataset[3],
                cost=fulldataset[4],
                total=fulldataset[5]
            )
            self.session.add(sold_product)
            self.session.commit()
            return "success"
        except Exception as e:
            self.session.rollback()
            return str(e)
        
    def select_all_sales(self):
        """Seleciona todas as vendas"""
        try:
            sales = self.session.query(
                Sale.idsale,
                Sale.idcustomer,
                Sale.date,
                Sale.total,
                Customer.name,
                Customer.cpf_cnpj
            ).join(Customer).order_by(desc(Sale.date)).all()
            
            # Formatar datas para compatibilidade
            formatted_sales = []
            for s in sales:
                formatted_sales.append((
                    s.idsale,
                    s.idcustomer,
                    s.date.strftime('%d/%m/%Y'),
                    s.total,
                    s.name,
                    s.cpf_cnpj
                ))
            return formatted_sales
        except Exception:
            return None

    def select_one_sale(self, idsale):
        """Seleciona uma venda por ID"""
        try:
            sale = self.session.query(
                Sale.idsale,
                Sale.idcustomer,
                Sale.date,
                Sale.total,
                Customer.name,
                Customer.cpf_cnpj
            ).join(Customer).filter(Sale.idsale == idsale).first()
            
            if sale:
                return (
                    sale.idsale,
                    sale.idcustomer,
                    sale.date.strftime('%d/%m/%Y'),
                    sale.total,
                    sale.name,
                    sale.cpf_cnpj
                )
            return None
        except Exception:
            return None

    def select_all_sold(self, idsale):
        """Seleciona produtos vendidos de uma venda"""
        try:
            sold_products = self.session.query(
                SoldProduct.idsoldproducts,
                SoldProduct.idproduct,
                Product.descr,
                Brand.brand,
                SoldProduct.quantity,
                SoldProduct.unitprice,
                SoldProduct.cost,
                SoldProduct.total
            ).join(Product).join(Brand).filter(SoldProduct.idsale == idsale).all()
            return sold_products
        except Exception:
            return None

    def update_sale(self, id_sale, data_sale):
        """Atualiza uma venda"""
        try:
            sale = self.session.query(Sale).filter(Sale.idsale == id_sale).first()
            if sale:
                sale.idcustomer = data_sale[0]
                sale.date = data_sale[1]
                sale.total = data_sale[2]
                self.session.commit()
                return "success"
            return "Sale not found"
        except Exception as e:
            self.session.rollback()
            return str(e)

    def delete_products_sold(self, id_sale):
        """Deleta produtos vendidos de uma venda"""
        try:
            self.session.query(SoldProduct).filter(SoldProduct.idsale == id_sale).delete()
            self.session.commit()
            return "success"
        except Exception as e:
            self.session.rollback()
            return str(e)

    def delete_sale(self, id_sale):
        """Deleta uma venda"""
        try:
            sale = self.session.query(Sale).filter(Sale.idsale == id_sale).first()
            if sale:
                self.session.delete(sale)  # Cascade vai deletar os produtos vendidos
                self.session.commit()
                return "success"
            return "Sale not found"
        except Exception as e:
            self.session.rollback()
            return str(e)
    
    def find_sale(self, text):
        """Busca vendas por texto"""
        try:
            pattern = f"%{text}%"
            sales = self.session.query(
                Sale.idsale,
                Sale.idcustomer,
                Sale.date,
                Sale.total,
                Customer.name,
                Customer.cpf_cnpj
            ).join(Customer).filter(
                or_(
                    Sale.idsale.like(pattern),
                    Sale.idcustomer.like(pattern),
                    Customer.name.like(pattern),
                    Customer.cpf_cnpj.like(pattern)
                )
            ).all()
            
            formatted_sales = []
            for s in sales:
                formatted_sales.append((
                    s.idsale,
                    s.idcustomer,
                    s.date.strftime('%d/%m/%Y'),
                    s.total,
                    s.name,
                    s.cpf_cnpj
                ))
            return formatted_sales
        except Exception as e:
            return str(e)
    
    def select_sales_history(self, id_customer):
        """Seleciona histórico de vendas de um cliente"""
        try:
            sales = self.session.query(
                Sale.idsale,
                Sale.date,
                Sale.total
            ).filter(Sale.idcustomer == id_customer).order_by(Sale.date).all()
            
            formatted_sales = []
            for s in sales:
                formatted_sales.append((
                    s.idsale,
                    s.date.strftime('%d/%m/%Y'),
                    s.total
                ))
            return formatted_sales
        except Exception:
            return None

    def select_sold_history(self, id_product):
        """Seleciona histórico de vendas de um produto"""
        try:
            sold_history = self.session.query(
                Sale.idsale,
                Sale.date,
                SoldProduct.total
            ).join(SoldProduct).filter(SoldProduct.idproduct == id_product).order_by(Sale.date).all()
            
            formatted_history = []
            for s in sold_history:
                formatted_history.append((
                    s.idsale,
                    s.date.strftime('%d/%m/%Y'),
                    s.total
                ))
            return formatted_history
        except Exception:
            return None

    def select_sales_from_previous_tirthy(self):
        """Seleciona vendas dos últimos 30 dias"""
        limit_date = date.today() - timedelta(days=30)
        try:
            sales = self.session.query(
                Sale.idsale,
                Sale.idcustomer,
                Sale.date,
                Sale.total,
                Customer.name,
                Customer.cpf_cnpj
            ).join(Customer).filter(Sale.date >= limit_date).order_by(desc(Sale.date)).all()
            
            formatted_sales = []
            for s in sales:
                formatted_sales.append((
                    s.idsale,
                    s.idcustomer,
                    s.date.strftime('%d/%m/%Y'),
                    s.total,
                    s.name,
                    s.cpf_cnpj
                ))
            return formatted_sales
        except Exception:
            return None
    
    def select_sales_from_previous_seven(self):
        """Seleciona vendas dos últimos 7 dias"""
        limit_date = date.today() - timedelta(days=7)
        try:
            sales = self.session.query(
                Sale.idsale,
                Sale.idcustomer,
                Sale.date,
                Sale.total,
                Customer.name,
                Customer.cpf_cnpj
            ).join(Customer).filter(Sale.date >= limit_date).order_by(desc(Sale.date)).all()
            
            formatted_sales = []
            for s in sales:
                formatted_sales.append((
                    s.idsale,
                    s.idcustomer,
                    s.date.strftime('%d/%m/%Y'),
                    s.total,
                    s.name,
                    s.cpf_cnpj
                ))
            return formatted_sales
        except Exception:
            return None
        
    def select_sales_from_today(self):
        """Seleciona vendas de hoje"""
        today = date.today()
        try:
            sales = self.session.query(
                Sale.idsale,
                Sale.idcustomer,
                Sale.date,
                Sale.total,
                Customer.name,
                Customer.cpf_cnpj
            ).join(Customer).filter(Sale.date >= today).order_by(desc(Sale.date)).all()
            
            formatted_sales = []
            for s in sales:
                formatted_sales.append((
                    s.idsale,
                    s.idcustomer,
                    s.date.strftime('%d/%m/%Y'),
                    s.total,
                    s.name,
                    s.cpf_cnpj
                ))
            return formatted_sales
        except Exception:
            return None

class DashboardDatabase:
    def __init__(self, route) -> None:
        self.route = route
        self.session: Session = db_config.get_session()

    def close(self):
        """Fecha a sessão do banco de dados"""
        if self.session:
            self.session.close()

    def select_percent_stock(self):
        """Calcula percentual de estoque"""
        try:
            result = self.session.query(
                func.sum(Product.stock) / func.sum(Product.maxstock) * 100
            ).scalar()
            return int(result) if result else 0
        except Exception:
            return 0

    def select_most_profitable(self):
        """Seleciona os 5 produtos mais lucrativos"""
        try:
            profitable = self.session.query(
                SoldProduct.idproduct,
                func.sum(SoldProduct.total - (SoldProduct.quantity * SoldProduct.cost)).label('profit'),
                Product.descr
            ).join(Product).group_by(SoldProduct.idproduct).order_by(desc('profit')).limit(5).all()
            return profitable
        except Exception:
            return None

    def select_sales_by_months(self, dates_data):
        """Seleciona vendas por meses"""
        try:
            final_result = []
            for dates in dates_data:
                result = self.session.query(func.sum(Sale.total)).filter(
                    and_(Sale.date >= dates[0], Sale.date <= dates[1])
                ).scalar()
                final_result.append(0 if result is None else round(result, 2))
            return final_result
        except Exception:
            return []

    def select_numb_of_customers(self):
        """Conta número de clientes"""
        today = date.today()
        first_day_of_month = date(today.year, today.month, 1)
        try:
            total_customers = self.session.query(func.count(Customer.idcustomers)).scalar()
            past_customers = self.session.query(func.count(Customer.idcustomers)).filter(
                Customer.date < first_day_of_month
            ).scalar()
            return total_customers, past_customers
        except Exception:
            return 0, 0

    def select_today_sales_billing(self):
        """Seleciona vendas e faturamento de hoje"""
        today = date.today()
        try:
            result = self.session.query(
                func.count(Sale.idsale),
                func.sum(Sale.total)
            ).filter(Sale.date == today).first()
            return result
        except Exception:
            return None
        
    def select_numb_of_products_and_stock(self):
        """Conta produtos e produtos com estoque baixo"""
        try:
            total_products = self.session.query(func.count(Product.idproducts)).scalar()
            low_stock = self.session.query(func.count(Product.idproducts)).filter(
                Product.stock <= Product.minstock
            ).scalar()
            return total_products, low_stock
        except Exception:
            return 0, 0