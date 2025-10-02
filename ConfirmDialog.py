import flet as ft

class ConfirmDialog(ft.AlertDialog):
    """Creates an AlertDialog that, if "yes" clicked, executes the function passed as a parameter.

    Args:
        function (method): method to be executed
        title (string): title of the dialog
        content (string): content of the question to be confirmed
    """
    def __init__(self, function, title="Confirmação", content="Tem certeza que deseja excluir?"):
        super().__init__()
        self.function = function
        self.data = None
        self.page = None

        self.modal = True
        self.title = ft.Text(title, size=18, weight="bold")
        self.content = ft.Text(content, size=14)
        
        # Criar botões seguindo o padrão oficial do Flet
        self.btn_cancel = ft.TextButton(
            text="Não",
            on_click=self.on_cancel
        )
        
        self.btn_confirm = ft.TextButton(
            text="Sim",
            on_click=self.on_confirm
        )
        
        self.actions = [
            self.btn_cancel,
            self.btn_confirm,
        ]
        self.actions_alignment = ft.MainAxisAlignment.END
        self.alignment = ft.alignment.center

    def on_cancel(self, e):
        print(f"🔍 ConfirmDialog: Botão 'Não' clicado!")
        e.page.close(self)
    
    def on_confirm(self, e):
        print(f"🔍 ConfirmDialog: Botão 'Sim' clicado!")
        print(f"🔍 ConfirmDialog: Dados do diálogo: {self.data}")
        print(f"🔍 ConfirmDialog: Função a ser executada: {self.function}")
        e.page.close(self)
        print(f"🔍 ConfirmDialog: Executando função...")
        self.function(self.data)
        print(f"🔍 ConfirmDialog: Função executada!")
