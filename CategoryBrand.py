"""
Módulo CategoryBrand - Gerenciamento de Categorias e Marcas

Este módulo contém as classes para gerenciamento de categorias e marcas
de produtos através de diálogos modais. Utiliza uma arquitetura baseada
em herança para evitar duplicação de código.

Classes:
    BaseManagementDialog: Classe base para diálogos de gerenciamento
    Category: Diálogo específico para gerenciamento de categorias
    Brand: Diálogo específico para gerenciamento de marcas

Funcionalidades:
    - Adicionar novas categorias/marcas
    - Listar categorias/marcas existentes
    - Excluir categorias/marcas
    - Validação de entrada
    - Tratamento de erros
    - Feedback visual através de SnackBars
"""

from flet import (
    DataTable, TextButton, TextField, IconButton, Text, Row,
    Column, ListView, MainAxisAlignment, AlertDialog, DataColumn,
    DataRow, DataCell, SnackBar, Icons, Colors
)
from Database import ProductsDatabase


class BaseManagementDialog(AlertDialog):
    """Classe base para diálogos de gerenciamento de categorias e marcas."""

    def __init__(self, products, title, field_label, table_name):
        super().__init__()
        self.products = products
        self.modal = True
        self.table_name = table_name
        self.title = Row(
            expand=True,
            controls=[Text(title, width=400)]
        )

        # Campo de entrada
        self.text_field = TextField(
            label=field_label, dense=True, expand=True
        )

        # Botão de salvar
        self.btn_save = IconButton(
            icon=Icons.SAVE_OUTLINED,
            icon_color=Colors.PRIMARY,
            icon_size=32,
            on_click=self._register_item
        )

        # Botão de voltar
        self.btn_back = TextButton(text="Voltar", on_click=self._back_clicked)

        # Tabela de dados
        self.data_table = DataTable(
            expand=True,
            columns=[
                DataColumn(Text('ID')),
                DataColumn(Text(table_name.upper())),
                DataColumn(Text('EXCLUIR')),
            ],
        )

        self.actions = [
            Column(
                width=400,
                expand=True,
                controls=[
                    Row(
                        controls=[
                            self.text_field,
                            self.btn_save,
                        ]
                    ),
                    ListView(
                        height=240,
                        controls=[
                            self.data_table,
                        ]
                    ),
                    Row(
                        alignment=MainAxisAlignment.END,
                        controls=[
                            self.btn_back,
                        ]
                    )
                ]
            )
        ]

    def build(self):
        """Retorna o diálogo construído."""
        return self

    def _back_clicked(self, e):
        """Callback para o botão voltar."""
        if self.table_name == "categorias":
            self.products.load_categories()
        else:
            self.products.load_brands()
        e.page.close(self)

    def _show_snackbar(self, message, is_success=True):
        """Exibe uma mensagem de snackbar."""
        color = 'green' if is_success else 'red'
        self.page.snack_bar = SnackBar(
            content=Text(message, color=color)
        )
        self.page.snack_bar.open = True

    def _register_item(self, e):
        """Registra um novo item no banco de dados."""
        # Validação de entrada
        if not self._validate_input():
            return

        def _execute_operation(mydb):
            if self.table_name == "categorias":
                return mydb.register_category(self.text_field.value.strip())
            else:
                return mydb.register_brand(self.text_field.value.strip())

        result = self._execute_db_operation(_execute_operation)

        if result == 'success':
            self._show_snackbar(
                f"{self.table_name.title()} registrada com sucesso!"
            )
            self.text_field.value = ""
        else:
            self._show_snackbar(
                f"Erro ao registrar a {self.table_name}: {result}", False
            )

        self._load_items()
        self.page.update()

    def _delete_item(self, e):
        """Deleta um item do banco de dados."""
        def _execute_operation(mydb):
            if self.table_name == "categorias":
                return mydb.delete_category(e.control.data)
            else:
                return mydb.delete_brand(e.control.data)

        result = self._execute_db_operation(_execute_operation)

        if result == 'success':
            self._show_snackbar(
                f"{self.table_name.title()} deletada com sucesso!"
            )
        else:
            self._show_snackbar(
                f"Erro ao deletar a {self.table_name}: {result}", False
            )

        self._load_items()
        self.page.update()

    def _load_items(self):
        """Carrega os itens do banco de dados."""
        def _execute_operation(mydb):
            if self.table_name == "categorias":
                return mydb.select_category()
            else:
                return mydb.select_brand()

        result = self._execute_db_operation(_execute_operation)

        if result is None:
            return  # Erro já foi tratado em _execute_db_operation

        self.data_table.rows.clear()
        for data in result:
            if self.table_name == "categorias":
                id_val = data.idcategory
                name_val = data.category
            else:
                id_val = data.idbrand
                name_val = data.brand

            self.data_table.rows.append(
                DataRow(
                    cells=[
                        DataCell(Text(str(id_val))),
                        DataCell(Text(name_val)),
                        DataCell(Row([
                            IconButton(
                                icon=Icons.DELETE_OUTLINED,
                                icon_color='red',
                                data=id_val,
                                on_click=self._delete_item
                            )
                        ])),
                    ]
                )
            )

        # Verificar se o controle está na página antes de atualizar
        if (hasattr(self.data_table, 'page') and
                self.data_table.page is not None):
            self.data_table.update()

    def _validate_input(self):
        """Valida a entrada do usuário."""
        value = self.text_field.value.strip()

        if not value:
            self._show_snackbar("Por favor, insira um valor válido.", False)
            return False

        if len(value) < 2:
            self._show_snackbar(
                "O valor deve ter pelo menos 2 caracteres.", False
            )
            return False

        if len(value) > 50:
            self._show_snackbar(
                "O valor deve ter no máximo 50 caracteres.", False
            )
            return False

        return True

    def _execute_db_operation(self, operation_func):
        """Executa uma operação de banco de dados com tratamento de erros."""
        try:
            mydb = ProductsDatabase(self.products.route)
            result = operation_func(mydb)
            mydb.close()
            return result
        except Exception as ex:
            self._show_snackbar(
                f"Erro inesperado: {str(ex)}", False
            )
            if 'mydb' in locals():
                mydb.close()
            return None


class Category(BaseManagementDialog):
    """Diálogo para gerenciamento de categorias."""

    def __init__(self, products):
        super().__init__(
            products=products,
            title="Gerenciar Categorias:",
            field_label="Insira a nova categoria",
            table_name="categorias"
        )

    def load_category(self):
        """Carrega as categorias do banco de dados."""
        self._load_items()


class Brand(BaseManagementDialog):
    """Diálogo para gerenciamento de marcas."""

    def __init__(self, products):
        super().__init__(
            products=products,
            title="Gerenciar Marcas:",
            field_label="Insira a nova marca",
            table_name="marcas"
        )

    def load_brand(self):
        """Carrega as marcas do banco de dados."""
        self._load_items()
