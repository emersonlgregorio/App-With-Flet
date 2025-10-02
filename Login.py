from flet import (Container, Row, Column, Container, Text, TextField, Icons, Colors, TextThemeStyle, OutlinedButton,
                  MainAxisAlignment, CrossAxisAlignment, alignment, padding, BoxShadow, Offset, ShadowBlurStyle)
from Database import UserDatabase
from Notification import Notification
from CreateFirstAdmin import CreateFirstAdmin

class Login(Container):
    def __init__(self, route):
        super().__init__()
        self.route = route
        
        self.text_user = TextField(label="Usuário", prefix_icon=Icons.PERSON_2_OUTLINED, expand=True, autofocus=True, on_change=self.analyze_to_enable_button)
        self.text_password = TextField(label="Senha", prefix_icon=Icons.LOCK_OUTLINE_ROUNDED, expand=True, password=True, can_reveal_password=True, on_change=self.analyze_to_enable_button)
        self.btn_login = OutlinedButton(text="Login", width=240, icon=Icons.LOGIN_OUTLINED, disabled=True, on_click=self.login_clicked)
        
        # Configurar o Container diretamente
        self.expand = True
        self.alignment = alignment.center
        self.content = Row(
            expand=True,
            alignment=MainAxisAlignment.CENTER,
            vertical_alignment=CrossAxisAlignment.CENTER,
            controls=[
                    Container(
                        padding=padding.only(60, 34, 60, 20),
                        bgcolor=Colors.SURFACE,
                        border_radius=10,
                        width=500,
                        height=360,
                        shadow=BoxShadow(
                            spread_radius=5,
                            blur_radius=5,
                            color=Colors.GREY_300,
                            offset=Offset(1,1),
                            blur_style=ShadowBlurStyle.NORMAL,
                        ),
                        content=Column(
                            #expand=True,
                            spacing=30,
                            alignment=MainAxisAlignment.START,
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                            tight=True,
                            controls=[
                                Row(
                                    alignment=MainAxisAlignment.CENTER,
                                    controls=[
                                        Text('Login', style=TextThemeStyle.TITLE_LARGE)
                                    ]
                                ),
                                Row(
                                    controls=[
                                        self.text_user,                                        
                                    ]
                                ),
                                Row(
                                    controls=[
                                        self.text_password,
                                    ]
                                ),
                                Row(
                                    alignment=MainAxisAlignment.CENTER,
                                    controls=[
                                        self.btn_login,
                                    ]
                                )
                            ]
                        )
                    )
                ]
            )
    
    def initialize(self):
        # O timer já está rodando automaticamente no Appbar
        pass
    
    def verify_count_of_users(self):
        mydb = UserDatabase(self.route)
        result = mydb.select_users_count()
        mydb.close()
        if result == 0:
            return False
        return True

    def create_admin(self):
        dialog = CreateFirstAdmin(self.route)
        self.route.page.dialog = dialog
        dialog.open = True
        self.route.page.update()

    def go_to_home(self, name, permission):
        self.route.config.set_permissions(name, permission)
        
        self.page.go("/home")
        self.route.bar.enable_btn_logout()
        self.route.bar.set_username(name)
        self.route.bar.set_title('Página Inicial')
        self.route.menu.cont.visible = True
        self.route.menu.update()
        self.route.page.update()

    def login(self):
        data = [self.text_user.value, self.text_password.value]
        mydb = UserDatabase(self.route)
        name, permission = mydb.login_verify(data)
        mydb.close()

        if name is None:
            Notification(self.route.page, 'Usuário ou senha incorretos!', 'red').show_message()
            return
        self.go_to_home(name, permission)

    def login_clicked(self, e):
        self.route.config.initialize()
        
        if self.route.config.host is None:
            return
        
        if not self.verify_count_of_users():
            self.create_admin()
            return

        self.login()
            
    def analyze_to_enable_button(self, e):
        self.btn_login.disabled = (
            self.text_user.value == "" or self.text_password.value == ""
        )
        self.update()
        
