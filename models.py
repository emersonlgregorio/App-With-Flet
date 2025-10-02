from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    
    idUser = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(65), nullable=False)
    user = Column(String(20), nullable=False, unique=True)
    password = Column(String(80), nullable=False)
    date = Column(Date, nullable=False)
    acesso = Column(String(10), nullable=False)


class Customer(Base):
    __tablename__ = 'customers'
    
    idcustomers = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    cpf_cnpj = Column(String(18), nullable=False, unique=True)
    tel = Column(String(20))
    email = Column(String(45))
    observ = Column(String(100))
    date = Column(Date, nullable=False)
    
    # Relacionamento com endereços
    addresses = relationship("Address", back_populates="customer",
                           cascade="all, delete-orphan")
    # Relacionamento com vendas
    sales = relationship("Sale", back_populates="customer")


class Address(Base):
    __tablename__ = 'adress'
    
    idadress = Column(Integer, primary_key=True, autoincrement=True)
    cod_customer = Column(String(18), ForeignKey('customers.cpf_cnpj'),
                         nullable=False)
    ender = Column(String(150), nullable=False)
    cidade = Column(String(45))
    uf = Column(String(2))
    CEP = Column(String(9))
    
    # Relacionamento com cliente
    customer = relationship("Customer", back_populates="addresses")


class Category(Base):
    __tablename__ = 'category'
    
    idcategory = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(String(45), nullable=False, unique=True)
    
    # Relacionamento com produtos
    products = relationship("Product", back_populates="category")


class Brand(Base):
    __tablename__ = 'brand'
    
    idbrand = Column(Integer, primary_key=True, autoincrement=True)
    brand = Column(String(45), nullable=False, unique=True)
    
    # Relacionamento com produtos
    products = relationship("Product", back_populates="brand")


class Product(Base):
    __tablename__ = 'products'
    
    idproducts = Column(Integer, primary_key=True, autoincrement=True)
    descr = Column(String(50), nullable=False)
    idcategory = Column(Integer, ForeignKey('category.idcategory'),
                       nullable=False)
    idbrand = Column(Integer, ForeignKey('brand.idbrand'), nullable=False)
    stock = Column(Integer, nullable=False)
    minstock = Column(Integer, nullable=False)
    maxstock = Column(Integer, nullable=False)
    observ = Column(String(100))
    costs = Column(Float, nullable=False)
    sellprice = Column(Float, nullable=False)
    margin = Column(Float, nullable=False)
    
    # Relacionamentos
    category = relationship("Category", back_populates="products")
    brand = relationship("Brand", back_populates="products")
    sold_products = relationship("SoldProduct", back_populates="product")


class Sale(Base):
    __tablename__ = 'sales'
    
    idsale = Column(Integer, primary_key=True, autoincrement=True)
    idcustomer = Column(Integer, ForeignKey('customers.idcustomers'),
                       nullable=False)
    date = Column(Date, nullable=False)
    total = Column(Float, nullable=False)
    
    # Relacionamentos
    customer = relationship("Customer", back_populates="sales")
    sold_products = relationship("SoldProduct", back_populates="sale",
                               cascade="all, delete-orphan")


class SoldProduct(Base):
    __tablename__ = 'soldproducts'
    
    idsoldproducts = Column(Integer, primary_key=True, autoincrement=True)
    idsale = Column(Integer, ForeignKey('sales.idsale'), nullable=False)
    idproduct = Column(Integer, ForeignKey('products.idproducts'),
                      nullable=False)
    quantity = Column(Integer, nullable=False)
    unitprice = Column(Float, nullable=False)
    cost = Column(Float, nullable=False)
    total = Column(Float, nullable=False)
    
    # Relacionamentos
    sale = relationship("Sale", back_populates="sold_products")
    product = relationship("Product", back_populates="sold_products")
