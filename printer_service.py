import subprocess
import platform
from typing import Generator
from ppla import PPLARenderer


DEFAULT_PRINTER = "ARGOX_OS-214_plus_PPLA_203dpi"
platform_os = platform.system()

class PrinterService():

    @staticmethod
    def print_labels(labels, printer: str | None = None):
        for label in PrinterService.render_labels(labels):
            PrinterService.send_to_printer(label, printer or DEFAULT_PRINTER)

    @staticmethod
    def send_to_printer(data: bytes, printer: str = DEFAULT_PRINTER) -> None:
        if platform_os == 'Linux':
            PrinterService.send_to_printer_posix(data, printer)
            return
        if platform_os == 'Windows':
            PrinterService.send_to_printer_win(data, printer)
            return
        raise NotImplementedError(f'Não existem método de impressão para {platform_os}')


    @staticmethod
    def send_to_printer_posix(data: bytes, printer: str = DEFAULT_PRINTER) -> None:
        subprocess.run(
            ["lp", "-d", printer, "-o", "raw"],
            input=data,
            check=True
        )

    @staticmethod
    def send_to_printer_win(data: bytes, printer: str = DEFAULT_PRINTER) -> None:
        import win32print

        hPrinter = win32print.OpenPrinter(printer)
        try:
            hJob = win32print.StartDocPrinter(hPrinter, 1, ("Etiqueta Teste PPLA", None, "RAW"))
            win32print.StartPagePrinter(hPrinter)
            win32print.WritePrinter(hPrinter, data)
            win32print.EndPagePrinter(hPrinter)
            win32print.EndDocPrinter(hPrinter)
        finally:
            win32print.ClosePrinter(hPrinter)

    @staticmethod
    def render_labels(labels) -> Generator[bytes]:
        for label in labels:
            renderer = PPLARenderer('teste')
            yield renderer.render_item(label)

    @staticmethod
    def list_printers_posix() -> list[str]:
        result = subprocess.run(
            ["lpstat", "-p"],
            capture_output=True,
            text=True,
            check=True
        )

        printers_names = []
        for line in result.stdout.splitlines():
          if line.startswith("printer "):
              # "printer NOME is idle. ..." -> pega o 2º token
              printers_names.append(line.split()[1])
        return printers_names
    @staticmethod
    def list_printers_win() -> list[str]:
        """
        Lista todas as impressoras disponíveis no sistema.
        """
        import win32print
        printers = [printer[2] for printer in win32print.EnumPrinters(2)]
        return printers

    @staticmethod
    def list_printers() -> list[str]:
        if platform_os == 'Linux':
            printers_names = PrinterService.list_printers_posix()
            return printers_names
        if platform_os == 'Windows':
            printers_names = PrinterService.list_printers_win()
            return printers_names
        raise NotImplementedError(f'Não existe listagem de impressoras para {platform_os}')
