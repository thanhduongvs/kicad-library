import os
from symbol_data import Rectangle, Circle, Arc, Polyline, Bezier, LibText, TextBox, LibPin
from symbol_data import KiLibManager

class SymbolSerializer:
    @staticmethod
    def _format_number(num: float):
        if num == 0.0: return "0"
        return f"{num:g}"

    @classmethod
    def save(cls, lib_manager: KiLibManager, output_filepath: str):
        lines = []
        def add(text: str, indent: int = 0):
            lines.append(("\t" * indent) + text)

        def write_stroke_fill(obj, indent: int):
            w = cls._format_number(obj.stroke.width)
            add(f'(stroke (width {w}) (type {obj.stroke.type}))', indent)
            add(f'(fill (type {obj.fill.type}))', indent)
            
        def write_effects(eff, indent: int):
            add('(effects', indent)
            add('(font', indent + 1)
            sx, sy = cls._format_number(eff.font.size_x), cls._format_number(eff.font.size_y)
            add(f'(size {sx} {sy})', indent + 2)
            add(')', indent + 1)
            if eff.justify and eff.justify != "center": add(f'(justify {eff.justify})', indent + 1)
            if getattr(eff, 'hide', False): add('(hide yes)', indent + 1)
            add(')', indent)

        add("(kicad_symbol_lib", 0)
        add(f'(version {lib_manager.metadata.version})', 1)
        add(f'(generator "{lib_manager.metadata.generator}")', 1)
        add(f'(generator_version "{lib_manager.metadata.generator_version}")', 1)

        for sym_name, sym in lib_manager.symbols.items():
            add(f'(symbol "{sym_name}"', 1)
            if getattr(sym, 'extends', ""): add(f'(extends "{sym.extends}")', 2)
            add(f'(exclude_from_sim {"yes" if sym.exclude_from_sim else "no"})', 2)
            add(f'(in_bom {"yes" if sym.in_bom else "no"})', 2)
            add(f'(on_board {"yes" if sym.on_board else "no"})', 2)
            add(f'(in_pos_files {"yes" if sym.in_pos_files else "no"})', 2)
            add(f'(duplicate_pin_numbers_are_jumpers {"yes" if sym.duplicate_pin_numbers_are_jumpers else "no"})', 2)

            for prop in sorted(sym.properties.values(), key=lambda p: p.id):
                x, y, angle = cls._format_number(prop.position.x), cls._format_number(prop.position.y), cls._format_number(prop.position.angle)
                add(f'(property "{prop.key}" "{prop.value}"', 2)
                add(f'(at {x} {y} {angle})', 3)
                if prop.show_name: add('(show_name yes)', 3)
                if prop.do_not_autoplace: add('(do_not_autoplace yes)', 3)
                if prop.hide: add('(hide yes)', 3)
                write_effects(prop.effects, 3)
                add(')', 2)

            units = set((item.unit, item.demorgan) for item in sym.draw_items)
            
            for u, d in sorted(units):
                add(f'(symbol "{sym_name}_{u}_{d}"', 2)
                items_in_unit = [i for i in sym.draw_items if i.unit == u and i.demorgan == d]
                
                for item in items_in_unit:
                    if isinstance(item, Rectangle):
                        add('(rectangle', 3)
                        add(f'(start {cls._format_number(item.start.x)} {cls._format_number(item.start.y)})', 4)
                        add(f'(end {cls._format_number(item.end.x)} {cls._format_number(item.end.y)})', 4)
                        write_stroke_fill(item, 4)
                        add(')', 3)
                        
                    elif isinstance(item, Circle):
                        add('(circle', 3)
                        add(f'(center {cls._format_number(item.center.x)} {cls._format_number(item.center.y)})', 4)
                        add(f'(radius {cls._format_number(item.radius)})', 4)
                        write_stroke_fill(item, 4)
                        add(')', 3)
                        
                    elif isinstance(item, Polyline):
                        add('(polyline', 3)
                        pts = " ".join([f"(xy {cls._format_number(pt.x)} {cls._format_number(pt.y)})" for pt in item.points])
                        add(f'(pts {pts})', 4)
                        write_stroke_fill(item, 4)
                        add(')', 3)
                        
                    elif isinstance(item, Arc):
                        add('(arc', 3)
                        add(f'(start {cls._format_number(item.start.x)} {cls._format_number(item.start.y)})', 4)
                        add(f'(mid {cls._format_number(item.mid.x)} {cls._format_number(item.mid.y)})', 4)
                        add(f'(end {cls._format_number(item.end.x)} {cls._format_number(item.end.y)})', 4)
                        write_stroke_fill(item, 4)
                        add(')', 3)
                        
                    elif isinstance(item, Bezier):
                        add('(bezier', 3)
                        pts = " ".join([f"(xy {cls._format_number(pt.x)} {cls._format_number(pt.y)})" for pt in item.points])
                        add(f'(pts {pts})', 4)
                        write_stroke_fill(item, 4)
                        add(')', 3)
                        
                    elif isinstance(item, LibText):
                        x, y, angle = cls._format_number(item.position.x), cls._format_number(item.position.y), cls._format_number(item.position.angle)
                        add(f'(text "{item.text}"', 3)
                        add(f'(at {x} {y} {angle})', 4)
                        write_effects(item.effects, 4)
                        add(')', 3)
                        
                    elif isinstance(item, TextBox):
                        add(f'(text_box "{item.text}"', 3)
                        px, py, ang = cls._format_number(item.position.x), cls._format_number(item.position.y), cls._format_number(item.position.angle)
                        add(f'(at {px} {py} {ang})', 4)
                        sx, sy = cls._format_number(item.size_x), cls._format_number(item.size_y)
                        add(f'(size {sx} {sy})', 4)
                        marg_str = " ".join(cls._format_number(m) for m in item.margins)
                        add(f'(margins {marg_str})', 4)
                        write_stroke_fill(item, 4)
                        write_effects(item.effects, 4)
                        add(')', 3)

                    elif isinstance(item, LibPin):
                        add(f'(pin {item.electrical_type} {item.style}', 3)
                        px, py, p_angle, p_len = cls._format_number(item.position.x), cls._format_number(item.position.y), cls._format_number(item.position.angle), cls._format_number(item.length)
                        add(f'(at {px} {py} {p_angle})', 4)
                        add(f'(length {p_len})', 4)
                        add(f'(name "{item.name}"', 4)
                        add('(effects', 5)
                        add('(font', 6)
                        add('(size 1.27 1.27)', 7)
                        add(')', 6)
                        add(')', 5)
                        add(')', 4)
                        add(f'(number "{item.number}"', 4)
                        add('(effects', 5)
                        add('(font', 6)
                        add('(size 1.27 1.27)', 7)
                        add(')', 6)
                        add(')', 5)
                        add(')', 4)
                        for alt in item.alternates:
                            add(f'(alternate "{alt.name}" {alt.electrical_type} {alt.style})', 4)
                        add(')', 3)
                
                add(')', 2)

            add(f'(embedded_fonts {"yes" if sym.embedded_fonts else "no"})', 2)
            add(')', 1)
            
        add(")", 0)

        try:
            with open(output_filepath, 'w', encoding='utf-8') as f:
                f.write("\n".join(lines) + "\n")
            print(f"[+] LƯU FILE THÀNH CÔNG: {os.path.abspath(output_filepath)}")
        except Exception as e:
            print(f"[-] Lỗi khi lưu file: {e}")