from kiutils.symbol import SymbolLib

def check_unexpected_fields(input_file):
    # List of allowed fields (using a Set for faster lookup)
    allowed_fields = {
        "Reference", 
        "Value", 
        "Footprint", 
        "Datasheet", 
        "Description", 
        "Category", 
        "Package", 
        "Manufacturer", 
        "Manufacturer Part", 
        "Distributor", 
        "Distributor Part", 
        "Distributor Alternate", 
        "Distributor Part Alternate",
        "ki_keywords",
        "ki_fp_filters",
        "ki_locked"
    }

    print(f"Scanning file: {input_file} ...\n")
    print("-" * 60)
    print(f"{'SYMBOL NAME':<40} | {'UNEXPECTED FIELD'}")
    print("-" * 60)

    try:
        # Load the library
        lib = SymbolLib.from_file(input_file)
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    count_issues = 0

    # Iterate through all symbols in the library
    for symbol in lib.symbols:
        # Iterate through all properties of the current symbol
        for prop in symbol.properties:
            # Check if the property key is NOT in the allowed list
            if prop.key not in allowed_fields:
                print(f"{symbol.entryName:<40} | {prop.key}")
                count_issues += 1

    print("-" * 60)
    if count_issues == 0:
        print("Result: No unexpected fields found. All clean!")
    else:
        print(f"Result: Found {count_issues} unexpected field(s).")

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    # Ensure the file name matches your actual file
    check_unexpected_fields('symbol.kicad_sym')