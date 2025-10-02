from flet import (Container, Row, Column, Container, Text, TextField, IconButton, DataTable, DataRow,
                  DataColumn, DataCell, Switch, Icons, Colors, TextThemeStyle, TextAlign, Card, Divider, ListView)
from datetime import datetime
import asyncio

from Notification import Notification
from Validator import Validator
from Database import ProductsDatabase
from Database import SalesDatabase
from SelectCustomer import SelectCustomer
from SelectProduct import SelectProduct

class RegisterSales(Container):
    def __init__(self, route):
        super().__init__()
        self.route = route
        self.sale_list_to_register = []
        self.products_list_to_register = []
        self.products_in_table = []
        self.list_to_update_stock = []

        self.text_description = Text("Busque um Produto...", expand=True, style=TextThemeStyle.DISPLAY_SMALL)
        self.tf_stock = TextField(expand=1, label="Estoque:", border='none', value="...", text_size=20, read_only=True)
        self.tf_brand = TextField(expand=1, label="Marca:", border='none', value="...", text_size=20, read_only=True)
        self.tf_quantity = TextField(expand=1, label="Quantidade:", border='none', value="2", text_size=20, read_only=True)
        self.tf_unit_price = TextField(expand=1, label="Preço Unitário:", border='none', value="1.500,00", prefix_text="R$", text_size=20, read_only=True)
        self.tf_total_price = TextField(expand=1, label="Valor Total:", border='none', value="3.000,00", prefix_text="R$", text_size=20, read_only=True)
        self.tf_margin = TextField(expand=1, label="Margem(%):", border='none', value="60,50", text_size=20, read_only=True)
        self.btn_back = IconButton(icon=Icons.ARROW_BACK_OUTLINED, icon_size=32, tooltip='Voltar para "Vendas"', on_click=self.back_clicked)

        self.btn_find_by_descr = IconButton(icon=Icons.SEARCH_ROUNDED, icon_size=32, tooltip="Pesquisar Produtos", on_click=self.find_by_descr)
        self.sw_find = Switch(height=10, tooltip="Pesquisar por descrição")
        self.tf_find_product = TextField(prefix=self.sw_find, label="Buscar...", expand=4, dense=True, on_change=self.find_product)
        self.tf_quantity2 = TextField(label="Quantidade", expand=1, prefix_icon=Icons.NUMBERS, text_align=TextAlign.CENTER, dense=True, on_change=self.validate_fields)
        self.tf_discount = TextField(label="Desconto", expand=1, prefix_icon=Icons.REMOVE_CIRCLE_OUTLINE_OUTLINED, dense=True, suffix_text="%", text_align=TextAlign.CENTER, on_change=self.validate_fields)
        self.btn_include = IconButton(icon=Icons.ADD_CIRCLE_OUTLINE_OUTLINED, tooltip="Incluir", icon_size=36, on_click=self.include_clicked)

        self.tf_id_sale = TextField(border="none", expand=3, label="Pedido nº:", value="Automático", text_size=16, read_only=True)
        self.tf_customer = TextField(border="none", expand=9, label="Cliente:", multiline=True, text_size=16, read_only=True)
        self.tf_CPF = TextField(border="none", expand=4, label="CPF:", text_size=16, read_only=True)
        self.tf_date = TextField(border="none", expand=3, label="Data:", text_size=16, read_only=True)
        self.tf_total_sale = TextField(border="none", expand=3, label="Total:", text_size=16, prefix_text="R$", read_only=True)
        self.btn_select_customer = IconButton(icon=Icons.SENSOR_OCCUPIED_OUTLINED, tooltip="Selecionar Cliente", on_click=lambda e: asyncio.run(self.select_customer_clicked(e)))
        self.btn_clear_sale = IconButton(icon=Icons.CLEANING_SERVICES_OUTLINED, tooltip="Limpar Campos", on_click=self.clear_sale_clicked)
        self.btn_close_sale = IconButton(icon=Icons.SHOPPING_CART_CHECKOUT_OUTLINED, tooltip="Salvar Venda", icon_color="primary", icon_size=36, on_click=self.register_or_update_clicked)
        self.dt_products_sold = DataTable(                                            
            expand=True,
            column_spacing=5,
            divider_thickness=0.4,
            #heading_row_color=Colors.ON_INVERSE_SURFACE,
            columns=[
                DataColumn(Text('ID')), 
                DataColumn(Text('CÓD. PR.')), 
                DataColumn(Text('DESCRIÇÃO')), 
                DataColumn(Text('MARCA')),
                DataColumn(Text('QUANT.')),
                DataColumn(Text('V. UNIT.')),
                DataColumn(Text('CUSTO')),
                DataColumn(Text('V. TOTAL')),
                DataColumn(Text("EXCLUIR"))
            ],
            rows=[
                DataRow(
                    cells=[
                        DataCell(Text('00001')),
                        DataCell(Text("00001")),
                        DataCell(Text("DESCRIÇÃO COMPLETA DO PRODUTO TAL")),
                        DataCell(Text("MULTILASER")),
                        DataCell(Text("02")),
                        DataCell(TextField(border="none", prefix_text="R$", value="115,50", read_only=True)),
                        DataCell(TextField(border="none", prefix_text="R$", value="100,00", read_only=True)),
                        DataCell(TextField(border="none", prefix_text="R$", value="331,00", read_only=True)),
                        DataCell(Row([IconButton(icon=Icons.DELETE_OUTLINED, icon_color='red', tooltip="Excluir Produto")])),
                    ],
                ),
            ],
        )

    def build(self):
        page_content = Container(
            #bgcolor='red',
            padding=5,
            border_radius=5,
            expand=True,
            content=Column(
                expand=True,
                controls=[
                    Row(
                        #expand=2,
                        controls=[
                            Column(
                                expand=True,
                                controls=[
                                    Row(
                                        controls=[
                                            Card(
                                                expand=True,
                                                surface_tint_color=Colors.INVERSE_PRIMARY,
                                                elevation = 1.5,
                                                content=Container(
                                                    padding=10,
                                                    content=Column(
                                                        controls=[
                                                            Row(
                                                                controls=[
                                                                    self.text_description,
                                                                    self.btn_back,
                                                                ]
                                                            ),
                                                            Row(
                                                                controls=[
                                                                    self.tf_stock,
                                                                    self.tf_brand,
                                                                    self.tf_quantity,
                                                                    self.tf_unit_price,
                                                                    self.tf_total_price,
                                                                    self.tf_margin,
                                                                ]
                                                            ),
                                                        ]
                                                    )
                                                )
                                            )
                                        ]
                                    ),
                                    Row(
                                        controls=[
                                            self.btn_find_by_descr,
                                            self.tf_find_product,
                                            self.tf_quantity2,
                                            self.tf_discount,
                                            self.btn_include,
                                        ]
                                    ),
                                ]
                            )
                        ]
                    ),
                    Divider(height=1),
                    Row(
                        expand=3,
                        controls=[
                            Column(
                                expand=True,
                                controls=[
                                    Row(
                                        controls=[
                                            self.tf_id_sale,
                                            self.tf_customer,
                                            self.tf_CPF,
                                            self.tf_date,
                                            self.tf_total_sale,
                                            self.btn_select_customer,
                                            self.btn_clear_sale,
                                            self.btn_close_sale,
                                        ]
                                    ),
                                    Divider(height=1),
                                    ListView(
                                        expand=True,
                                        controls=[
                                            self.dt_products_sold,
                                        ]
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )
        )

        content = Row(
            expand=True,
            spacing=10,
            controls=[
                page_content,
            ]
        )
        
        # Configurar o Container diretamente
        self.content = content
    def initialize(self):
        print("Initializing Register Sales Page")
        
        try:
            self.clear_card()

            for lists in [self.products_in_table, self.sale_list_to_register, self.products_list_to_register, self.list_to_update_stock]:
                lists.clear()

            for control in [self.text_description, self.tf_stock, self.tf_brand, self.tf_find_product, self.tf_customer,
            self.tf_CPF, self.tf_date, self.tf_total_sale, self.tf_quantity2, self.tf_discount]:
                control.value = ""
            
            self.route.bar.set_title("Nova Venda")
            self.tf_id_sale.value = "Automático"
            self.text_description.data = ""
            self.tf_customer.data = ""
            self.btn_close_sale.disabled = True
            self.dt_products_sold.rows.clear()
            
            # Atualizar a página corretamente
            if hasattr(self.route, 'page') and self.route.page:
                self.route.page.update()
                
        except Exception as ex:
            print(f"❌ ERRO em initialize: {ex}")
            import traceback
            traceback.print_exc()
            # Tentar atualizar a página mesmo em caso de erro
            if hasattr(self.route, 'page') and self.route.page:
                self.route.page.update()

    def load_data_for_update(self):
        print("Initializing Editor Sales Page")
        self.tf_CPF.value = self.sale_list_to_register.pop()
        self.tf_customer.value = self.sale_list_to_register.pop()
        self.tf_id_sale.value = self.sale_list_to_register.pop(0)
        self.tf_customer.data = self.sale_list_to_register[0]
        self.tf_date.value = self.sale_list_to_register[1]
        date_object = datetime.strptime(self.tf_date.value, "%d/%m/%Y")
        formatted_date = datetime.strftime(date_object, "%Y%m%d")
        self.sale_list_to_register[1] = formatted_date
        self.tf_total_sale.value = Validator.format_to_currency(self.sale_list_to_register[2])
        self.update()
        
        self.fill_in_product_table(self.products_in_table)
        self.list_to_update_stock = []

    def back_clicked(self, _):
        try:
            self.route.page.go("/sales")
            self.route.bar.set_title("Vendas")
            self.route.page.update()
        except Exception as ex:
            print(f"❌ ERRO em back_clicked: {ex}")
            import traceback
            traceback.print_exc()

    async def select_customer_clicked(self, e):
        dialog = SelectCustomer(self.route)
        self.route.page.open(dialog)
        asyncio.create_task(dialog.verify_data())
        await dialog.verify_data()
        if dialog.data == "back":
            return
        if self.tf_id_sale.value == "Automático":
            self.fill_in_customer_to_register(e, dialog.data)
        else:
            self.fill_in_customer_to_update(e, dialog.data)
               
    def fill_in_customer_to_register(self, e, data):
        self.tf_customer.data = data[0]
        self.tf_customer.value = data[1]
        self.tf_CPF.value = data[2]
        today = datetime.now()
        self.tf_date.value = today.strftime("%d/%m/%Y")
        
        self.sale_list_to_register = [
            data[0],
            today.strftime("%Y-%m-%d"),
            0.00,
        ]
        self.update_total()

        # Verificar se o controle está na página antes de atualizar
        if hasattr(self.route, 'page') and self.route.page is not None:
            self.route.page.update()
        self.validate_fields(e)

    def fill_in_customer_to_update(self, e, data):
        self.tf_customer.data = data[0]
        self.tf_customer.value = data[1]
        self.tf_CPF.value = data[2]
        
        self.sale_list_to_register[0] = data[0]

        self.update()
        self.validate_fields(e)

    def clear_sale_clicked(self, _):
        self.initialize()

    def clear_card(self):
        try:
            for control in [self.text_description, self.tf_stock, self.tf_brand, self.tf_quantity, self.tf_quantity2,
                            self.tf_unit_price, self.tf_total_price, self.tf_margin, self.tf_discount]:
                control.value = ""
                control.data = ""
            
            self.btn_include.disabled = True
            self.tf_find_product.focus()
            
            # Atualizar a página corretamente
            if hasattr(self.route, 'page') and self.route.page:
                self.route.page.update()
                
        except Exception as ex:
            print(f"❌ ERRO em clear_card: {ex}")
            import traceback
            traceback.print_exc()

    def load_card(self, data):
        try:
            self.text_description.data = data[0] # product_id
            self.text_description.value = data[1]
            self.tf_brand.data = data[3] # brand_id
            self.tf_unit_price.value = Validator.format_to_currency(float(data[4]))
            self.tf_unit_price.data = Validator.format_to_currency(data[4]) # unit_price
            self.tf_margin.data = Validator.format_to_currency(data[5]) # costs
            self.tf_stock.value = str(data[6])
            self.tf_brand.value = data[7]
            
            # Atualizar a página corretamente
            if hasattr(self.route, 'page') and self.route.page:
                self.route.page.update()
                
        except Exception as ex:
            print(f"❌ ERRO em load_card: {ex}")
            import traceback
            traceback.print_exc()

    def find_product(self, e):
        print("🔍 ===== FIND_PRODUCT CHAMADO =====")
        print(f"🔍 Valor digitado: '{self.tf_find_product.value}'")
        
        if self.tf_find_product.value == "":
            print("🔍 Campo vazio, limpando card")
            self.clear_card()
            return

        try:
            mydb = ProductsDatabase(self.route)
            print(f"🔍 Switch de busca por descrição: {self.sw_find.value}")
            
            if self.sw_find.value:
                print("🔍 Buscando por descrição")
                result = mydb.find_product_by_description(self.tf_find_product.value)
            else:
                print("🔍 Buscando por código")
                code = Validator.format_to_int(self.tf_find_product.value)
                print(f"🔍 Código formatado: {code} (tipo: {type(code)})")
                
                if isinstance(code, int):
                    result = mydb.find_product_by_code(code)
                    print(f"🔍 Resultado da busca por código: {result}")
                else:
                    print("🔍 Código inválido, resultado = None")
                    result = None
            
            mydb.close()
            
            if result:
                print(f"🔍 Produto encontrado: {result}")
                self.load_card(result)
            else:
                print("🔍 Nenhum produto encontrado, limpando card")
                self.clear_card()
                
            print("🔍 Chamando validate_fields")
            self.validate_fields(e)
            print("🔍 validate_fields concluído")
            
            # Atualizar a página corretamente
            if hasattr(self.route, 'page') and self.route.page:
                self.route.page.update()
            
        except Exception as ex:
            print(f"❌ ERRO em find_product: {ex}")
            print(f"❌ Tipo do erro: {type(ex)}")
            import traceback
            traceback.print_exc()
            self.clear_card()
            # Garantir que a página seja atualizada mesmo em caso de erro
            if hasattr(self.route, 'page') and self.route.page:
                self.route.page.update()

    def is_customer_selected(self):
        try:
            if self.tf_customer.data == "":
                self.btn_include.disabled = True
                self.tf_customer.value = "Selecione um Cliente!"
                Notification(self.route.page, "Selecione um Cliente!", "blue").show_message()
                
                # Atualizar a página corretamente
                if hasattr(self.route, 'page') and self.route.page:
                    self.route.page.update()
                return False
            return True
        except Exception as ex:
            print(f"❌ ERRO em is_customer_selected: {ex}")
            import traceback
            traceback.print_exc()
            return False

    def is_product_selected(self, unit_price):
        try:
            if not isinstance(unit_price, float):
                if self.tf_find_product.value == "":
                    Notification(self.route.page, "Busque por um produto!", "blue").show_message()
                    self.text_description.value = "Busque um Produto..."
                self.btn_include.disabled = True
                
                # Atualizar a página corretamente
                if hasattr(self.route, 'page') and self.route.page:
                    self.route.page.update()
                return False
            return True
        except Exception as ex:
            print(f"❌ ERRO em is_product_selected: {ex}")
            import traceback
            traceback.print_exc()
            return False

    def get_quantity_if_its_valid(self, quantity):
        try:
            if self.tf_quantity2.value == "":
                self.tf_quantity2.error_text = ""
                self.clear_calcs()
                return None
            MIN_QUANTITY = 1
            final_quantity = Validator.format_to_int(quantity)
            if (not isinstance(final_quantity, int) or final_quantity < MIN_QUANTITY):
                self.btn_include.disabled = True
                self.tf_quantity2.error_text = "Valor Inválido!"
                
                # Atualizar a página corretamente
                if hasattr(self.route, 'page') and self.route.page:
                    self.route.page.update()
                return None
            return final_quantity
        except Exception as ex:
            print(f"❌ ERRO em get_quantity_if_its_valid: {ex}")
            import traceback
            traceback.print_exc()
            return None

    def get_discount_if_its_valid(self, discount):
        try:
            if self.tf_discount.value == "":
                return 0.0
            else:
                final_discount = Validator.format_to_float(discount)
                if (not isinstance(final_discount, float) or final_discount < 0):
                    self.btn_include.disabled = True
                    self.tf_discount.error_text = "Valor Inválido!"
                    
                    # Atualizar a página corretamente
                    if hasattr(self.route, 'page') and self.route.page:
                        self.route.page.update()
                    return None
                return final_discount
        except Exception as ex:
            print(f"❌ ERRO em get_discount_if_its_valid: {ex}")
            import traceback
            traceback.print_exc()
            return None

    def is_stock_available(self, id):
        try:
            # for data in self.dt_products_sold.rows:
            #     for col, text in enumerate(data.cells):
            #         print(text.content.value) if col < 8 else None
            quantity = 0
            for row in range(len(self.dt_products_sold.rows)):
                if self.dt_products_sold.rows[row].cells[1].content.value == id:
                    quantity += int(self.dt_products_sold.rows[row].cells[4].content.value)

            quantity += int(self.tf_quantity2.value)
            if quantity > int(self.tf_stock.value):
                self.btn_include.disabled = True
                Notification(self.route.page, "Não há estoque suficiente para incluir o produto. Verifique a quantidade em estoque e os produtos já inclusos!", "red").show_message()
                
                # Atualizar a página corretamente
                if hasattr(self.route, 'page') and self.route.page:
                    self.route.page.update()
                return False
            return True
        except Exception as ex:
            print(f"❌ ERRO em is_stock_available: {ex}")
            import traceback
            traceback.print_exc()
            return False

    def validate_fields(self, _):
        try:
            if not self.is_customer_selected():
                return        

            unit_price = Validator.format_to_float(self.tf_unit_price.data)
            if not self.is_product_selected(unit_price):
                return
            
            quantity = self.get_quantity_if_its_valid(self.tf_quantity2.value)
            if quantity is None:
                return
            
            discount = self.get_discount_if_its_valid(self.tf_discount.value)
            if discount is None:
                return

            if not self.is_stock_available(str(self.text_description.data)):
                return
            
            costs = Validator.format_to_float(self.tf_margin.data)

            self.tf_quantity2.error_text = ""
            self.tf_discount.error_text = ""
            self.btn_include.disabled = False
            
            # Atualizar a página corretamente
            if hasattr(self.route, 'page') and self.route.page:
                self.route.page.update()
                
            self.calculate_fields(quantity, unit_price, discount, costs)
            
        except Exception as ex:
            print(f"❌ ERRO em validate_fields: {ex}")
            import traceback
            traceback.print_exc()

    def clear_calcs(self):
        try:
            self.tf_quantity.value = ""
            self.tf_total_price.value = ""
            self.margin = ""
            self.btn_include.disabled = True
            
            # Atualizar a página corretamente
            if hasattr(self.route, 'page') and self.route.page:
                self.route.page.update()
                
        except Exception as ex:
            print(f"❌ ERRO em clear_calcs: {ex}")
            import traceback
            traceback.print_exc()

    def calculate_fields(self, quantity, unit_price, discount, costs):
        try:
            unit_price = unit_price - (unit_price * discount / 100)
            margin = (unit_price - costs) / costs * 100 if costs > 0 else 100.00
            total_price = quantity * unit_price
            
            self.tf_quantity.value = str(quantity)
            self.tf_unit_price.value = Validator.format_to_currency(unit_price)
            self.tf_total_price.value = Validator.format_to_currency(total_price)
            self.tf_margin.value = "{:.2f}".format(margin)
            
            # Atualizar a página corretamente
            if hasattr(self.route, 'page') and self.route.page:
                self.route.page.update()
                
        except Exception as ex:
            print(f"❌ ERRO em calculate_fields: {ex}")
            import traceback
            traceback.print_exc()
        
    def include_clicked(self, _):
        print("🔍 Botão Incluir clicado!")
        print(f"🔍 text_description.data: {self.text_description.data}")
        print(f"🔍 text_description.value: {self.text_description.value}")
        print(f"🔍 tf_brand.value: {self.tf_brand.value}")
        print(f"🔍 tf_quantity.value: {self.tf_quantity.value}")
        print(f"🔍 tf_unit_price.value: {self.tf_unit_price.value}")
        print(f"🔍 tf_margin.data: {self.tf_margin.data}")
        print(f"🔍 tf_total_price.value: {self.tf_total_price.value}")
        
        data = [
            "Aut.",
            str(self.text_description.data), # id product
            self.text_description.value, # product description
            self.tf_brand.value,
            self.tf_quantity.value,
            Validator.format_to_float(self.tf_unit_price.value),
            Validator.format_to_float(self.tf_margin.data), # costs
            Validator.format_to_float(self.tf_total_price.value),
        ]
        print(f"🔍 Data a ser incluída: {data}")
        self.products_in_table.append(data)
        self.fill_in_product_table(self.products_in_table)
        self.tf_find_product.value = ""
        self.clear_card()
        print("🔍 Produto incluído com sucesso!")

    def fill_in_product_table(self, fulldata):
        try:
            self.dt_products_sold.rows.clear()
            for row, data in enumerate(fulldata):
                self.dt_products_sold.rows.append(
                    DataRow(
                        cells=[
                            DataCell(Text(data[0])),
                            DataCell(Text(data[1])),
                            DataCell(Text(data[2])),
                            DataCell(Text(data[3])),
                            DataCell(Text(data[4])),
                            DataCell(TextField(border="none", prefix_text="R$", value=Validator.format_to_currency(data[5]), read_only=True)),
                            DataCell(TextField(border="none", prefix_text="R$", value=Validator.format_to_currency(data[6]), read_only=True)),
                            DataCell(TextField(border="none", prefix_text="R$", value=Validator.format_to_currency(data[7]), read_only=True)),
                            DataCell(IconButton(icon=Icons.DELETE_OUTLINED, icon_color='red', data=row, on_click=self.delete_product))
                        ]
                    )
                )
            self.dt_products_sold.update()
            self.update_total()
        except Exception as ex:
            print(f"❌ ERRO em fill_in_product_table: {ex}")
            import traceback
            traceback.print_exc()

    def update_total(self):
        try:
            if len(self.products_in_table) == 0:
                self.tf_total_sale.value = "0,00"
                self.btn_close_sale.disabled = True
                if hasattr(self.route, 'page') and self.route.page:
                    self.route.page.update()
                return
            total = 0.0
            for data in self.products_in_table:
                total += data[7]
            self.tf_total_sale.value = Validator.format_to_currency(total)
            self.btn_close_sale.disabled = False
            if hasattr(self.route, 'page') and self.route.page:
                self.route.page.update()
            self.sale_list_to_register[2] = total
        except Exception as ex:
            print(f"❌ ERRO em update_total: {ex}")
            import traceback
            traceback.print_exc()

    def delete_product(self, e):
        try:
            if self.dt_products_sold.rows[e.control.data].cells[0].content.value != "Aut.":
                self.list_to_update_stock.append([self.products_in_table[e.control.data][1], self.products_in_table[e.control.data][4]])

            if len(self.products_in_table) > 0:
                del self.products_in_table[e.control.data]
                self.update_total()
                self.fill_in_product_table(self.products_in_table)
        except Exception as ex:
            print(f"❌ ERRO em delete_product: {ex}")
            import traceback
            traceback.print_exc()
        
    def register_or_update_clicked(self, _):
        print("🔍 ===== REGISTER_OR_UPDATE_CLICKED =====")
        print(f"🔍 Número de produtos na tabela: {len(self.dt_products_sold.rows)}")
        print(f"🔍 ID da venda: {self.tf_id_sale.value}")
        
        self.products_list_to_register = []
        for row in range(len(self.dt_products_sold.rows)):
            print(f"🔍 Processando linha {row}:")
            print(f"🔍   - Célula 0 (Aut.): {self.dt_products_sold.rows[row].cells[0].content.value}")
            print(f"🔍   - Célula 1 (ID): {self.dt_products_sold.rows[row].cells[1].content.value}")
            print(f"🔍   - Célula 4 (Qtd): {self.dt_products_sold.rows[row].cells[4].content.value}")
            print(f"🔍   - Célula 5 (Preço): {self.dt_products_sold.rows[row].cells[5].content.value}")
            
            data = [
                Validator.format_to_int(self.dt_products_sold.rows[row].cells[1].content.value),
                Validator.format_to_int(self.dt_products_sold.rows[row].cells[4].content.value),
                Validator.format_to_float(self.dt_products_sold.rows[row].cells[5].content.value),
                Validator.format_to_float(self.dt_products_sold.rows[row].cells[6].content.value),
                Validator.format_to_float(self.dt_products_sold.rows[row].cells[7].content.value),
            ]
            print(f"🔍   - Data processada: {data}")
            self.products_list_to_register.append(data)
            if self.dt_products_sold.rows[row].cells[0].content.value == "Aut.":
                self.list_to_update_stock.append([data[0], - data[1]])

        print(f"🔍 Lista de produtos para registrar: {self.products_list_to_register}")
        print(f"🔍 Lista de vendas: {self.sale_list_to_register}")

        if self.tf_id_sale.value == "Automático":
            print("🔍 Registrando nova venda...")
            self.register_sale(self.sale_list_to_register, self.products_list_to_register)
            self.update_stock(self.list_to_update_stock)
        else:
            print("🔍 Atualizando venda existente...")
            self.update_sale(int(self.tf_id_sale.value), self.sale_list_to_register, self.products_list_to_register)
            return

        print("🔍 Chamando initialize()...")
        self.initialize()
        print("🔍 initialize() concluído")

    def register_sale(self, sale_data, products_data):
        print(f"🔍 register_sale chamado com sale_data: {sale_data}")
        print(f"🔍 register_sale chamado com products_data: {products_data}")
        
        mydb = SalesDatabase(self.route)
        result, id_or_error = mydb.register_sale(sale_data)
        mydb.close()
        
        print(f"🔍 Resultado do register_sale: result={result}, id_or_error={id_or_error}")
        
        if result is None:
            print(f"❌ ERRO no register_sale: {id_or_error}")
            Notification(self.route.page, f"Erro: {id_or_error}", "red").show_message()
            return
        
        print(f"🔍 Venda registrada com sucesso! ID: {id_or_error}")
        self.register_sold_products(id_or_error, products_data)

    def register_sold_products(self, sale_id, products_data):
        result = []
        mydb = SalesDatabase(self.route)
        for fulldataset in products_data:
            fulldataset.insert(0, sale_id)
            result.append(mydb.register_sold_products(fulldataset))
        mydb.close()

        if len(products_data) == len(result):
            Notification(self.route.page, "Pedido cadastrado/atualizado com sucesso", "green").show_message()
            return
        Notification(self.route.page, f"Erro ao cadastrar/atualizar o pedido: {result[-1]}", "red").show_message()
        
    def update_sale(self, id_sale, sale_data, products_data):
        mydb = SalesDatabase(self.route)
        result = mydb.update_sale(id_sale, sale_data)
        
        if result == "success":
            del_result = mydb.delete_products_sold(id_sale)
            mydb.close()
        else:
            Notification(self.route.page, f"Erro ao atualizar a venda: {result}", "red").show_message()
            mydb.close()
            return

        if del_result == "success":
            self.register_sold_products(id_sale, products_data)
        else:
            Notification(self.route.page, f"Erro ao atualizar a venda (exclusão dos produtos vendidos): {del_result}", "red").show_message()
            return
        
        if len(self.list_to_update_stock) > 0:
            self.update_stock(self.list_to_update_stock)

        self.route.page.go("/sales")
        self.route.bar.set_title("Vendas")
        self.route.page.update()
        
    def update_stock(self, data):
        mydb = ProductsDatabase(self.route)
        result = []
        for temp_data in data:
            result.append(mydb.update_stock(temp_data))
        mydb.close()

        if len(result) == len(data):
            Notification(self.route.page, f"Pedido salvo com sucesso. {len(data)} produto(s) atualizado(s) no estoque!", "green").show_message()
        else:
            Notification(self.route.page, f"Erro ao atualizar o estoque : {result[-1]}", "red").show_message()

        self.list_to_update_stock = []

    def find_by_descr(self, e):
        dialog = SelectProduct(self.route)
        self.route.page.open(dialog)
    
