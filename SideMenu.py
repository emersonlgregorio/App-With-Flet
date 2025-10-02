from flet import (Container, Container, IconButton, Icons, NavigationRail, NavigationRailLabelType,
                  NavigationRailDestination, Icon, padding, border_radius)

from SetGeneralConfig import SetGeneralConfig

class SideMenu(Container):
    def __init__(self, route):
        super().__init__()
        self.route = route
        
        self.cont = Container(            
            padding=padding.all(5),
            #bgcolor=Colors.ON_INVERSE_SURFACE,                       
            border_radius=border_radius.all(5),
            visible=False,
        )        
        self.nnrail = NavigationRail(
            extended=False,
            label_type=NavigationRailLabelType.NONE,
            min_width=56,                
            min_extended_width=160, 
            bgcolor='transparent',
            leading=IconButton(icon=Icons.SWAP_HORIZ_ROUNDED, icon_size=40, tooltip="Mostrar/Ocultar Opções", on_click=self.menu_clicked),
            group_alignment=-0.95,
            destinations=[
                NavigationRailDestination(
                    icon=Icons.COTTAGE_OUTLINED, selected_icon=Icons.COTTAGE, label='Home',
                ),
                NavigationRailDestination(
                    icon=Icons.PERM_CONTACT_CALENDAR_OUTLINED, selected_icon=Icons.PERM_CONTACT_CALENDAR, label='Clientes'
                ),
                NavigationRailDestination(
                    icon=Icons.PERSON_OUTLINED, selected_icon=Icons.PERSON_ROUNDED, label='Usuários'
                ),
                NavigationRailDestination(
                    icon=Icons.INVENTORY_2_OUTLINED, selected_icon=Icons.INVENTORY, label='Produtos'
                ),
                NavigationRailDestination(
                    icon=Icons.SHOPPING_CART_OUTLINED, selected_icon=Icons.SHOPPING_CART, label='Vendas'
                ),
                # NavigationRailDestination(
                #     icon=Icons.SETTINGS_OUTLINED, selected_icon_content=Icon(Icons.SETTINGS), label='Configurações',
                # ),
            ],
            trailing=IconButton(icon=Icons.SETTINGS, on_click=self.show_config_page),
            on_change=self.nav_clicked,
        )  
        self.cont.content = self.nnrail
        
        # Configurar o Container diretamente
        self.content = self.cont

    def menu_clicked(self, e):
        self.nnrail.extended = not self.nnrail.extended        
        self.update()

    def nav_clicked(self, e):
        if e.control.selected_index == 0:            
            self.page.go("/home")
            self.route.bar.set_title('Pagina Inicial')
            self.route.page.update()
            self.update()
            return
        elif e.control.selected_index == 1:
            self.page.go("/customers")
            self.route.bar.set_title('Clientes')
            self.route.page.update()
            self.update()
            return
        elif e.control.selected_index == 2:            
            self.page.go("/users")
            self.route.bar.set_title('Controle de Usuários')
            self.route.page.update()
            self.update()
            return
        elif e.control.selected_index == 3:            
            self.page.go("/products")
            self.route.bar.set_title('Produtos')
            self.route.page.update()
            self.update()
            return
        elif e.control.selected_index == 4:
            self.page.go("/sales")
            self.route.bar.set_title('Vendas')
            self.route.page.update()
            self.update()

    def show_config_page(self, e):
        dialog = SetGeneralConfig(self.route)
        self.route.page.dialog = dialog
        dialog.open = True
        self.route.page.update()

