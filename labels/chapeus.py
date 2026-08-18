from functools import partial

from ppla import PPLAItem
from utils import remove_acentos

initial_line = 238
ppla_descricao_partial = partial(PPLAItem, y_axis=10, x_axis=200)
ppla_ref_partial = partial(PPLAItem, y_axis=52, x_axis=initial_line)
ppla_tam_partial = partial(PPLAItem, y_axis=52, x_axis=initial_line+18)
ppla_cor_partial = partial(PPLAItem, y_axis=52, x_axis=initial_line+36)
bar_code_partial = partial(PPLAItem, y_axis=10, x_axis=205, alignment=1, font='F', multh=2, multv=2, subtype_font=30)


class PPLACintoItemFactory:
    def __init__(self, descricao: str, ref: str, tam: str, cor: str, bar_code: str) -> None:
        """Factory to create PPLA items for a label."""
        self.descricao = ppla_descricao_partial(text=descricao[:20])
        self.ref = ppla_ref_partial(text=f'REF {ref}')
        self.tam = ppla_tam_partial(text=tam)
        self.cor = ppla_cor_partial(text=remove_acentos(cor))
        self.bar_code = bar_code_partial(text=bar_code)
    
    def render(self) -> bytes:
        return (
            self.descricao.render() +
            self.ref.render() +
            self.tam.render() +
            self.cor.render() +
            self.bar_code.render()
        )
