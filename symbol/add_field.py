import sys

def add_subcategory_if_missing(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    i = 0
    
    # Định nghĩa nội dung SubCategory cần thêm
    # Chúng ta sẽ thay thế {indent} bằng khoảng trắng thực tế tìm thấy trong file
    subcategory_template = [
        '{indent}(property "SubCategory" ""\n',
        '{indent}    (at 0 0 0)\n',
        '{indent}    (effects\n',
        '{indent}        (font\n',
        '{indent}            (size 1.27 1.27)\n',
        '{indent}        )\n',
        '{indent}        (hide yes)\n',
        '{indent}    )\n',
        '{indent})\n'
    ]

    while i < len(lines):
        line = lines[i]
        new_lines.append(line)
        
        # 1. Tìm thấy dòng bắt đầu property "Category"
        if '(property "Category"' in line:
            # Lấy lề (indentation) của dòng hiện tại để dùng cho SubCategory sau này
            current_indent = line[:line.find('(')]
            
            # 2. Tìm điểm kết thúc của block "Category" này
            # Nguyên tắc: Đếm dấu mở '(' và đóng ')' cho đến khi cân bằng
            open_count = line.count('(')
            close_count = line.count(')')
            
            # Nếu chưa đóng block ngay trên 1 dòng, tiếp tục đọc các dòng tiếp theo
            while open_count > close_count and i + 1 < len(lines):
                i += 1
                next_line = lines[i]
                new_lines.append(next_line)
                open_count += next_line.count('(')
                close_count += next_line.count(')')
            
            # Lúc này biến i đang đứng ở dòng cuối cùng của block "Category"
            
            # 3. Kiểm tra dòng tiếp theo (bỏ qua dòng trống) xem có phải là SubCategory không
            check_index = i + 1
            is_subcategory_next = False
            
            # Tìm dòng có nội dung tiếp theo
            while check_index < len(lines):
                stripped_line = lines[check_index].strip()
                if stripped_line == "":
                    check_index += 1
                    continue
                
                if '(property "SubCategory"' in lines[check_index]:
                    is_subcategory_next = True
                break # Đã tìm thấy dòng nội dung tiếp theo, dừng kiểm tra

            # 4. Nếu KHÔNG phải SubCategory, thì chèn block mới vào
            if not is_subcategory_next:
                print(" -> Đã thêm SubCategory sau Category.")
                for tmpl in subcategory_template:
                    # Chèn indent tương ứng với file gốc (thường là 2 hoặc 4 dấu cách)
                    new_lines.append(tmpl.format(indent=current_indent))
        
        i += 1

    # Ghi lại nội dung vào file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

# --- CÁCH SỬ DỤNG ---
# Thay đổi đường dẫn file bên dưới thành file của bạn
# file_path = "duong_dan_den_file_cua_ban.kicad_sym"
# add_subcategory_if_missing(file_path)

if __name__ == "__main__":
    # Ví dụ chạy trực tiếp nếu bạn gọi file từ command line
    
    add_subcategory_if_missing("symbol.kicad_sym")
    print("Hoàn tất xử lý file.")
    