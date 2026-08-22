from tkinter import ttk
import tkinter as tk
from tkinter import filedialog, messagebox
from functools import partial

# from ppla import PPLABuilder
# from utils.utils import populate_builder, print_builder
# from loaddata.loaddata import load_data
# from config import PRINTER_NAME


def list_printers():
    return ['teste']

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
        self.widget_lote = tk.Frame(self.widget_input_fields)
        self.widget_lote.grid(row=0, column=0) 
        self.input_lote = self.create_entry_field(self.widget_lote, 'Lote')

        self.widget_aba = tk.Frame(self.widget_input_fields)
        self.widget_aba.grid(row=0, column=1)
        self.input_aba = self.create_entry_field(self.widget_aba, 'Aba')

        self.widget_tamanho = tk.Frame(self.widget_input_fields)
        self.widget_tamanho.grid(row=0, column=2)
        self.input_tamanho = self.create_entry_field(self.widget_tamanho, 'Tamanho')

        self.widget_cor = tk.Frame(self.widget_input_fields)
        self.widget_cor.grid(row=1, column=0)
        self.input_cor = self.create_entry_field(self.widget_cor, 'Cor')

        self.widget_qtd = tk.Frame(self.widget_input_fields)
        self.widget_qtd.grid(row=1, column=1)
        self.input_qtd = self.create_entry_field(self.widget_qtd, 'Quantidade')

        self.input_widgets = [
            self.input_lote,
            self.input_aba,
            self.input_tamanho,
            self.input_cor,
            self.input_qtd
        ]

        self.load_data_button = tk.Button(self.widget_input_fields, text="Adicionar Etiqueta", font=self.font, padx=10, command=self.add_label_to_table) 
        self.load_data_button.grid(row=1, column=2, sticky="e", pady=20)

        # table widget
        self.widget_table = tk.Frame(self.widget_table_components)
        self.widget_table.grid(row=2, columnspan=3)
        self.tree_table = self.render_order_table(self.widget_table, 'teste')

    def add_label_to_table(self) -> None:
        values = [w_input.get() for w_input in self.input_widgets]
        print(values)

        if not all(values):
            messagebox.showinfo('Erro', 'É necessário preencheer todos os campos')
            return

        self.tree_table.insert('', tk.END, values=values)

    def render_order_table(self, parent: tk.Frame, printer: str) -> ttk.Treeview:
        col_names = ['Lote', 'Aba', 'Cor', 'Tamanho', 'Quantidade']
        cols_width = [100, 100, 100, 100, 100]
        tree = ttk.Treeview(parent, columns=col_names, show='headings')
        for col, col_width in zip(col_names, cols_width):
            tree.heading(col, text=col)

        tree.grid(row=2, column=0, sticky='nsew', pady=10, padx=10)

        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set) # type: ignore
        scrollbar.grid(row=2, column=1, sticky='ns')

        delete_button = tk.Button(
            parent, text="Excluir Etiqueta", font=self.font, padx=10,
            command=partial(self.delete_label_from_table, tree)
        )
        delete_button.grid(row=3, column=0, sticky="w", pady=10, padx=10)

        print_button = tk.Button(parent, text="Imprimir", font=self.font, padx=10)
        print_button.grid(row=3, column=0, sticky="e", pady=10, padx=10)

        return tree

    def delete_label_from_table(self, tree: ttk.Treeview) -> None:
        selected = tree.selection()
        if not selected:
            messagebox.showinfo('Erro', 'Selecione uma linha para excluir')
            return
        for item_id in selected:
            tree.delete(item_id)
        # print_button['command'] = partial(self.print_labels, printer, selected_data)
    #
    # def print_labels(self, printer, df) -> None:
    #     builder = PPLABuilder(printer)
    #     builder = populate_builder(builder, df)
    #     print_builder(builder, printer)
    #

    def create_entry_field(self, parent: tk.Frame, name: str) -> tk.Entry:
        input_label = tk.Label(parent, text=name, font=self.font, width=10)
        input_label.grid(row=0, column=0, sticky='nsew', padx=10)

        input_entry = tk.Entry(parent, font=self.font)
        input_entry.grid(row=0, column=1, sticky='ew')

        return input_entry

    def create_file_button(self, parent: tk.Frame, name: str) -> tk.Entry:
        input_file_label = tk.Label(parent, text=name, font=self.font, padx=10)
        input_file_label.grid(row=0, column=0)

        input_file_entry = tk.Entry(parent, font=self.font, width=50)
        input_file_entry.grid(row=2, column=0)
        input_file_button = tk.Button(parent, text="Selecionar Arquivo", font=self.font)
        input_file_button['command'] = partial(self.upload_file, input_file_entry)
        input_file_button.grid(row=2, column=1)

        return input_file_entry

    def upload_file(self, entry_button: tk.Entry) -> None:
        file_path = filedialog.askopenfilename(
            title="Selecione o arquivo",
            filetypes=(("Arquivos Excel", "*.csv"),)
        )
        entry_button.delete(0, tk.END)
        entry_button.insert(0, file_path)

