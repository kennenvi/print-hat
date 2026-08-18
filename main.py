import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from functools import partial

# from ppla import PPLABuilder
# from utils.utils import populate_builder, print_builder
# from loaddata.loaddata import load_data
# from config import PRINTER_NAME
# from utils.utils import list_printers


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

        self.widget2 = tk.Frame(self.main_frame)
        self.widget2.grid(row=0, column=0)
        self.product_entry = self.create_file_button(self.widget2, "Arquivos do Cadastro dos Produtos")

        self.widget3 = tk.Frame(self.main_frame)
        self.widget3.grid(row=1, column=0)
        self.order_entry = self.create_file_button(self.widget3, "Arquivo do Lote")

        # self.load_data_button = tk.Button(self.main_frame, text="Carregar dados", font=self.font, padx=10, command=self.prepare_load_data)
        # self.load_data_button.grid(row=2, column=0, sticky="e", pady=20)

    # def prepare_load_data(self) -> None:
    #     order_file = self.order_entry.get()
    #     products_file = self.product_entry.get()
    #     if not any([order_file, products_file]):
    #         message_level = tk.Toplevel(self.master, takefocus=True)
    #         tk.Label(message_level, text="É necessário selecionar todos os arquivos", font=self.font, padx=10, pady=10).grid()
    #         return
    #
    #     try:
    #         self.data = load_data(order_file, products_file)
    #     except Exception:
    #         message_level = tk.Toplevel(self.master, takefocus=True)
    #         message_text = 'Erro ao carregar os arquivos, por favor verifique os arquivos e tente novamente.'
    #         tk.Label(message_level, text=message_text, font=self.font, padx=10, pady=10).grid()
    #         return
    #
    #     self.render_order()
    #
    # def render_combo(self, parent: tk.Frame, text: str, codigos: list[str]) -> ttk.Combobox:
    #     label = tk.Label(parent, text=text, font=self.font, padx=10)
    #     label.grid(row=0, column=0)
    #     combo = ttk.Combobox(parent, values=codigos, width=30, font=self.font)
    #     combo.current(0)
    #     combo.grid(row=1, column=0)
    #
    #     return combo
    #
    # def render_order(self) -> None:
    #     order_level = tk.Toplevel(self.master, takefocus=True)
    #     order_level.title("Lote")
    #     order_level.grid()
    #
    #     # Combos
    #     combos_frame = tk.Frame(order_level)
    #     combos_frame.grid(row=0, column=0)
    #
    #     # Combo Printer
    #     combo_printer_frame = tk.Frame(combos_frame)
    #     combo_printer_frame.grid(row=0, column=1, padx=20, pady=10)
    #     combo_printer_text = "Selecione a impressora"
    #     combo_printer = self.render_combo(combo_printer_frame, combo_printer_text, list_printers())
    #
    #     # Combo Order
    #     combo_order_frame = tk.Frame(combos_frame)
    #     combo_order_frame.grid(row=0, column=0, padx=20, pady=10)
    #     codigos = self.data['codigo'].unique().tolist() if self.data is not None else []
    #     combo_order_text = "Selecione o código para imprimir"
    #     combo = self.render_combo(combo_order_frame, combo_order_text, codigos)
    #
    #     combo.bind("<<ComboboxSelected>>", lambda event: self.render_order_table(order_level, combo_printer.get(), int(combo.get())))
    #     combo_printer.bind("<<ComboboxSelected>>", lambda event: self.render_order_table(order_level, combo_printer.get(), int(combo.get())))
    #     self.render_order_table(order_level, combo_printer.get())
    #
    # def render_order_table(self, parent: tk.Toplevel, printer: str, cod: int|None = None) -> None:
    #     if self.data is None:
    #         return
    #
    #     if not cod:
    #         cod = self.data['codigo'].iloc[0]
    #
    #     selected_data = self.data[self.data['codigo'] == cod]
    #     selected_data = order_df(selected_data)
    #     selected_data_display = selected_data.drop(columns=['bar_code'])
    #     cols_to_group = ['codigo', 'descricao', 'tamanho', 'cor']
    #     selected_data_grouped = selected_data_display.groupby(cols_to_group).agg('count').reset_index()
    #     selected_data_grouped = selected_data_grouped.rename(columns={'id': 'quantidade'})
    #     selected_data_grouped = order_df(selected_data_grouped)
    #
    #     cols_width = [100, 300, 100, 100, 100]        
    #     tree = ttk.Treeview(parent, columns=list(selected_data_grouped.columns), show='headings')
    #     for col, col_width in zip(selected_data_grouped.columns, cols_width):
    #         tree.heading(col, text=col)
    #         tree.column(col, width=col_width)
    #
    #     for _, row in selected_data_grouped.iterrows():
    #         tree.insert('', tk.END, values=list(row))
    #
    #     tree.grid(row=2, column=0, sticky='nsew', pady=10, padx=10)
    #
    #     scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=tree.yview)
    #     tree.configure(yscroll=scrollbar.set) # type: ignore
    #     scrollbar.grid(row=2, column=1, sticky='ns')
    #
    #     print_button = tk.Button(parent, text="Imprimir", font=self.font, padx=10)
    #     print_button.grid(row=3, column=0, sticky="e", pady=10, padx=10)
    #     print_button['command'] = partial(self.print_labels, printer, selected_data)
    #
    # def print_labels(self, printer, df) -> None:
    #     builder = PPLABuilder(printer)
    #     builder = populate_builder(builder, df)
    #     print_builder(builder, printer)
    #
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

root = tk.Tk()
root.title("Impressão de Etiquetas")
app = Application(root)

root.mainloop()
