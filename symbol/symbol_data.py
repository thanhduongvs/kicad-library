import os
from dataclasses import dataclass, field
from typing import List, Dict, Optional

# ================= CÁC KIỂU DỮ LIỆU CƠ SỞ =================
@dataclass
class Position:
    x: float = 0.0
    y: float = 0.0
    angle: float = 0.0

@dataclass
class FontInfo:
    size_x: float = 1.27
    size_y: float = 1.27
    bold: bool = False
    italic: bool = False

@dataclass
class Effects:
    font: FontInfo = field(default_factory=FontInfo)
    justify: str = "left"
    hide: bool = False

@dataclass
class Stroke:
    width: float = 0.0
    type: str = "default"

@dataclass
class Fill:
    type: str = "none"

# ================= KIẾN TRÚC KẾ THỪA (CHUẨN KICAD C++) =================
@dataclass
class LibItem:
    unit: int = 1
    demorgan: int = 1

@dataclass
class LibShape(LibItem):
    stroke: Stroke = field(default_factory=Stroke)
    fill: Fill = field(default_factory=Fill)

@dataclass
class Rectangle(LibShape):
    start: Position = field(default_factory=Position)
    end: Position = field(default_factory=Position)

@dataclass
class Circle(LibShape):
    center: Position = field(default_factory=Position)
    radius: float = 0.0

@dataclass
class Arc(LibShape):
    start: Position = field(default_factory=Position)
    mid: Position = field(default_factory=Position)
    end: Position = field(default_factory=Position)

@dataclass
class Polyline(LibShape):
    points: List[Position] = field(default_factory=list)

@dataclass
class Bezier(LibShape):
    points: List[Position] = field(default_factory=list)

@dataclass
class LibText(LibItem):
    text: str = ""
    position: Position = field(default_factory=Position)
    effects: Effects = field(default_factory=Effects)

@dataclass
class TextBox(LibShape):
    text: str = ""
    position: Position = field(default_factory=Position)
    size_x: float = 0.0
    size_y: float = 0.0
    margins: List[float] = field(default_factory=lambda: [1.016, 1.016, 1.016, 1.016])
    effects: Effects = field(default_factory=Effects)

@dataclass
class PinAlternate:
    name: str
    electrical_type: str = "unspecified"
    style: str = "line"

@dataclass
class LibPin(LibItem):
    number: str = ""
    name: str = ""
    electrical_type: str = "passive"
    style: str = "line"
    length: float = 2.54
    position: Position = field(default_factory=Position)
    alternates: List[PinAlternate] = field(default_factory=list)

@dataclass
class LibField(LibItem):
    id: int = 0
    key: str = ""
    value: str = ""
    position: Position = field(default_factory=Position)
    effects: Effects = field(default_factory=Effects)
    show_name: bool = False
    do_not_autoplace: bool = False
    hide: bool = False

# ================= QUẢN LÝ THƯ VIỆN & PARSER =================
@dataclass
class LibMetadata:
    version: str = "20251024"
    generator: str = "kicad_symbol_editor"
    generator_version: str = "10.0"

@dataclass
class Symbol:
    name: str
    extends: str = ""
    exclude_from_sim: bool = False
    in_bom: bool = True
    on_board: bool = True
    in_pos_files: bool = True
    duplicate_pin_numbers_are_jumpers: bool = False
    embedded_fonts: bool = False
    
    properties: Dict[str, LibField] = field(default_factory=dict)
    draw_items: List[LibItem] = field(default_factory=list)

    @property
    def pins(self) -> List[LibPin]:
        return [i for i in self.draw_items if isinstance(i, LibPin)]

    def get_prop(self, key: str) -> str:
        return self.properties[key].value if key in self.properties else ""

    def set_prop(self, key: str, value: str = None, p_id: int = None, hide: bool = None, x: float = None, y: float = None, angle: float = None):
        if key in self.properties:
            p = self.properties[key]
            if value is not None: p.value = value
            if p_id is not None: p.id = p_id
            if hide is not None: p.hide = hide
            if x is not None: p.position.x = x
            if y is not None: p.position.y = y
            if angle is not None: p.position.angle = angle
        else:
            actual_value = value if value is not None else ""
            actual_p_id = p_id if p_id is not None else (max([p.id for p in self.properties.values()] + [3]) + 1)
            actual_hide = hide if hide is not None else False
            actual_x = x if x is not None else 0.0
            actual_y = y if y is not None else 0.0
            actual_angle = angle if angle is not None else 0.0
            
            self.properties[key] = LibField(
                id=actual_p_id, key=key, value=actual_value, 
                position=Position(actual_x, actual_y, actual_angle), 
                effects=Effects(), hide=actual_hide
            )

    def add_item(self, item: LibItem):
        self.draw_items.append(item)


