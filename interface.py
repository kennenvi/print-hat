import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from typing import TypeVar, Callable
from printer_service import PrinterService
from service import PrintHatService


T = TypeVar('T', bound=tk.Widget)

class Application:
    font = ("Calibri", 10)

    def __init__(self, master: tk.Tk) -> None:
        self.master = master
        self.data = None

        self.main_frame = tk.Frame(self.master, padx=20, pady=20)
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.grid()

        # Input widgets
        self.widget_lote = self.create_entry_widget(self.main_frame, row=0, column=0, pady=10) 
        self.input_lote = self.create_input_component(self.widget_lote, 'Lote')

        self.widget_aba = self.create_entry_widget(self.main_frame, row=0, column=1, pady=10) 
        self.input_aba = self.create_input_component(self.widget_aba, 'Aba')

        self.widget_tamanho = self.create_entry_widget(self.main_frame, row=0, column=2, pady=10) 
        self.input_tamanho = self.create_input_component(self.widget_tamanho, 'Tamanho')

        self.widget_cor = self.create_entry_widget(
                self.main_frame, row=0, column=3, pady=10) 
        self.input_cor = self.create_input_component(self.widget_cor, 'Cor')

        self.widget_qtd = self.create_entry_widget(self.main_frame,
                                                 row=1, column=0)
        self.input_qtd = self.create_input_component(self.widget_qtd, 'Quantidade')

        self.widget_qtd_pilha = self.create_entry_widget(
                self.main_frame, row=1, column=1)
        self.input_qtd_pilha = self.create_input_component(self.widget_qtd_pilha, 'Quantidade por pilha')
        self.input_qtd_pilha.insert(0, '10')

        self.widget_printer = self.create_entry_widget(
                self.main_frame, row=1, column=2, columnspan=2)
        printers = PrinterService.list_printers() + ['dadsa', 't2']
        self.combo_printer = self.create_input_component(self.widget_printer, 'Impressora', ttk.Combobox) 
        self.combo_printer['values'] = printers
        self.combo_printer['state'] = 'readonly'
        self.combo_printer.current(0)

        self.load_data_button = tk.Button(self.main_frame, text="Imprimir", font=self.font, padx=10,
                                            command=self.print_label) 
        self.load_data_button.grid(row=2, column=3, sticky='se')

    def print_label(self) -> None:
        input_widgets = [
            self.input_cor,
            self.input_tamanho,
            self.input_aba,
            self.input_lote,
            self.input_qtd,
            self.input_qtd_pilha,
            self.combo_printer
        ]
        values = [w_input.get() for w_input in input_widgets]
        print(values)

        if not all(values):
            messagebox.showinfo('Erro', 'É necessário preencheer todos os campos')
            return
        PrintHatService.print_labels(*values)

    def create_entry_widget(self, parent: tk.Frame, row: int, column: int, **kwargs) -> tk.Frame:
        widget = tk.Frame(parent)
        widget_args = {'row': row, 'column': column, 'sticky': 'nswe', **kwargs}
        widget.grid(**widget_args)
        return widget

    def create_input_component(self, parent: tk.Frame, name: str, tk_component: Callable[..., T] = tk.Entry) -> T:
        parent.columnconfigure(1, weight=1)
        parent.rowconfigure(0, weight=1)

        input_label = tk.Label(parent, text=name, font=self.font)
        input_label.grid(row=0, column=0, sticky='w', padx=10)

        input_entry = tk_component(parent, font=self.font)
        input_entry.grid(row=0, column=1, sticky='nswe')

        return input_entry

