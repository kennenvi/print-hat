import subprocess
import platform
from ppla import PPLARenderer


DEFAULT_PRINTER = "ARGOX_OS-214_plus_PPLA_203dpi"
platform_os = platform.system()


class PrinterService():

    @staticmethod
    def print_labels(labels):
        for label in PrinterService.render_labels(labels):
            PrinterService.send_to_printer(label)

    @staticmethod
    def send_to_printer(data: bytes, printer: str = DEFAULT_PRINTER) -> None:
        if platform_os == 'Linux':
            PrinterService.send_to_printer_posix(data, printer)
            return
        if platform_os == 'Windows':
            PrinterService.send_to_printer_win(data, printer)
            return
        raise NotImplementedError('Não existem método de imperssão para outros OS')

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
    def render_labels(labels):
        for label in labels:
            renderer = PPLARenderer('teste')
            yield renderer.render_item(label)