class KiLibManager:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.metadata = LibMetadata()
        self.symbols: Dict[str, Symbol] = {}
        self._load_and_parse()

    def add_symbol(self, name: str) -> Symbol:
        if name in self.symbols: return self.symbols[name]
        sym = Symbol(name=name)
        sym.set_prop("Reference", "U", p_id=0, x=0, y=7.62)
        sym.set_prop("Value", name, p_id=1, x=0, y=5.08)
        sym.set_prop("Footprint", "", p_id=2, hide=True)
        sym.set_prop("Datasheet", "", p_id=3, hide=True)
        self.symbols[name] = sym
        return sym

    def get_symbol(self, name: str) -> Optional[Symbol]:
        return self.symbols.get(name)

    def save_to_file(self, output_filepath: str = None):
        from symbol_serializer import SymbolSerializer
        if output_filepath is None: output_filepath = self.filepath
        SymbolSerializer.save(self, output_filepath)

    def _load_and_parse(self):
        if not os.path.exists(self.filepath): return
        with open(self.filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        parsed_data = self._parse(self._tokenize(content))
        if not parsed_data: return

        for item in parsed_data[1:]:
            if not isinstance(item, list): continue
            if item[0] == 'version': self.metadata.version = item[1]
            elif item[0] == 'generator': self.metadata.generator = item[1]
            elif item[0] == 'generator_version': self.metadata.generator_version = item[1]
            elif item[0] == 'symbol': self._parse_symbol_item(item, parsed_data)

    def _parse_symbol_item(self, item, full_data):
        sym_name = item[1]
        if "_" in sym_name and sym_name.split("_")[-1].isdigit(): return 
        
        sym = Symbol(name=sym_name)
        prop_id = 4
        
        for sub in item[2:]:
            if not isinstance(sub, list): continue
            tag = sub[0]
            if tag == 'extends': sym.extends = sub[1]
            elif tag == 'exclude_from_sim': sym.exclude_from_sim = (sub[1] == 'yes')
            elif tag == 'in_bom': sym.in_bom = (sub[1] == 'yes')
            elif tag == 'on_board': sym.on_board = (sub[1] == 'yes')
            elif tag == 'in_pos_files': sym.in_pos_files = (sub[1] == 'yes')
            elif tag == 'duplicate_pin_numbers_are_jumpers': sym.duplicate_pin_numbers_are_jumpers = (sub[1] == 'yes')
            elif tag == 'embedded_fonts': sym.embedded_fonts = (sub[1] == 'yes')
            elif tag == 'property':
                k = sub[1]
                pid = {"Reference":0, "Value":1, "Footprint":2, "Datasheet":3}.get(k, prop_id)
                if pid == prop_id: prop_id += 1
                sym.properties[k] = self._parse_field(sub, pid)
            elif tag == 'symbol':
                block_name = sub[1]
                if block_name.startswith(sym_name + "_"):
                    try:
                        parts = block_name.replace(sym_name + "_", "").split("_")
                        u, d = int(parts[0]), int(parts[1])
                    except: u, d = 1, 1
                    self._parse_graphics_and_pins(sym, sub, u, d)

        # Hỗ trợ format KiCad cũ
        for block in full_data[1:]:
            if isinstance(block, list) and block[0] == 'symbol' and block[1].startswith(sym_name + "_"):
                try:
                    parts = block[1].replace(sym_name + "_", "").split("_")
                    u, d = int(parts[0]), int(parts[1])
                except: u, d = 1, 1
                self._parse_graphics_and_pins(sym, block, u, d)
        
        self.symbols[sym_name] = sym

    def _parse_field(self, node, pid):
        f = LibField(id=pid, key=node[1], value=node[2] if len(node)>2 and isinstance(node[2], str) else "")
        for attr in node[3:]:
            if not isinstance(attr, list): continue
            if attr[0] == 'at': f.position = Position(float(attr[1]), float(attr[2]), float(attr[3]) if len(attr)>3 else 0)
            elif attr[0] == 'hide': f.hide = (attr[1] == 'yes')
            elif attr[0] == 'show_name': f.show_name = (attr[1] == 'yes')
            elif attr[0] == 'do_not_autoplace': f.do_not_autoplace = (attr[1] == 'yes')
            elif attr[0] == 'effects': 
                self._parse_effects(f.effects, attr)
                if f.effects.hide:
                    f.hide = True
                    f.effects.hide = False
        return f

    def _parse_effects(self, eff: Effects, node):
        for attr in node[1:]:
            if not isinstance(attr, list): continue
            if attr[0] == 'justify': eff.justify = " ".join(attr[1:])
            elif attr[0] == 'hide': eff.hide = (attr[1] == 'yes')
            elif attr[0] == 'font':
                for font_attr in attr[1:]:
                    if isinstance(font_attr, list) and font_attr[0] == 'size':
                        eff.font.size_x = float(font_attr[1])
                        eff.font.size_y = float(font_attr[2])

    def _parse_stroke_fill(self, obj, node):
        for attr in node[1:]:
            if not isinstance(attr, list): continue
            if attr[0] == 'stroke':
                for s in attr[1:]:
                    if isinstance(s, list):
                        if s[0] == 'width': obj.stroke.width = float(s[1])
                        elif s[0] == 'type': obj.stroke.type = s[1]
            elif attr[0] == 'fill':
                for f in attr[1:]:
                    if isinstance(f, list) and f[0] == 'type': obj.fill.type = f[1]

    def _parse_graphics_and_pins(self, sym: Symbol, block, u, d):
        for node in block[2:]:
            if not isinstance(node, list): continue
            
            if node[0] == 'pin':
                pin = LibPin(number="", name="", electrical_type=node[1], style=node[2] if len(node)>2 and isinstance(node[2], str) else "line", unit=u, demorgan=d)
                for attr in node[3:]:
                    if isinstance(attr, list):
                        if attr[0] == 'name': pin.name = attr[1]
                        elif attr[0] == 'number': pin.number = attr[1]
                        elif attr[0] == 'length': pin.length = float(attr[1])
                        elif attr[0] == 'at': pin.position = Position(float(attr[1]), float(attr[2]), float(attr[3]) if len(attr)>3 else 0)
                        elif attr[0] == 'alternate':
                            alt = PinAlternate(name=attr[1])
                            if len(attr) > 2 and isinstance(attr[2], str): alt.electrical_type = attr[2]
                            if len(attr) > 3 and isinstance(attr[3], str): alt.style = attr[3]
                            pin.alternates.append(alt)
                sym.add_item(pin)
                
            elif node[0] == 'rectangle':
                r = Rectangle(unit=u, demorgan=d)
                for attr in node[1:]:
                    if isinstance(attr, list):
                        if attr[0] == 'start': r.start = Position(float(attr[1]), float(attr[2]))
                        elif attr[0] == 'end': r.end = Position(float(attr[1]), float(attr[2]))
                self._parse_stroke_fill(r, node)
                sym.add_item(r)
                
            elif node[0] == 'circle':
                c = Circle(unit=u, demorgan=d)
                for attr in node[1:]:
                    if isinstance(attr, list):
                        if attr[0] == 'center': c.center = Position(float(attr[1]), float(attr[2]))
                        elif attr[0] == 'radius': c.radius = float(attr[1])
                self._parse_stroke_fill(c, node)
                sym.add_item(c)
                
            elif node[0] == 'polyline':
                pl = Polyline(unit=u, demorgan=d)
                for attr in node[1:]:
                    if isinstance(attr, list) and attr[0] == 'pts':
                        for pt in attr[1:]:
                            if isinstance(pt, list) and pt[0] == 'xy': pl.points.append(Position(float(pt[1]), float(pt[2])))
                self._parse_stroke_fill(pl, node)
                sym.add_item(pl)

            elif node[0] == 'arc':
                a = Arc(unit=u, demorgan=d)
                for attr in node[1:]:
                    if isinstance(attr, list):
                        if attr[0] == 'start': a.start = Position(float(attr[1]), float(attr[2]))
                        elif attr[0] == 'mid': a.mid = Position(float(attr[1]), float(attr[2]))
                        elif attr[0] == 'end': a.end = Position(float(attr[1]), float(attr[2]))
                self._parse_stroke_fill(a, node)
                sym.add_item(a)
                
            elif node[0] == 'bezier':
                bz = Bezier(unit=u, demorgan=d)
                for attr in node[1:]:
                    if isinstance(attr, list) and attr[0] == 'pts':
                        for pt in attr[1:]:
                            if isinstance(pt, list) and pt[0] == 'xy': bz.points.append(Position(float(pt[1]), float(pt[2])))
                self._parse_stroke_fill(bz, node)
                sym.add_item(bz)

            elif node[0] == 'text':
                t = LibText(text=node[1], unit=u, demorgan=d)
                for attr in node[1:]:
                    if isinstance(attr, list):
                        if attr[0] == 'at': t.position = Position(float(attr[1]), float(attr[2]), float(attr[3]) if len(attr)>3 else 0)
                        elif attr[0] == 'effects': self._parse_effects(t.effects, attr)
                sym.add_item(t)

            elif node[0] == 'text_box':
                tb = TextBox(text=node[1], unit=u, demorgan=d)
                for attr in node[1:]:
                    if isinstance(attr, list):
                        if attr[0] == 'at': tb.position = Position(float(attr[1]), float(attr[2]), float(attr[3]) if len(attr)>3 else 0)
                        elif attr[0] == 'size': tb.size_x, tb.size_y = float(attr[1]), float(attr[2])
                        elif attr[0] == 'margins': tb.margins = [float(x) for x in attr[1:5]]
                        elif attr[0] == 'effects': self._parse_effects(tb.effects, attr)
                self._parse_stroke_fill(tb, node)
                sym.add_item(tb)

    def _tokenize(self, text: str) -> list:
        tokens, in_string, current, i = [], False, [], 0
        while i < len(text):
            c = text[i]
            if in_string:
                current.append(c)
                if c == '"' and text[i-1] != '\\':
                    in_string, tokens, current = False, tokens + ["".join(current)], []
            else:
                if c == '"':
                    if current: tokens.append("".join(current)); current = []
                    in_string, current = True, [c]
                elif c in '()':
                    if current: tokens.append("".join(current)); current = []
                    tokens.append(c)
                elif c.isspace():
                    if current: tokens.append("".join(current)); current = []
                else: current.append(c)
            i += 1
        if current: tokens.append("".join(current))
        return tokens

    def _parse(self, tokens: list) -> list:
        stack, current_list = [], []
        for token in tokens:
            if token == '(':
                stack.append(current_list)
                current_list = []
            elif token == ')':
                if not stack: break
                parent = stack.pop()
                parent.append(current_list)
                current_list = parent
            else:
                if token.startswith('"') and token.endswith('"'): token = token[1:-1]
                current_list.append(token)
        return current_list[0] if current_list else []