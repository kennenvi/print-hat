class PPLAItem:
    def __init__(self, 
            y_axis: int, 
            x_axis: int,
            text: str,
            alignment: int|str=4,
            font: str|int=2, 
            multh: int=1, 
            multv: int=1, 
            subtype_font: int=0
        ) -> None:
        self.y_axis = str(y_axis).zfill(4)
        self.x_axis = str(x_axis).zfill(4)
        self.text = text
        self.alignment = alignment
        self.font = font
        self.multh = multh
        self.multv = multv
        self.subtype_font = str(subtype_font).zfill(3)

    def render(self) -> bytes:
        return f"{self.alignment}{self.font}{self.multh}{self.multv}{self.subtype_font}{self.y_axis}{self.x_axis}{self.text}\x03\n".encode('utf-8')

class PPLABuilder:
    def __init__(self, printer_name: str) -> None:
        self.printer_name: str = printer_name
        self.items: list[PPLAItem] = []

    def add_item(self, item: PPLAItem) -> None:
        self.items.append(item)

    def render_all(self) -> bytes:
        rendered_items = ''.join(item.render().decode('utf-8') for item in self.items)
        return f"\n\x02L\x03\nD11\x03\n{rendered_items}E\x03\n".encode('utf-8')
    
    def render(self, item: PPLAItem) -> bytes:
        return f"\n\x02L\x03\nD11\x03\n{item.render().decode('utf-8')}E\x03\n".encode('utf-8')

    def __iter__(self):
        for item in self.items:
            yield self.render(item)
