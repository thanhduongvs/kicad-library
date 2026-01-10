from kiutils.symbol import SymbolLib, Property
from kiutils.items.common import Position, Effects, Font

def add_extended_properties(input_file, output_file):
    # List of fields to add if they are missing
    target_fields = [
        "Category", 
        "Package", 
        "Manufacturer", 
        "Manufacturer Part", 
        "Distributor", 
        "Distributor Part", 
        "Distributor Alternate", 
        "Distributor Part Alternate"
    ]

    # List of fields that must be forced to HIDE (hide=True)
    fields_to_hide = ["Footprint", "Datasheet", "Description", "Category"]

    print(f"Reading file: {input_file} ...")
    
    try:
        lib = SymbolLib.from_file(input_file)
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    count_modified = 0

    for symbol in lib.symbols:
        is_modified = False
        
        # Track existing keys to check against target_fields later
        existing_keys = set()

        # --- STEP 1: UPDATE EXISTING PROPERTIES ---
        for prop in symbol.properties:
            existing_keys.add(prop.key)
            
            # Check if this property should be hidden (e.g., Footprint, Datasheet)
            if prop.key in fields_to_hide:
                # Ensure 'effects' object exists to avoid NoneType errors
                if prop.effects is None:
                    prop.effects = Effects()
                    # Setup default font if necessary
                    f_size = Position(X=1.27, Y=1.27)
                    f = Font()
                    f.size = f_size
                    prop.effects.font = f

                # If currently shown (hide=False or None), set to hidden (True)
                if not prop.effects.hide:
                    prop.effects.hide = True
                    is_modified = True
            
            # Ensure 'Package' is always VISIBLE (hide=False)
            if prop.key == "Package":
                 if prop.effects is None:
                    prop.effects = Effects()
                    f_size = Position(X=1.27, Y=1.27)
                    f = Font()
                    f.size = f_size
                    prop.effects.font = f
                 
                 # If currently hidden, unhide it
                 if prop.effects.hide:
                    prop.effects.hide = False
                    is_modified = True

        # --- STEP 2: ADD MISSING PROPERTIES ---
        for field in target_fields:
            if field not in existing_keys:
                should_hide = True
                if field == "Package":
                    should_hide = False
                
                # Setup Font and Effects (using safe initialization method)
                font_size = Position(X=1.27, Y=1.27)
                
                new_font = Font()
                new_font.size = font_size
                
                new_effects = Effects()
                new_effects.font = new_font
                new_effects.hide = should_hide
                
                # Setup Property
                new_prop = Property(key=field, value="")
                
                # Assign position manually to avoid __init__ keyword argument issues
                new_prop.position = Position(X=0, Y=0, angle=0)
                new_prop.effects = new_effects
                
                symbol.properties.append(new_prop)
                is_modified = True
        
        if is_modified:
            count_modified += 1

    lib.to_file(output_file)
    print(f"Done! Updated {count_modified} symbols.")
    print(f"New file saved at: {output_file}")

if __name__ == "__main__":
    add_extended_properties('symbol.kicad_sym', 'symbol_extended.kicad_sym')