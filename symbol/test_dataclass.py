from symbol_data import KiLibManager, Rectangle, Position, Stroke, Fill, LibPin, PinAlternate

# 1. Đọc file
lib = KiLibManager("test.kicad_sym")

# 2. Tạo linh kiện STM32
mcu = lib.add_symbol("STM32MP135_TEST")
mcu.set_prop("Description", "Dual Cortex-A7 MPU")
mcu.set_prop("Category", "IC")
mcu.set_prop("SubCategory", "MCU")
mcu.set_prop("Package", "QFN32_5.0x5.0")
mcu.set_prop("Manufacturer", "YAGEO")
mcu.set_prop("Manufacturer Part", "RC0603FR-0710KL")
mcu.set_prop("Distributor", "LCSC")
mcu.set_prop("Distributor Part", "C98220")
mcu.set_prop("Distributor Alternate", "DigiKey")
mcu.set_prop("Distributor Part Alternate", "C2907002")
# 3. Tạo hình hộp bao quanh
khung = Rectangle(
    unit=1,
    start=Position(x=0, y=0),  # ĐÃ SỬA: Dùng x, y thường
    end=Position(x=12.7, y=-12.7),    # ĐÃ SỬA: Dùng x, y thường
    stroke=Stroke(width=0, type="solid"),
    fill=Fill(type="background")
)
mcu.add_item(khung)

# 4. Tạo chân cắm đa chức năng (Alternate Pins)
chan_pa0 = LibPin(
    unit=1, number="1", name="PA0", electrical_type="bidirectional", length=2.54,
    position=Position(x=-2.54, y=-5.08, angle=0)  # ĐÃ SỬA: Dùng x, y thường
)
chan_pa0.alternates.append(PinAlternate(name="TIM2_CH1", electrical_type="output"))
chan_pa0.alternates.append(PinAlternate(name="USART2_CTS", electrical_type="input"))

mcu.add_item(chan_pa0)

# 5. Lưu ra file mới
lib.save_to_file("test.kicad_sym")