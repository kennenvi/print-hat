from labels.chapeus import Label, PPLALabelChapeu
from printer_service import PrinterService
from copy import deepcopy
from itertools import zip_longest


class PrintHatService():
    @staticmethod
    def print_labels(labels: list, qtd_pilha, printer) -> None:
        labels_label = [Label(*label) for label in labels]
        organized_labels = PrintHatService._organize_labels(labels_label)
        # print('org', organized_labels)
        ppla_items = PrintHatService._build_ppla_items(organized_labels)
        # print('ppla_items len', len(ppla_items))
        # print('ppla_items', ppla_items)

        PrinterService.print_labels(ppla_items, printer)

    @staticmethod
    def calculate_mods(cor, tamanho, aba, lote, qtd, qtd_pilha) -> list[Label]:
        label = Label(cor, tamanho, aba, lote, qtd)
        qtd_pilha = int(qtd_pilha)
        qtd = int(label.qtd)
        qtd_pilha = int(qtd_pilha)
        # print(f'qtd inicial == {qtd}')
        label.qtd = str(qtd_pilha)
        # print(f'qtd inicial == {qtd}')

        quocient, reminder = divmod(qtd, qtd_pilha)
        # print('quociente', quocient)
        # print('reminder', reminder)

        labels: list[Label] = []
        for _ in range(quocient):
            labels.append(label)
        if reminder:
            reminder_label = deepcopy(label)
            reminder_label.qtd = str(reminder)
            labels.append(reminder_label)

        return labels 

    @staticmethod
    def _organize_labels(labels, n=2, fillment=None) -> list[tuple]:
        args = [iter(labels)] * n
        return [tuple(grupo) for grupo in zip_longest(*args, fillvalue=fillment)]

    @staticmethod
    def _build_ppla_items(labels: list[tuple]):
        return [PPLALabelChapeu(label1, label2) for label1, label2 in labels]


if __name__ == '__main__':
    cor='1'
    tamanho='1'
    aba='1'
    lote='1'
    qtd='12'
    labels = [cor, tamanho, aba, lote, qtd]
    qtd_pilha='10'
    printer='ARGOX_OS-214_plus_PPLA_203dpi'
    PrintHatService.print_labels(labels, qtd_pilha, printer)
