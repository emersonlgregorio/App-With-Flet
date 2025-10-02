import flet as ft

def main(page: ft.Page):
    page.title = "Teste Modal Confirmação"

    def show_confirm_dialog(e):
        def on_confirm():
            print("🔍 Usuário confirmou!")
            page.close(dialog)
        
        def on_cancel():
            print("🔍 Usuário cancelou!")
            page.close(dialog)

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar Exclusão", size=18, weight="bold"),
            content=ft.Text("Tem certeza que deseja excluir este usuário?", size=14),
            actions=[
                ft.TextButton("Não", on_click=lambda e: on_cancel()),
                ft.TextButton("Sim", on_click=lambda e: on_confirm()),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            alignment=ft.alignment.center,
        )
        
        print("🔍 Abrindo diálogo...")
        page.open(dialog)

    page.add(
        ft.ElevatedButton("Testar Modal", on_click=show_confirm_dialog)
    )

if __name__ == "__main__":
    ft.app(target=main)

