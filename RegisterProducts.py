from flet import (Container, Row, Column, Text, TextField, IconButton, DataTable,
                  Dropdown, OutlinedButton, DataRow, DataColumn, DataCell, Icons,
                  Colors, TextThemeStyle, TextAlign, CrossAxisAlignment,
                  VerticalDivider, ListView, MainAxisAlignment, dropdown)

from Notification import Notification
from CategoryBrand import Category, Brand
from Database import ProductsDatabase, SalesDatabase
from Validator import Validator

class RegisterProducts(Container):
    def __init__(self, route):
        super().__init__()
        self.route = route

        self.text_label = Text(value="Novo Produto:", style=TextThemeStyle.TITLE_LARGE)
        self.tf_id = TextField(label="ID (Aut)", read_only=True, dense=True, expand=1, text_size=24)
        self.tf_descr = TextField(label="Descrição", expand=4, text_size=24, dense=True, on_change=self.analyze_fields)
        self.dp_category = Dropdown(label="Categoria", expand=2, on_change=self.analyze_fields)
        self.btn_manage_categories = IconButton(icon=Icons.ADD_CIRCLE_OUTLINE, icon_color=Colors.PRIMARY, icon_size=32, on_click=self.manage_categories_clicked)
        self.dp_brand = Dropdown(label="Marca", expand=2, on_change=self.analyze_fields)
        self.btn_manage_brands = IconButton(icon=Icons.ADD_CIRCLE_OUTLINE, icon_color=Colors.PRIMARY, icon_size=32, on_click=self.manage_brands_clicked)
        self.tf_stock = TextField(label="Estoque", expand=1, text_align=TextAlign.CENTER, on_change=self.analyze_fields)
        self.tf_min_stock = TextField(label="Est. Mínimo", expand=1, text_align=TextAlign.CENTER, on_change=self.analyze_fields)
        self.tf_max_stock = TextField(label="Est. Máximo", expand=1, text_align=TextAlign.CENTER, on_change=self.analyze_fields)
        self.tf_observ = TextField(label="Observação", expand=3, on_change=self.analyze_fields)
        self.tf_costs = TextField(label="Custo", expand=2, prefix_text="R$", text_size=24, dense=True,  on_change=self.analyze_fields, on_blur=self.calc_margin)
        self.tf_selling_price = TextField(label="Preço de Venda", expand=2, prefix_text="R$", text_size=24, dense=True,  on_change=self.analyze_fields, on_blur=self.calc_margin)
        self.tf_margin = TextField(label="Margem", expand=1, suffix_text="%", text_align=TextAlign.RIGHT, text_size=24, dense=True,  on_change=self.analyze_fields, on_blur=self.calc_selling_price)
        self.btn_save_exit = OutlinedButton(
            text='Salvar e Sair', icon=Icons.SAVE_OUTLINED,
            on_click=self.save_exit_clicked, disabled=True)
        self.btn_save_view = OutlinedButton(
            text='Salvar e Visualizar', icon=Icons.VISIBILITY_OUTLINED,
            on_click=self.save_view_clicked, disabled=True)
        self.btn_save_new = OutlinedButton(
            text='Salvar e Novo', icon=Icons.ADD_OUTLINED,
            on_click=self.save_new_clicked, disabled=True)
        self.btn_back = IconButton(tooltip='Voltar para "Produtos"', icon=Icons.ARROW_BACK_OUTLINED, icon_size=32, on_click=self.back_clicked)

        self.dt_order_history = DataTable(
            column_spacing=15,
            divider_thickness=0.4,
            # heading_row_color=Colors.ON_INVERSE_SURFACE,
            expand=True,
            columns=[
                DataColumn(Text('Pedido')),
                DataColumn(Text('Data')),
                DataColumn(Text('Valor')),
                DataColumn(Text('Ver')),
            ],
        )

        self.text_total = Text(value="R$ 350,00", style=TextThemeStyle.TITLE_MEDIUM)

    def build(self):
        page_content = Container(
            # bgcolor='red',
            padding=0,
            border_radius=5,
            expand=True,
            content=Column(
                controls=[
                    # Corpo principal
                    Container(
                        # bgcolor='white',
                        expand=True,
                        content=Row(
                            vertical_alignment=CrossAxisAlignment.START,
                            controls=[
                                Container(
                                    # bgcolor='red',
                                    expand=5,
                                    border_radius=5,
                                    padding=15,
                                    content=Column(
                                        expand=True,
                                        horizontal_alignment=CrossAxisAlignment.CENTER,
                                        controls=[
                                            Row(
                                                controls=[
                                                    self.text_label,
                                                    Row(expand=True),  # spacer
                                                    self.btn_back,
                                                ]
                                            ),
                                            Row(
                                                controls=[
                                                    self.tf_id,
                                                    self.tf_descr,
                                                ]
                                            ),
                                            Row(
                                                controls=[
                                                    self.dp_category,
                                                    self.btn_manage_categories,
                                                    Column(),
                                                    self.dp_brand,
                                                    self.btn_manage_brands,
                                                ]
                                            ),
                                            Row(
                                                controls=[
                                                    Text(value="Estoque:", style=TextThemeStyle.TITLE_LARGE),
                                                ]
                                            ),
                                            Row(
                                                controls=[
                                                    self.tf_stock,
                                                    self.tf_min_stock,
                                                    self.tf_max_stock,
                                                    self.tf_observ,
                                                ]
                                            ),
                                            Row(
                                                controls=[
                                                    Text(value="Preços:", style=TextThemeStyle.TITLE_LARGE),
                                                ]
                                            ),
                                            Row(
                                                controls=[
                                                    self.tf_costs,
                                                    self.tf_selling_price,
                                                    self.tf_margin,
                                                ]
                                            ),
                                            Column(expand=True),
                                            Row(
                                                alignment=MainAxisAlignment.END,
                                                spacing=10,
                                                controls=[
                                                    self.btn_save_exit,
                                                    self.btn_save_view,
                                                    self.btn_save_new,
                                                ]
                                            ),
                                        ]
                                    )
                                ),
                                VerticalDivider(width=1),
                                Container(
                                    # bgcolor='red',
                                    expand=2,
                                    border_radius=5,
                                    padding=15,
                                    content=Column(
                                        alignment=MainAxisAlignment.START,
                                        horizontal_alignment=CrossAxisAlignment.CENTER,
                                        spacing=20,
                                        controls=[
                                            Text(value="Histórico de Vendas", style=TextThemeStyle.TITLE_MEDIUM),
                                            ListView(
                                                expand=True,
                                                controls=[
                                                    self.dt_order_history,
                                                ]
                                            ),
                                            Row(
                                                alignment=MainAxisAlignment.END,
                                                controls=[
                                                    Text('Total:', style=TextThemeStyle.TITLE_MEDIUM),
                                                    self.text_total,
                                                ]
                                            )
                                        ]
                                    )
                                )
                            ]
                        )
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
        print("🔍 Initializing Register Products Page")
        print(f"🔍 Estado atual dos campos antes de limpar:")
        print(f"  - tf_id.value: {self.tf_id.value}")
        print(f"  - tf_descr.value: {self.tf_descr.value}")
        print(f"  - dp_category.value: {self.dp_category.value}")
        print(f"  - dp_brand.value: {self.dp_brand.value}")
        
        self.load_categories()
        self.load_brands()
        
        # Verificar se é um novo produto ou edição
        if hasattr(self, 'is_new_product') and self.is_new_product:
            print("🔍 Modo novo produto - limpando campos")
            self.clear_fields()
            self.text_label.value = "Novo Produto:"
            self.is_new_product = False  # Reset da flag
        elif self.tf_id.value and self.tf_id.value != "":
            print("🔍 Modo edição - mantendo dados carregados")
            self.text_label.value = "Editar Produto:"
        else:
            print("🔍 Modo novo produto (sem dados) - limpando campos")
            self.clear_fields()
            self.text_label.value = "Novo Produto:"
        
        self.update()
        
        print(f"🔍 Estado dos campos após initialize:")
        print(f"  - tf_id.value: {self.tf_id.value}")
        print(f"  - tf_descr.value: {self.tf_descr.value}")
        print(f"  - dp_category.value: {self.dp_category.value}")
        print(f"  - dp_brand.value: {self.dp_brand.value}")

    def back_clicked(self, e):
        self.route.page.go("/products")
        self.route.bar.set_title("Produtos")
        self.route.page.update()

    def manage_categories_clicked(self, e):
        dialog = Category(self)
        self.route.page.open(dialog)
        # Carregar dados após o dialog estar na página
        dialog.load_category()
    
    def manage_brands_clicked(self, e):
        dialog = Brand(self)
        self.route.page.open(dialog)
        # Carregar dados após o dialog estar na página
        dialog.load_brand()

    def load_categories(self):
        mydb = ProductsDatabase(self.route)
        result = mydb.select_category()
        mydb.close()

        self.dp_category.options.clear()
        for data in result:
            # select_category() retorna objetos SQLAlchemy Category
            name_val = data.category
            self.dp_category.options.append(dropdown.Option(name_val))
        self.dp_category.update()

    def load_brands(self):
        mydb = ProductsDatabase(self.route)
        result = mydb.select_brand()
        mydb.close()
        
        self.dp_brand.options.clear()
        for data in result:
            # select_brand() retorna objetos SQLAlchemy Brand
            name_val = data.brand
            self.dp_brand.options.append(dropdown.Option(name_val))
        self.dp_brand.update()

    def validate_int_fields(self, e):
        fields = [self.tf_stock, self.tf_min_stock, self.tf_max_stock]
        for control in fields:
            if control.value != "":
                value = Validator.format_to_int(control.value)
                if value is not None and value >= 0:
                    control.error_text = ""
                else:
                    control.error_text = "Valor inválido!"
                    self.set_buttons_state(True)
        self.update()

    def validate_float_fields(self, e):
        fields = [self.tf_costs, self.tf_margin, self.tf_selling_price]
        for control in fields:
            if control.value != "":
                value = Validator.format_to_float(control.value)
                if value is not None and value >= 0:
                    control.error_text = ""
                else:
                    control.error_text = "Valor inválido!"
                    self.set_buttons_state(True)
        self.update()

    def calc_margin(self, e):
        cost = Validator.format_to_float(self.tf_costs.value)
        selling_price = Validator.format_to_float(self.tf_selling_price.value)

        if not all(isinstance(value, float) for value in [cost, selling_price]):
            return

        if cost != 0:
            margin = (selling_price - cost) / cost * 100
        else:
            margin = 100
        self.tf_costs.value = Validator.format_to_currency(cost)
        self.tf_selling_price.value = Validator.format_to_currency(selling_price)
        self.tf_margin.value = Validator.format_to_currency(margin)
        self.tf_margin.update()
        self.analyze_fields(e)

    def calc_selling_price(self, e):
        cost = Validator.format_to_float(self.tf_costs.value)
        margin = Validator.format_to_float(self.tf_margin.value)

        if not all(isinstance(value, float) for value in [cost, margin]):
            return

        if cost != 0:
            selling_price = margin / 100 * cost + cost
        else:
            Notification(self.route.page, "Não é possível calcular o preço de venda com base na margem, pois o custo é R$0,00!", "red").show_message()
            return

        self.tf_costs.value = Validator.format_to_currency(cost)
        self.tf_margin.value = Validator.format_to_currency(margin)
        self.tf_selling_price.value = Validator.format_to_currency(selling_price)
        self.tf_selling_price.update()
        
        self.analyze_fields(e)

    def clear_fields(self):
        print("🔍 clear_fields chamado")
        print(f"🔍 Estado dos campos antes de limpar:")
        print(f"  - tf_id.value: {self.tf_id.value}")
        print(f"  - tf_descr.value: {self.tf_descr.value}")
        print(f"  - dp_category.value: {self.dp_category.value}")
        print(f"  - dp_brand.value: {self.dp_brand.value}")
        
        for control in [self.tf_id, self.tf_descr, 
                        self.tf_stock, self.tf_min_stock,
                        self.tf_max_stock, self.tf_observ, self.tf_costs,
                        self.tf_selling_price, self.tf_margin]:
            control.value = ""
            control.error_text = ""
        self.dp_category.value = ""
        self.dp_brand.value = ""
        self.dt_order_history.rows.clear()
        self.text_total.value = ""
        self.set_buttons_state(True)
        self.tf_descr.focus()
        self.update()
        
        print(f"🔍 Estado dos campos após limpar:")
        print(f"  - tf_id.value: {self.tf_id.value}")
        print(f"  - tf_descr.value: {self.tf_descr.value}")
        print(f"  - dp_category.value: {self.dp_category.value}")
        print(f"  - dp_brand.value: {self.dp_brand.value}")

    def analyze_fields(self, e):
        required_fields = [
            self.tf_descr, self.dp_category, self.dp_brand, self.tf_stock, self.tf_min_stock,
            self.tf_max_stock, self.tf_costs, self.tf_selling_price,
            self.tf_margin
        ]

        all_fields_filled = all(control.value != "" for control in required_fields)
        all_fields_empty = all(control.value == "" or None for control in required_fields)

        for control in required_fields:
            control.error_text = "" if control.value != "" else "Campo obrigatório"

        if all_fields_empty:
            for control in required_fields:
                control.error_text = ""

        self.set_buttons_state(not all_fields_filled)
        self.validate_int_fields(e)
        self.validate_float_fields(e)
        self.update()

    def load_product(self, id):
        print(f"🔍 load_product chamado com ID: {id} (tipo: {type(id)})")
        
        mydb = ProductsDatabase(self.route)
        result = mydb.select_products_full(id)
        mydb.close()

        print(f"🔍 Resultado da consulta: {result}")
        print(f"🔍 Tipo do resultado: {type(result)}")

        if result is None:
            print(f"❌ ERRO: Nenhum produto encontrado para ID: {id}")
            return

        # O método select_products_full retorna uma tupla com os dados já formatados
        # Tupla: (id, descr, category, brand, stock, minstock, maxstock, observ, costs, sellprice, margin)
        data_list = list(result)
        print(f"🔍 Data list: {data_list}")

        # Carregar dados nos campos
        self.tf_id.value = str(data_list[0])
        self.tf_descr.value = str(data_list[1])
        self.dp_category.value = str(data_list[2])
        self.dp_brand.value = str(data_list[3])
        self.tf_stock.value = str(data_list[4])
        self.tf_min_stock.value = str(data_list[5])
        self.tf_max_stock.value = str(data_list[6])
        self.tf_observ.value = str(data_list[7])

        # Formatar valores monetários
        try:
            self.tf_costs.value = Validator.format_to_currency(float(data_list[8]))
        except Exception:
            self.tf_costs.value = str(data_list[8])

        try:
            self.tf_selling_price.value = Validator.format_to_currency(float(data_list[9]))
        except Exception:
            self.tf_selling_price.value = str(data_list[9])

        try:
            self.tf_margin.value = Validator.format_to_currency(float(data_list[10]))
        except Exception:
            self.tf_margin.value = str(data_list[10])

        print(f"🔍 Campos carregados:")
        print(f"  - tf_id.value: {self.tf_id.value}")
        print(f"  - tf_descr.value: {self.tf_descr.value}")
        print(f"  - dp_category.value: {self.dp_category.value}")
        print(f"  - dp_brand.value: {self.dp_brand.value}")

        # Habilitar botões de salvar
        self.set_buttons_state(False)
        print(f"🔍 Chamando self.update()")
        self.update()
        print(f"🔍 self.update() concluído")

    def set_buttons_state(self, disabled):
        """Controla o estado dos botões de salvar"""
        self.btn_save_exit.disabled = disabled
        self.btn_save_view.disabled = disabled
        self.btn_save_new.disabled = disabled

    def save_exit_clicked(self, e):
        """Salva e volta para a lista de produtos"""
        if self.tf_id.value == "":
            self.register_product(e)
        else:
            self.update_product(e)
        self.back_clicked(e)

    def save_view_clicked(self, e):
        """Salva e recarrega o produto em modo de edição"""
        if self.tf_id.value == "":
            # Novo produto - registrar primeiro
            self.register_product(e)
            # Aguardar um pouco para o produto ser registrado
            import time
            time.sleep(0.1)
            # Tentar carregar o produto recém-criado
            try:
                mydb = ProductsDatabase(self.route)
                # Buscar o último produto inserido
                result = mydb.select_products_full(None)  # Buscar todos
                mydb.close()
                if result:
                    # Pegar o último produto (assumindo que é o recém-criado)
                    if isinstance(result, list):
                        last_product = result[-1]
                        product_id = last_product[0] if hasattr(last_product, '__getitem__') else last_product.idproducts
                    else:
                        product_id = result.idproducts
                    self.load_product(product_id)
            except Exception as ex:
                print(f"❌ Erro ao carregar produto recém-criado: {ex}")
                self.clear_fields()
        else:
            # Produto existente - atualizar
            self.update_product(e)
            # Recarregar o produto
            try:
                self.load_product(int(self.tf_id.value))
            except Exception as ex:
                print(f"❌ Erro ao recarregar produto: {ex}")

    def save_new_clicked(self, e):
        """Salva e inicia um novo cadastro"""
        if self.tf_id.value == "":
            self.register_product(e)
        else:
            self.update_product(e)
        self.clear_fields()

    def add_save_clicked(self, e):
        if self.tf_id.value == "":
            self.register_product(e)
        else:
            self.update_product(e)

    def register_product(self, e):
        fulldataset = [
            self.tf_descr.value.upper(),
            self.dp_category.value,
            self.dp_brand.value,
            int(self.tf_stock.value),
            int(self.tf_min_stock.value),
            int(self.tf_max_stock.value),
            self.tf_observ.value,
            Validator.format_to_float(self.tf_costs.value),
            Validator.format_to_float(self.tf_selling_price.value),
            Validator.format_to_float(self.tf_margin.value),
        ]
        
        mydb = ProductsDatabase(self.route)
        result = mydb.register_products(fulldataset)
        mydb.close()

        if result == "success":
            Notification(self.route.page, "Produto registrado com sucesso", "green").show_message()
        else:
            Notification(self.route.page, f"Erro ao registrar o produto: {result}", "red").show_message()

    def update_product(self, e):
        fulldataset = [
            int(self.tf_id.value),
            self.tf_descr.value.upper(),
            self.dp_category.value,
            self.dp_brand.value,
            int(self.tf_stock.value),
            int(self.tf_min_stock.value),
            int(self.tf_max_stock.value),
            self.tf_observ.value,
            Validator.format_to_float(self.tf_costs.value),
            Validator.format_to_float(self.tf_selling_price.value),
            Validator.format_to_float(self.tf_margin.value),
        ]
        
        mydb = ProductsDatabase(self.route)
        result = mydb.update_products(fulldataset)
        mydb.close()

        if result == "success":
            Notification(self.route.page, "Produto atualizado com sucesso", "green").show_message()
        else:
            Notification(self.route.page, f"Erro ao atualizar o produto: {result}", "red").show_message()

    def get_sold_from_db(self):
        print(f"🔍 get_sold_from_db chamado com tf_id.value: {self.tf_id.value}")
        
        mydb = SalesDatabase(self.route)
        result = mydb.select_sold_history(self.tf_id.value)
        mydb.close()

        print(f"🔍 Resultado select_sold_history: {result}")
        
        if result:
            total = sum(map(lambda x: x[2], result))
            self.text_total.value = f"R${Validator.format_to_currency(total)}"
            self.update()
            self.fill_in_history_table(result)
        else:
            print("🔍 Nenhum histórico de vendas encontrado")
            self.text_total.value = "R$ 0,00"
            self.update()

    def fill_in_history_table(self, fulldata):
        self.dt_order_history.rows.clear()
        for data in fulldata:
            self.dt_order_history.rows.append(
                DataRow(
                    cells=[
                        DataCell(Text(data[0])),
                        DataCell(Text(data[1])),
                        DataCell(Text(value=f"R${Validator.format_to_currency(data[2])}")),
                        DataCell(IconButton(icon=Icons.VISIBILITY_OUTLINED, icon_color="blue", tooltip="Ver pedido", data=data[0], on_click=self.see_sale_clicked)),
                    ]
                )
            )
        self.dt_order_history.update()

    def see_sale_clicked(self, e):
        self.route.page.go("/sales")
        self.route.bar.set_title("Vendas")
        self.route.menu.nnrail.selected_index = 4
        self.route.menu.update()
        self.route.page.update()

        self.route.sales.select_sale_clicked(e.control.data)
