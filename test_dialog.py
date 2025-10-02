from flet import app, Page, AlertDialog, TextButton, Text, MainAxisAlignment, RoundedRectangleBorder

def main(page: Page):
    page.title = "Teste Dialog"
    
    def show_dialog(e):
        def close_dialog(e):
            page.dialog.open = False
            page.update()
            print("🔍 Diálogo fechado!")

        def confirm_delete(e):
            page.dialog.open = False
            page.update()
            print("🔍 Confirmação clicada!")

        dialog = AlertDialog(
            modal=True,
            title=Text("Confirmação"),
            content=Text("Tem certeza que deseja excluir?"),
            actions=[
                TextButton("Não", on_click=close_dialog),
                TextButton("Sim", on_click=confirm_delete),
            ],
            actions_alignment=MainAxisAlignment.END,
            shape=RoundedRectangleBorder(radius=10)
        )
        page.dialog = dialog
        dialog.open = True
        page.update()
        print("🔍 Diálogo aberto!")

    page.add(TextButton("Testar Dialog", on_click=show_dialog))

if __name__ == "__main__":
    app(target=main)
