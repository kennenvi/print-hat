import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from typing import TypeVar, Callable
from printer_service import PrinterService
from service import PrintHatService
from functools import partial
from dataclasses import asdict


T = TypeVar('T', bound=tk.Widget)
QTD_MAXIMO_ETIQUETAS = 100_000

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

        # Wrapper widgets
        self.widget_input_fields = tk.Frame(self.main_frame)
        self.widget_input_fields.grid(row=0, column=0)
        self.widget_table_components = tk.Frame(self.main_frame)
        self.widget_table_components.grid(row=1, column=0)

        # Input widgets
        self.widget_lote = self.create_entry_widget(self.widget_input_fields, row=0, column=0, pady=10) 
        self.input_lote = self.create_input_component(self.widget_lote, 'Lote')

        self.widget_aba = self.create_entry_widget(self.widget_input_fields, row=0, column=1, pady=10) 
        self.input_aba = self.create_input_component(self.widget_aba, 'Aba')

        self.widget_tamanho = self.create_entry_widget(self.widget_input_fields, row=0, column=2, pady=10) 
        self.input_tamanho = self.create_input_component(self.widget_tamanho, 'Tamanho')

        self.widget_cor = self.create_entry_widget(
                self.widget_input_fields, row=0, column=3, pady=10) 
        self.input_cor = self.create_input_component(self.widget_cor, 'Cor')

        self.widget_qtd = self.create_entry_widget(self.widget_input_fields,
                                                 row=1, column=0)
        self.input_qtd = self.create_input_component(self.widget_qtd, 'Quantidade')

        self.widget_qtd_pilha = self.create_entry_widget(
                self.widget_input_fields, row=1, column=1)
        self.input_qtd_pilha = self.create_input_component(self.widget_qtd_pilha, 'Quantidade por pilha')
        self.input_qtd_pilha.insert(0, '10')

        self.widget_printer = self.create_entry_widget(
                self.widget_input_fields, row=1, column=2, columnspan=2)
        printers = PrinterService.list_printers() + ['dadsa', 't2']
        self.combo_printer = self.create_input_component(self.widget_printer, 'Impressora', ttk.Combobox) 
        self.combo_printer['values'] = printers
        self.combo_printer['state'] = 'readonly'
        self.combo_printer.current(0)

        self.load_data_button = tk.Button(self.widget_input_fields, text="Adicionar", font=self.font, padx=10,
                                            command=self.add_label_to_table) 
        self.load_data_button.grid(row=2, column=3, sticky='se')

        self.input_widgets = [
            self.input_cor,
            self.input_tamanho,
            self.input_aba,
            self.input_lote,
            self.input_qtd,
        ]
        # table widget
        self.widget_table = tk.Frame(self.main_frame)
        self.widget_table.grid(row=3, column=0) 
        self.tree_table = self.render_order_table(self.widget_table, 'Tabela')

    def print_label(self) -> None:
        tree_items = self.tree_table.get_children()
        row_values = [self.tree_table.item(item_id, 'values') for item_id in tree_items]
        qtd = self.input_qtd.get()
        qtd_pilha = self.input_qtd_pilha.get()
        printer = self.combo_printer.get()
        # print('row_values', row_values)

        if not row_values:
            messagebox.showinfo('Erro', 'É necessário inserir pelo menos um item')
            return
        if int(qtd) > 100_000:
            messagebox.showinfo('Erro', 'Número máximo de etiquetas é 100.000')
            return

        PrintHatService.print_labels(row_values, qtd_pilha, printer)

    def add_label_to_table(self) -> None:
        # validation
        qtd = self.input_qtd.get()
        try:
            int(qtd)
        except ValueError:
            messagebox.showerror('Erro', f'"Quantidade" precisa ser um número e não: "{qtd}"')
            return
        if int(qtd) > QTD_MAXIMO_ETIQUETAS:
            messagebox.showerror('Erro', f'Número máximo de etiquetas é {QTD_MAXIMO_ETIQUETAS}')
            return
        qtd_pilha = self.input_qtd_pilha.get()
        try:
            int(qtd_pilha)
        except ValueError:
            messagebox.showerror('Erro', f'"Quantidade por pilha" precisa ser um número e não: "{qtd_pilha}"')
            return

        values = [w_input.get() for w_input in self.input_widgets]
        # print(values)
        values.append(qtd_pilha)
        labels = PrintHatService.calculate_mods(*values)
        values_calculated = [asdict(l) for l in labels]
        # print(values_calculated)

        if not all(values):
            messagebox.showinfo('Erro', 'É necessário preencheer todos os campos')
            return

        for label in values_calculated:
            label_values = list(label.values())
            self.tree_table.insert('', tk.END, values=label_values)

    def render_order_table(self, parent: tk.Frame, printer: str) -> ttk.Treeview:
        col_names = ['Lote', 'Aba', 'Cor', 'Tamanho', 'Quantidade']
        cols_width = [100, 100, 100, 100, 100]
        tree = ttk.Treeview(parent, columns=col_names, show='headings')
        for col, col_width in zip(col_names, cols_width):
            tree.column(col, anchor='center')
            tree.heading(col, anchor='center', text=col)

        tree.grid(row=2, column=0, sticky='nsew', pady=10, padx=10)

        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set) # type: ignore
        scrollbar.grid(row=2, column=1, sticky='ns')

        delete_button = tk.Button(
            parent, text="Excluir Etiqueta", font=self.font, padx=10,
            command=partial(self.delete_label_from_table, tree)
        )
        delete_button.grid(row=3, column=0, sticky="w", pady=10, padx=10)

        print_button = tk.Button(parent, text="Imprimir", font=self.font, padx=10, command=self.print_label)
        print_button.grid(row=3, column=0, sticky="e", pady=10, padx=10)

        return tree

    def delete_label_from_table(self, tree: ttk.Treeview) -> None:
        selected = tree.selection()
        if not selected:
            messagebox.showinfo('Erro', 'Selecione uma linha para excluir')
            return
        for item_id in selected:
            tree.delete(item_id)

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

