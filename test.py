import subprocess
from ppla import PPLAItem, PPLARenderer


def imprimir_ppla(dados: bytes, impressora: str = "ARGOX_OS-214_plus_PPLA_203dpi") -> None:
    subprocess.run(
        ["lp", "-d", impressora, "-o", "raw"],
        input=dados,
        check=True
    )

# Medidas corretas encontradas (preservar)
# cor = PPLAItem(x_axis=20, y_axis=10, text='Preto', alignment=1, font=3)
# tamanho = PPLAItem(x_axis=20, y_axis=97, text='Preto', alignment=1, font=3)
# aba = PPLAItem(x_axis=141, y_axis=10, text='A10', alignment=1, font=3)
# lote = PPLAItem(x_axis=141, y_axis=97, text='1427', alignment=1, font=3)
# qtd = PPLAItem(x_axis=75, y_axis=50, text='250 un', alignment=1, font=3)

LEFT_MARGIN = 15
BOTTOM_MARGIN = 5
HEIGHT=115 # Altura da etiqueta em dots
LENGTH=165 # Largura de uma célula
# MM_TO_DOT=4.125 # Valor de mm para dot
MM_TO_DOT=3.85 # Valor de mm para dot
SEP_LENGTH=MM_TO_DOT * 3 # Valor da separação da etiquetas 3mm para dot
LABEL_SEP=int(round(44 * MM_TO_DOT, 1)) # Distancia entre a primeiro e a segunda etiqueta

def adjust_x_axix(x_value: int, label_sep: int = LABEL_SEP) -> int:
        return x_value + label_sep

# First Label
cor = PPLAItem(x_axis=LEFT_MARGIN, y_axis=BOTTOM_MARGIN, text='Preto', alignment=1, font=3)
tamanho = PPLAItem(x_axis=LEFT_MARGIN, y_axis=97, text='GG', alignment=1, font=3)
aba = PPLAItem(x_axis=141, y_axis=BOTTOM_MARGIN, text='A10', alignment=1, font=3)
lote = PPLAItem(x_axis=135, y_axis=97, text='1427', alignment=1, font=3)
qtd = PPLAItem(x_axis=66, y_axis=50, text='250 un', alignment=1, font=3)

# Second Label
cor_2 = PPLAItem(x_axis=adjust_x_axix(LEFT_MARGIN), y_axis=BOTTOM_MARGIN, text='Preto', alignment=1, font=3)
tamanho_2 = PPLAItem(x_axis=adjust_x_axix(LEFT_MARGIN), y_axis=97, text='GG', alignment=1, font=3)
aba_2 = PPLAItem(x_axis=adjust_x_axix(141), y_axis=BOTTOM_MARGIN, text='A10', alignment=1, font=3)
lote_2 = PPLAItem(x_axis=adjust_x_axix(135), y_axis=97, text='1427', alignment=1, font=3)
qtd_2 = PPLAItem(x_axis=adjust_x_axix(66), y_axis=50, text='250 un', alignment=1, font=3)

# itens = [cor, tamanho, aba, lote, qtd, cor_2, tamanho_2, aba_2, lote_2, qtd_2]
from labels.chapeus import label_chapeu
itens = [label_chapeu]
renderer = PPLARenderer('teste')
for item in itens:
    renderer.add_item(item)
# dados = (
#         # PPLARenderer.render_item(cor) + 
#         # PPLARenderer.render_item(tamanho)
#         # PPLARenderer.render_item(aba)
#         # PPLARenderer.render_item(lote)
#         PPLARenderer.render_item(qtd)
# )
dados = renderer.render_all()
print(dados)
imprimir_ppla(dados)
