from flet import (Container, Row, Column, Container, Text, IconButton, Icons, Colors, padding, FontWeight,
                  alignment, MainAxisAlignment, CrossAxisAlignment, AppBar, Icon, PopupMenuButton, PopupMenuItem,
                  Theme, ThemeMode)
import datetime
import locale
import threading
import time

class Appbar(Container):
    def __init__(self, route):
        super().__init__()
        self.route = route

        self.hour_text = Text('', size=15, weight=FontWeight.W_600)
        self.week_text = Text('', size=12, weight=FontWeight.W_200)
        self.text_title = Text(value='Login', size=26, weight=FontWeight.W_500)
        self.btn_change_theme = IconButton(icon=Icons.DARK_MODE_OUTLINED, tooltip="Tema claro/escuro", on_click=self.change_theme)
        self.text_user = Text('Faça o Login para acessar o sistema!', size=15, weight=FontWeight.W_600)
        self.btn_logout = IconButton(icon=Icons.LOGOUT_OUTLINED, disabled=True, tooltip="Logout", on_click=self.logout)

        # Timer simples para atualizar data/hora (iniciado após criar os elementos)
        self.timer_running = True
        self.timer_thread = threading.Thread(target=self.update_timer, daemon=True)
        self.timer_thread.start()

        # Configurar locale de forma segura
        try:
            locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')
        except locale.Error:
            try:
                locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
            except locale.Error:
                try:
                    locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil.1252')
                except locale.Error:
                    # Usar locale padrão se pt_BR não estiver disponível
                    pass

    def build(self):
        self.app_barr = AppBar(
            elevation=10,
            leading_width=180,        
            bgcolor=Colors.PRIMARY_CONTAINER,
            leading=Container(
                #bgcolor='grey',
                padding=padding.only(left=15),
                alignment=alignment.center,
                content=Row(
                    expand=True,
                    alignment=MainAxisAlignment.CENTER,
                    vertical_alignment=CrossAxisAlignment.CENTER,
                    controls=[
                        Icon(Icons.COTTAGE_OUTLINED, size=36),
                        Column(
                            expand=True,
                            alignment=MainAxisAlignment.CENTER,
                            spacing=0,
                            controls=[
                                self.hour_text,
                                self.week_text
                            ]
                        )
                    ]            
                )
            ),
            title = self.text_title,
            actions=[
                self.btn_change_theme,
                PopupMenuButton(
                    icon=Icons.COLOR_LENS_OUTLINED,
                    tooltip="Trocar cor do tema",
                    items=[
                        PopupMenuItem(
                            content=Row(
                                controls=[
                                    Icon(Icons.COLOR_LENS_OUTLINED, color=Colors.PURPLE_300),
                                    Text('Roxo')
                                ]
                            ),
                            on_click=self.change_color_seed,          
                        ),
                        PopupMenuItem(
                            content=Row(
                                controls=[
                                    Icon(Icons.COLOR_LENS_OUTLINED, color=Colors.ORANGE_300),
                                    Text('Laranja')
                                ]
                            ),
                            on_click=self.change_color_seed,           
                        ),
                        PopupMenuItem(
                            content=Row(
                                controls=[
                                    Icon(Icons.COLOR_LENS_OUTLINED, color=Colors.GREEN_300),
                                    Text('Verde')
                                ]
                            ),
                            on_click=self.change_color_seed,           
                        ),
                        PopupMenuItem(
                            content=Row(
                                controls=[
                                    Icon(Icons.COLOR_LENS_OUTLINED, color=Colors.RED_300),
                                    Text('Vermelho')
                                ]
                            ),
                            on_click=self.change_color_seed,           
                        ),
                        PopupMenuItem(
                            content=Row(
                                controls=[
                                    Icon(Icons.COLOR_LENS_OUTLINED, color=Colors.BLUE_300),
                                    Text('Azul (Default)')
                                ]
                            ),
                            on_click=self.change_color_seed,         
                        ),
                        PopupMenuItem(
                            content=Row(
                                controls=[
                                    Icon(Icons.COLOR_LENS_OUTLINED, color=Colors.YELLOW_300),
                                    Text('Amarelo')
                                ]
                            ),
                            on_click=self.change_color_seed,          
                        ),
                        PopupMenuItem(
                            content=Row(
                                controls=[
                                    Icon(Icons.COLOR_LENS_OUTLINED, color=Colors.INDIGO_300),
                                    Text('Indigo')
                                ]
                            ),
                            on_click=self.change_color_seed,          
                        ),
                        PopupMenuItem(
                            content=Row(
                                controls=[
                                    Icon(Icons.COLOR_LENS_OUTLINED, color=Colors.TEAL_300),
                                    Text('Teal')
                                ]
                            ),
                            on_click=self.change_color_seed,          
                        ),
                        PopupMenuItem(
                            content=Row(
                                controls=[
                                    Icon(Icons.COLOR_LENS_OUTLINED, color=Colors.LIME_300),
                                    Text('Lime')
                                ]
                            ),
                            on_click=self.change_color_seed,          
                        ),
                        PopupMenuItem(
                            content=Row(
                                controls=[
                                    Icon(Icons.COLOR_LENS_OUTLINED, color=Colors.BROWN_400),
                                    Text('Marrom')
                                ]
                            ),
                            on_click=self.change_color_seed,          
                        ),
                    ]
                ),
                Container(
                    padding=10,
                    content=Column(
                        spacing=0,
                        controls=[
                            Text('Bem Vindo!', size=12),
                            self.text_user,
                        ],
                    ),
                ),
                self.btn_logout,
            ],
        )    
        return self.app_barr

    def change_theme(self, e):        
        if self.route.page.theme_mode == ThemeMode.LIGHT:
            self.route.page.theme_mode=ThemeMode.DARK
            self.btn_change_theme.icon = Icons.WB_SUNNY_OUTLINED
            self.route.page.update()
            return
        if self.route.page.theme_mode == ThemeMode.DARK:
            self.route.page.theme_mode=ThemeMode.LIGHT
            self.btn_change_theme.icon = Icons.DARK_MODE_OUTLINED
            self.route.page.update()
            return

    def change_color_seed(self, e):
        self.route.page.theme = Theme(
            color_scheme_seed=e.control.content.controls[0].color
        )
        self.route.page.update()

    def set_title(self, text):
        self.text_title.value = text
        self.text_title.update()

    def enable_btn_logout(self):
        self.btn_logout.disabled = False

    def logout(self, e):
        self.route.page.go("/")
        self.btn_logout.disabled = True
        self.set_username('Faça o Login para acessar o sistema!')
        self.set_title("Login")
        #self.update()
        self.route.menu.cont.visible = False
        self.route.menu.update()
        self.route.page.update()
    
    def set_username(self, text):
        self.text_user.value = text
        self.route.page.update()

    def update_timer(self):
        """Timer que atualiza a data/hora a cada segundo"""
        while self.timer_running:
            try:
                # Verificar se os elementos já foram criados e adicionados à página
                if (hasattr(self, 'hour_text') and hasattr(self, 'week_text') and 
                    hasattr(self.route, 'page') and self.route.page is not None):
                    self.update_day()
                time.sleep(1)
            except Exception as e:
                print(f"Erro no timer: {e}")
                break

    def update_day(self):
        try:
            # Obtém a data atual
            today = datetime.date.today()

            # Obtem a hora atual
            agora = datetime.datetime.now()

            # Formata a hora em uma string com o formato h:m:s
            hora_formatada = agora.strftime("%H:%M:%S")

            # Define o formato de data para apenas dia e mês
            date_format = "%d/%m"

            # Define o texto para a label de data
            date_text = today.strftime(date_format)

            # Define o texto para a label de dia da semana
            day_of_week_text = today.strftime("%A")

            # Define o texto das labels
            self.hour_text.value = f'{date_text} - {hora_formatada}'
            self.week_text.value = day_of_week_text.upper()
            
            # Atualizar apenas se os controles estão na página
            if hasattr(self.hour_text, 'page') and self.hour_text.page is not None:
                self.hour_text.update()
            if hasattr(self.week_text, 'page') and self.week_text.page is not None:
                self.week_text.update()
        except Exception as e:
            print(f"Erro ao atualizar data/hora: {e}")
        


