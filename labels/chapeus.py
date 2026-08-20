from functools import partial
from copy import deepcopy
from typing import TypeVar
from dataclasses import dataclass

from ppla import PPLAItem
from utils import remove_acentos


LEFT_MARGIN = 15
BOTTOM_MARGIN = 5
HEIGHT=115 # Altura da etiqueta em dots
LENGTH=165 # Largura de uma célula
# MM_TO_DOT=4.125 # Valor de mm para dot
MM_TO_DOT=3.85 # Valor de mm para dot
SEP_LENGTH=MM_TO_DOT * 3 # Valor da separação da etiquetas 3mm para dot
LABEL_SEP=int(round(44 * MM_TO_DOT, 1)) # Distancia entre a primeiro e a segunda etiqueta

def adjust_x_axis(x_value: int, label_sep: int = LABEL_SEP) -> int:
        return x_value + label_sep

class PPLAItemChapeu(PPLAItem):
    def __init__(self, y_axis: int, x_axis: int, text: str, alignment: int | str = 1, font: str | int = 3, multh: int = 1, multv: int = 1, subtype_font: int = 0) -> None:
         super().__init__(y_axis, x_axis, text, alignment, font, multh, multv, subtype_font)

@dataclass
class Label:
    cor: str
    tamanho: str
    aba: str
    lote: str
    qtd: str

# Labels
ppla_cor_partial = partial(PPLAItemChapeu, x_axis=LEFT_MARGIN, y_axis=BOTTOM_MARGIN)
ppla_tamanho_partial = partial(PPLAItemChapeu, x_axis=LEFT_MARGIN, y_axis=97)
ppla_aba_partial = partial(PPLAItemChapeu, x_axis=141, y_axis=BOTTOM_MARGIN)
ppla_lote_partial = partial(PPLAItemChapeu, x_axis=135, y_axis=97)
ppla_qtd_partial = partial(PPLAItemChapeu, x_axis=66, y_axis=50)

class PPLALabelChapeu:
    def __init__(self, label1: Label, label2: None | Label = None) -> None:
        """Factory to create PPLA items for a label."""
        self.items: list[PPLAItem] = [
            ppla_cor_partial(text=remove_acentos(label1.cor)),
            ppla_tamanho_partial(text=label1.tamanho),
            ppla_aba_partial(text=label1.aba),
            ppla_lote_partial(text=label1.lote),
            ppla_qtd_partial(text=f'{label1.qtd} un'),
        ]

        if not label2:
            return

        self.items.extend([
            self.adjust_partial(ppla_cor_partial)(text=remove_acentos(label1.cor)),
            self.adjust_partial(ppla_tamanho_partial)(text=label1.tamanho),
            self.adjust_partial(ppla_aba_partial)(text=label1.aba),
            self.adjust_partial(ppla_lote_partial)(text=label1.lote),
            self.adjust_partial(ppla_qtd_partial)(text=f'{label1.qtd} un'),
        ])

    @staticmethod
    def adjust_partial(item: partial) -> partial:
        new_keywords = {k:(adjust_x_axis(v) if k=='x_axis' else v) for k,v in item.keywords.items()}
        new_partial = partial(item.func, **new_keywords)
        return new_partial

    def render(self) -> bytes:
        res = b''
        for item in self.items:
            res += item.render()
        return res

label1 = Label(
    cor='Preto', 
    tamanho='GG',
    aba='A10',
    lote='1423',
    qtd='120'
)
label2 = Label(
    cor='Preto', 
    tamanho='GG',
    aba='A10',
    lote='1423',
    qtd='120'
)
label2 = None 
label_chapeu = PPLALabelChapeu(label1, label2)

