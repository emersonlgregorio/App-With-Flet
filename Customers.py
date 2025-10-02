from flet import (Container, Row, Column, Container, Text, TextField, IconButton, DataTable, 
                  DataRow, DataColumn, DataCell, Icons, TextThemeStyle, VerticalDivider, ListView, Colors,
                  MainAxisAlignment, CrossAxisAlignment, FilePickerResultEvent, Card, Divider)
from Database import CustomerDatabase, SalesDatabase
from ConfirmDialog import ConfirmDialog
from Notification import Notification
from Reports import CustomerReport
from Notification import Notification
from Validator import Validator

class Customers(Container):
    def __init__(self, route):
        super().__init__()
        self.route = route

        self.btn_clear_filters = IconButton(icon=Icons.CLEAR_ALL_OUTLINED, tooltip="Limpar Filtros", on_click=self.clear_filter_clicked)
        self.tf_find_customer = TextField(label='Buscar...', expand=True, dense=True, prefix_icon=Icons.SEARCH_ROUNDED, on_change=self.find_customers)
        self.btn_print = IconButton(icon=Icons.PICTURE_AS_PDF_OUTLINED, tooltip="Gerar arquivo .pdf", on_click=self.pdf_clicked)
        self.btn_new_customer = IconButton(icon=Icons.ADD_OUTLINED, tooltip="Novo Cliente", icon_color="primary", icon_size=36, on_click=self.new_customer_clicked)
        self.text_total = Text('R$0,00', style=TextThemeStyle.TITLE_MEDIUM)

        self.dt_customers = DataTable(                                            
            expand=True,
            divider_thickness=0.4,
            #heading_row_color=Colors.SURFACE_VARIANT,
            sort_ascending=True,
            columns=[
                DataColumn(Text('ID')), 
                DataColumn(Text('NOME')), 
                DataColumn(Text('CPF')),
                DataColumn(Text('TELEFONE')), 
                DataColumn(Text('AÇÕES')), 
            ],
            rows=[
                DataRow(
                    cells=[
                        DataCell(Text('02')),
                        DataCell(Text("John Player Special")),
                        DataCell(Text("308.602.798-39")),
                        DataCell(Text("18 99999 9999")),
                        DataCell(Row([IconButton(icon=Icons.EDIT_OUTLINED, icon_color='blue'), 
                                      IconButton(icon=Icons.DELETE_OUTLINED, icon_color='red'), 
                                      IconButton(icon=Icons.ADD_SHOPPING_CART_OUTLINED, icon_color='green'),
                        ])),
                    ],
                ),
            ],
        )

        self.dt_order_history = DataTable(
            column_spacing=15,
            divider_thickness=0.4,
            #heading_row_color=Colors.ON_INVERSE_SURFACE,
            expand=True,
            columns=[
                DataColumn(Text('Pedido')), 
                DataColumn(Text('Data')), 
                DataColumn(Text('Valor')),
                DataColumn(Text('Ver')),                                                 
            ],
        )

        self.side_card_column = Column()
        self.side_card = Card(
            elevation=1.5,
            animate_scale=200,
            #expand=True,
            surface_tint_color=Colors.INVERSE_PRIMARY,
            content=Container(
                padding=10,
                content=self.side_card_column,
            )
        )

    def build(self):
        customers_content = Container(
            #bgcolor='red',
            padding=0,
            border_radius=5,
            expand=True,
            content=Column(
                controls=[
                    # Corpo principal
                    Container(
                        #bgcolor='white',
                        expand=True,
                        content=Row(
                            vertical_alignment=CrossAxisAlignment.START,
                            controls=[
                                Container(
                                    #bgcolor='red',
                                    expand=5,
                                    border_radius=5,
                                    padding=15,
                                    content=Column(
                                        expand=True,
                                        alignment=MainAxisAlignment.CENTER,
                                        spacing=20,
                                        horizontal_alignment=CrossAxisAlignment.CENTER,
                                        controls=[
                                            Row(
                                                spacing=20,
                                                controls=[
                                                    self.btn_clear_filters,
                                                    self.btn_print,
                                                    self.tf_find_customer,
                                                    self.btn_new_customer,
                                                ]
                                            ),
                                            ListView(
                                                expand=True,
                                                controls=[
                                                    self.dt_customers,
                                                ]
                                            ),
                                        ]
                                    )
                                ),
                                VerticalDivider(width=1),
                                Container(
                                    #bgcolor='red',
                                    expand=2,
                                    border_radius=5,
                                    padding=15,
                                    content=Column(
                                        expand=True,
                                        controls=[
                                            Column(
                                                #expand=1,
                                                horizontal_alignment='center',
                                                controls=[
                                                    self.side_card,
                                                ]
                                            ),
                                            Divider(height=3, color="transparent"),
                                            Column(
                                                alignment=MainAxisAlignment.START,
                                                horizontal_alignment=CrossAxisAlignment.CENTER,
                                                spacing=10,
                                                expand=True,
                                                controls=[
                                                    Text('Histórico de Pedidos', style=TextThemeStyle.TITLE_MEDIUM),
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
                customers_content,
            ]
        )
        # Configurar o Container diretamente
        self.content = customers_content
    
    def new_customer_clicked(self, e):
        self.route.page.go("/register_customer")
        self.route.bar.set_title('Cadastrar Novo Cliente')
        self.route.page.update()

    def initialize(self):
        print("Initializing Customers's Page")
        self.dt_order_history.rows.clear()
        self.side_card.visible = False
        self.text_total.value = ""
        self.update()
        self.load_customers()

    def load_customers(self):
        self.dt_customers.rows.clear()
        mydb = CustomerDatabase(self.route)
        result = mydb.select_customers()
        mydb.close()

        for data in result:
            self.dt_customers.rows.append(
                DataRow(
                    cells=[
                        DataCell(Text(str(data[0]))),
                        DataCell(Text(data[1])),
                        DataCell(Text(data[2])),
                        DataCell(Text(data[3])),
                        DataCell(Row([IconButton(icon=Icons.EDIT_OUTLINED, icon_color='blue', data=data[2], tooltip="Editar Cliente", on_click=self.edit_clicked),
                                      IconButton(icon=Icons.DELETE_OUTLINED, icon_color='red', data=data[2], tooltip="Excluir Cliente", on_click=self.delete_clicked), 
                                      IconButton(icon=Icons.ADD_SHOPPING_CART_OUTLINED, icon_color='green', tooltip="Nova Venda", data=data[2], on_click=self.new_sale_clicked),
                        ])),
                    ],
                    on_select_changed=lambda e: self.table_row_clicked(e.control.cells[0].content.value, e.control.cells[2].content.value),
                ),
            )
        self.dt_customers.update()

    def delete_clicked(self, e):
        print(f"🔍 Botão excluir clicado!")
        cpf_cnpj = e.control.data
        print(f"🔍 CPF/CNPJ do cliente a ser excluído: {cpf_cnpj}")
        
        # Criar e exibir diálogo de confirmação usando o padrão oficial do Flet
        dialog = ConfirmDialog(
            self.delete_customer, 
            "Confirmar Exclusão", 
            f"Tem certeza que deseja excluir o cliente com CPF/CNPJ '{cpf_cnpj}'?"
        )
        dialog.data = cpf_cnpj
        print(f"🔍 Diálogo criado: {dialog}")
        
        # Usar page.open() em vez de dialog.open = True
        self.route.page.open(dialog)
        print(f"🔍 Diálogo aberto usando page.open()")

    def delete_customer(self, id):
        print(f"🔍 Customers: Método delete_customer chamado com ID: {id}")
        mydb = CustomerDatabase(self.route)
        result = mydb.delete_customer(id)
        mydb.close()

        if result == 'success':
            Notification(self.route.page, "Cliente excluído com sucesso!", "green").show_message()
        else:
            Notification(self.route.page, f"Erro ao excluir o cliente: {result}", "red").show_message()
        self.load_customers()
        self.route.page.update()

    def edit_clicked(self, e):
        self.route.page.go("/register_customer")
        self.route.bar.set_title('Editar Cliente')
        self.route.page.update()
        
        self.route.register_customer.text_new_customer.value = "Editar Cliente:"
        self.route.register_customer.load_customer(e.control.data)

        self.route.register_customer.get_sales_data_from_db()

    def find_customers(self, e):
        if self.tf_find_customer.value == "":
            self.load_customers()
            self.update()
            return
        
        self.dt_customers.rows.clear()
        mydb = CustomerDatabase(self.route)
        result = mydb.find_customer(self.tf_find_customer.value)
        mydb.close()
        
        for data in result:
            self.dt_customers.rows.append(
                DataRow(
                    cells=[
                        DataCell(Text(str(data[0]))),
                        DataCell(Text(data[1])),
                        DataCell(Text(data[2])),
                        DataCell(Text(data[3])),
                        DataCell(Row([IconButton(icon=Icons.EDIT_OUTLINED, icon_color='blue', data=data[2], tooltip="Editar cliente", on_click=self.edit_clicked),
                                      IconButton(icon=Icons.DELETE_OUTLINED, icon_color='red', data=data[2], tooltip="Excluir cliente", on_click=self.delete_clicked), 
                                      IconButton(icon=Icons.ADD_SHOPPING_CART_OUTLINED, icon_color='green', data=data[2], tooltip="Nova venda", on_click=self.new_sale_clicked),
                        ])),
                    ],
                    on_select_changed=lambda e: self.table_row_clicked(e.control.cells[0].content.value, e.control.cells[2].content.value),
                ),
            )
        self.update()
        self.route.page.update()

    def create_report_customer(self, e: FilePickerResultEvent):
        if e.path is None:
            return
        filename = f"{e.path}.{e.control.allowed_extensions[0]}"
        text = [
            self.dt_customers.columns[0].label.value,
            self.dt_customers.columns[1].label.value,
            self.dt_customers.columns[2].label.value,
            self.dt_customers.columns[3].label.value,
        ]

        data = [text]
        for row in range(len(self.dt_customers.rows)):
            text = []
            for col in range(len(self.dt_customers.columns)):
                text.append(self.dt_customers.rows[row].cells[col].content.value) if col < 4 else None
            data.append(text)
    
        printer = CustomerReport(filename, data)
        result, error = printer.print_report()
        
        if result == 'success':
            Notification(self.page, f'Arquivo "{filename}" gerado com sucesso!', "green").show_message()
        else:
            Notification(self.page, f'Erro ao gerar o arquivo {filename}: "{error}"', "red").show_message()

    def pdf_clicked(self, e):
        self.route.save_file_dialog.on_result = self.create_report_customer
        self.route.save_file_dialog.save_file(dialog_title="Salvar como ...", allowed_extensions=["pdf"])
        self.update()

    def new_sale_clicked(self, e):
        mydb = CustomerDatabase(self.route)
        result = mydb.select_one_customer(e.control.data)
        mydb.close()
        data = list(result[0])
        del data[-3:]
        
        self.route.page.go("/register_sales")
        self.route.bar.set_title("Nova Venda")
        self.route.menu.nnrail.selected_index = 4
        self.route.menu.update()
        self.route.page.update()

        self.route.register_sales.fill_in_customer_to_register(e, data)

    def table_row_clicked(self, id_customer, cpf_cnpj):
        mydb = CustomerDatabase(self.route)
        result = mydb.select_one_customer(cpf_cnpj)
        adresses = mydb.select_adresses(cpf_cnpj)
        mydb.close()
        self.fill_in_side_card(result[0], adresses)
        
        mydb = SalesDatabase(self.route)
        result = mydb.select_sales_history(id_customer)
        mydb.close()
        total = sum(map(lambda x: x[2], result))
        self.text_total.value = f"R${Validator.format_to_currency(total)}"
        self.update()
        self.fill_in_history_table(result)

    def fill_in_history_table(self, fulldata):
        self.dt_order_history.rows.clear()
        for data in fulldata:
            self.dt_order_history.rows.append(
                DataRow(
                    cells=[
                        DataCell(Text(data[0])),
                        DataCell(Text(data[1])),
                        DataCell(Text(f"R${Validator.format_to_currency(data[2])}")),
                        DataCell(IconButton(icon=Icons.VISIBILITY_OUTLINED, icon_color="blue", data=data[0], tooltip="Visualizar pedido", on_click=self.see_sale_clicked))
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

    def fill_in_side_card(self, customer_data, adresses):
        self.side_card.visible = True
        self.side_card_column.controls.clear()
        self.side_card_column.controls.append(Row(alignment='center', controls=[Text(value=customer_data[1], text_align="center", expand=True, style=TextThemeStyle.TITLE_SMALL)]),)
        self.side_card_column.controls.append(Row(alignment="left", spacing=20, controls=[Text(value=f"ID: {customer_data[0]}"), Text(value=f"CPF: {customer_data[2]}"),]),)
        self.side_card_column.controls.append(Text(value=f"Tel.: {customer_data[3]}"),)
        self.side_card_column.controls.append(Text(value=f"E-mail: {customer_data[4]}"),)
        self.side_card_column.controls.append(Text(value=f"Observ.: {customer_data[5]}"),)
        self.side_card_column.controls.append(Divider(height=1),)

        for i, data in enumerate(adresses):
            self.side_card_column.controls.append(
                Text(value=f"Ender. {i+1}: {data[0]}, {data[1]}/{data[2]}, CEP {data[3]}"),
            )
        self.side_card_column.update()

    def clear_filter_clicked(self, e):
        self.tf_find_customer.value = ""
        self.update()
        self.load_customers()
