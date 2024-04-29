import flet as ft


# Definição de estudos e atributos da classe Header

header_style: dict[str,any] = {
    "height":60,
    "bgcolor": "#081D33",
    "border_radius": ft.border_radius.only(top_left=15, top_right=15),
    "padding": ft.padding.only(left=15,right=15)
}


#Método para criar e retorn um textfield

def search_field(function:callable):
    return ft.TextField(
        border_color=ft.colors.BLACK,
        height=20,
        text_size=14,
        content_padding=0,
        cursor_color=ft.colors.WHITE,
        cursor_width=1,
        color=ft.colors.BLACK,
        hint_text="Procurar",
        on_change=function
    )
#  Metodo par aadiacanar um container para o search_+field

def search_bar(control: ft.TextField):
    return ft.Container(
        width=350,
        bgcolor=ft.colors.WHITE10,
        border_radius=6,
        opacity=0,
        animate_opacity=300,
        padding=8,
        content=ft.Row(
            spacing=10,
            vertical_alignment="center",
            controls=[
                ft.Icon(
                    name=ft.icons.SEARCH_ROUNDED,
                    size=17,
                    opacity=0.85,
                ),
                control,
            ]
        )
    )

#Definir a classe falar Headr

class Headr(ft.Container):
    def __init__(self):
        super().__init__()

        #Criar um textflit para procurar

        self.search_value: ft.TextField = search_field(None)

        #Cria uma caixa de pesquisa

        self.search: ft.Container = search_bar(self.search_value)

        #Define outros atributos


###############
'''
<iframe width="949" height="534" src="https://www.youtube.com/embed/Xl7BXURZ_HI" title="Python Tutorial DataTable Using Flet" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
'''



def main (page:ft.Page) -> None:

    page.bgcolor = "#fdfdfd"

    page.add(
        ft.Column(
            expand=True,
            controls=[
                #header ...
                ft.Divider(height=2, color="transparent"),
                #form ...
                ft.Column(
                    scroll="Hidden",
                    expand=True,
                    controls=[ft.Row(controls=[])] # Tabela Data table
                )
            ]
        )
    )

    page.update()

ft.app(target=main)