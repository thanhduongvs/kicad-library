import csv
import os
import sys
import argparse
from .symbol_data import KiLibManager, Rectangle, Position, Stroke, Fill, LibPin

def parse_unit(unit_str: str) -> int:
    unit_str = unit_str.upper().strip()
    if unit_str == "ALL" or not unit_str.startswith("UNIT"): return 1
    letter = unit_str.replace("UNIT", "").strip()
    if len(letter) == 1 and 'A' <= letter <= 'Z': return ord(letter) - ord('A') + 1
    return 1

def parse_angle(ori: str) -> float:
    ori = ori.upper().strip()
    if ori == "RIGHT": return 0.0
    elif ori == "UP": return 90.0
    elif ori == "LEFT": return 180.0
    elif ori == "DOWN": return 270.0
    return 0.0

def parse_elec_type(etype: str) -> str:
    etype = etype.lower().strip()
    mapping = {
        "power input": "power_in", "power output": "power_out",
        "open collector": "open_collector", "open emitter": "open_emitter",
        "tri-state": "tri_state", "bidirectional": "bidirectional",
        "passive": "passive", "input": "input", "output": "output",
    }
    return mapping.get(etype, "unspecified")

def create_symbol_from_csv(lib_manager: KiLibManager, symbol_name: str, csv_filepath: str):
    print(f"[*] Đang phân tích file CSV: '{csv_filepath}' ...")
    sym = lib_manager.add_symbol(symbol_name)
    sym.set_prop("Description", f"Generated from {os.path.basename(csv_filepath)}", hide=True)

    unit_pins = {}
    auto_layout_queue = {} 

    with open(csv_filepath, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        cols = {k.strip(): k for k in reader.fieldnames if k}
        
        for row in reader:
            def get_val(key, default=""): return row[cols[key]].strip() if key in cols else default
            num = get_val("Number", "")
            if not num: continue
            
            name = get_val("Name", "")
            etype = parse_elec_type(get_val("Electrical Type", "Passive"))
            style = get_val("Graphic Style", "Line").lower()
            length = float(get_val("Length", "2.54"))
            unit_val = parse_unit(get_val("Unit", "ALL"))
            
            x_str, y_str = get_val("X Position", ""), get_val("Y Position", "")
            needs_auto = (x_str == "" or y_str == "")
            x, y = float(x_str) if x_str else 0.0, float(y_str) if y_str else 0.0
            angle = parse_angle(get_val("Orientation", "Right"))
            
            pin = LibPin(
                unit=unit_val, number=num, name=name,
                electrical_type=etype, style=style, length=length,
                position=Position(x=x, y=y, angle=angle)
            )
            sym.add_item(pin)
            
            if unit_val not in unit_pins:
                unit_pins[unit_val] = []
                auto_layout_queue[unit_val] = []
            unit_pins[unit_val].append(pin)
            if needs_auto: auto_layout_queue[unit_val].append(pin)

    # AUTO LAYOUT
    for u, auto_pins in auto_layout_queue.items():
        if not auto_pins: continue
        total_auto = len(auto_pins)
        left_count = (total_auto + 1) // 2
        start_y = ((max(left_count, total_auto - left_count) - 1) * 2.54) / 2
        box_width = 20.32
        
        for i, p in enumerate(auto_pins):
            if i < left_count:
                p.position.x = -box_width / 2 - p.length
                p.position.y = start_y - i * 2.54
                p.position.angle = 0 
            else:
                p.position.x = box_width / 2 + p.length
                p.position.y = start_y - (i - left_count) * 2.54
                p.position.angle = 180 

    # AUTO RECTANGLE
    for u, pins in unit_pins.items():
        if not pins: continue
        body_x, body_y = [], []
        for p in pins:
            px, py, ang, l = p.position.x, p.position.y, p.position.angle, p.length
            if ang == 0:    body_x.append(px + l); body_y.append(py)
            elif ang == 180: body_x.append(px - l); body_y.append(py)
            elif ang == 90:  body_x.append(px); body_y.append(py + l)
            elif ang == 270: body_x.append(px); body_y.append(py - l)
        
        if not body_x or not body_y: continue
        min_bx, max_bx, min_by, max_by = min(body_x), max(body_x), min(body_y), max(body_y)
        
        if not any(p.position.angle in [90, 270] for p in pins): min_by -= 2.54; max_by += 2.54
        if not any(p.position.angle in [0, 180] for p in pins): min_bx -= 2.54; max_bx += 2.54
            
        khung = Rectangle(
            unit=u, start=Position(x=min_bx, y=max_by), end=Position(x=max_bx, y=min_by),
            stroke=Stroke(width=0.254, type="solid"), fill=Fill(type="background")
        )
        sym.draw_items.insert(0, khung)
        
    print(f"[+] Tạo thành công '{symbol_name}' với {len(sym.pins)} chân, chia làm {len(unit_pins)} khối (Unit)!")


def main():
    parser = argparse.ArgumentParser(
        description="🚀 KiCad Symbol Generator: Tạo thư viện KiCad (.kicad_sym) tự động từ file CSV.",
        epilog="Ví dụ: csv2kicad input.csv -s AMS1117 -o my_lib.kicad_sym"
    )
    parser.add_argument("csv_file", help="Đường dẫn đến file CSV chứa danh sách chân.")
    parser.add_argument("-s", "--symbol", required=True, help="Tên linh kiện muốn tạo (Ví dụ: STM32MP135).")
    parser.add_argument("-o", "--output", default="generated_lib.kicad_sym", help="Tên file thư viện đầu ra (Mặc định: generated_lib.kicad_sym).")

    args = parser.parse_args()

    if not os.path.exists(args.csv_file):
        print(f"[-] LỖI: Không tìm thấy file '{args.csv_file}'!")
        sys.exit(1)

    try:
        lib = KiLibManager(args.output)
        create_symbol_from_csv(lib, args.symbol, args.csv_file)
        lib.save_to_file()
    except Exception as e:
        print(f"[-] LỖI TRONG QUÁ TRÌNH TẠO: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()