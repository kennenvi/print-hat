import subprocess
from ppla import PPLARenderer


DEFAULT_PRINTER = "ARGOX_OS-214_plus_PPLA_203dpi"

class PrinterService():

    @staticmethod
    def print_labels(labels):
        for label in PrinterService.render_labels(labels):
            PrinterService.send_to_printer(label)

    @staticmethod
    def send_to_printer(data: bytes, printer: str = DEFAULT_PRINTER) -> None:
        subprocess.run(
            ["lp", "-d", printer, "-o", "raw"],
            input=data,
            check=True
        )

    @staticmethod
    def render_labels(labels):
        for label in labels:
            renderer = PPLARenderer('teste')
            yield renderer.render_item(label)

