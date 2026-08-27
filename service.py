from labels.chapeus import Label, PPLALabelChapeu
from printer_service import PrinterService
from copy import deepcopy



class PrintHatService():
    @staticmethod
    def print_labels(cor, tamanho, aba, lote, qtd, qtd_pilha, printer) -> None:
        label = Label(cor, tamanho, aba, lote, qtd)
        labels, label_mod = PrintHatService.calculate_mods(label, qtd_pilha)
        print(len(labels))

        res_labels = PrintHatService._verify_mod(label_mod, label)
        labels.extend(res_labels)

        PrinterService.print_labels(labels, printer)

    @staticmethod
    def calculate_mods(label, qtd_pilha) -> tuple[list[PPLALabelChapeu], int]:
        qtd = int(label.qtd)
        qtd_pilha = int(qtd_pilha)
        print(f'qtd inicial == {qtd}')
        label.qtd = qtd_pilha
        print(f'qtd inicial == {qtd}')

        label_mod = qtd % qtd_pilha
        qtd_label_10 = qtd - label_mod

        print(f'qtd_label_10 == {qtd_label_10}')
        print(f'label_mod == {label_mod}')

        labels = []
        for _ in range(qtd_label_10 // 2):
            labels.append(PPLALabelChapeu(label1=label, label2=label))
        if qtd_label_10 % 2 != 0:
            labels.append(PPLALabelChapeu(label1=label))

        return labels, label_mod

    @staticmethod
    def _verify_mod(qtd_labels: int, label: Label) -> list[PPLALabelChapeu]:
        label_mod = qtd_labels % 2
        label_for_rest = deepcopy(label)
        label_for_rest.qtd = str(qtd_labels)
        print('=================')
        print(f'label_mod == {label_mod}')
        if qtd_labels == 1:
            print('qtd_labels == 1')
            labels = [PPLALabelChapeu(label1=label_for_rest)]
        elif qtd_labels == 2:
            print('qtd_labels == 2')
            labels = [PPLALabelChapeu(label1=label_for_rest, label2=label_for_rest)]
        else:
            print('entrou no else')
            labels = [
                PPLALabelChapeu(label1=label_for_rest, label2=label_for_rest)
                for _ in range(qtd_labels // 2)
            ]
            if label_mod != 0:
                print('Entrou no adicional')
                labels.append(PPLALabelChapeu(label1=label_for_rest))
        print(f'len2 == {len(labels)}')
        return labels


if __name__ == '__main__':
    label = Label(cor='1', tamanho='1', aba='1', lote='1', qtd='12')
    PrintHatService.print_labels(label)
