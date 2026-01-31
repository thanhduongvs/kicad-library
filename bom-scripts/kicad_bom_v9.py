# -*- coding: utf-8 -*-
#
# Custom BOM generator for KiCad in CSV format
#
# Requirements:
# 1. Sort by "Category" field
# 2. Exclude components where Category == "PCB"
# 3. Components with DNP (Do Not Populate) must be at the end of the list
# 4. Insert a blank line before the DNP section
#

import kicad_netlist_reader_v9 as kicad_netlist_reader
import kicad_utils_v9 as kicad_utils
import csv
import sys
import os

# Helper function to get clean footprint name (e.g., "Package_TO_SOT:SOT-23" -> "SOT-23")
def get_clean_footprint(fp_string):
    if ":" in fp_string:
        return fp_string.split(":")[-1]
    return fp_string

# Get the input and output file paths from command line arguments
input_file = sys.argv[1]
output_path = sys.argv[2]

# --- DIRECTORY AND FILE HANDLING ---
# Get the base directory of the project
project_dir = os.path.dirname(output_path)

# Define the 'assembly' directory path
assembly_dir = os.path.join(project_dir, 'assembly')

# Create 'assembly' folder if it doesn't exist
if not os.path.exists(assembly_dir):
    os.makedirs(assembly_dir)

# Handle filename: starts with 'bom_' and ends with '.csv'
filename = os.path.basename(output_path)
if not filename.startswith('bom_'):
    filename = 'bom_' + filename

if not filename.lower().endswith('.csv'):
    filename += '.csv'

# Set the final destination to be inside the assembly folder
final_output = os.path.join(assembly_dir, filename)

# Initialize the netlist reader
net = kicad_netlist_reader.netlist(input_file)

# Open the output file
try:
    f = kicad_utils.open_file_writeUTF8(final_output, 'w')
except IOError:
    print("Can't open output file for writing: " + final_output, file=sys.stderr)
    f = sys.stdout

# Initialize CSV writer with standard formatting
out = csv.writer(f, lineterminator='\n', delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

# Get components from the netlist, excluding those marked "Exclude from BOM"
components = net.getInterestingComponents(excludeBOM=True)

# --- STEP 1: FILTERING ---
# Filter out components with Category "PCB" (case-insensitive)
filtered_components = []
for c in components:
    if c.getField("Category").upper() == "PCB":
        continue
    filtered_components.append(c)

# --- STEP 2: GROUPING ---
# Group components by Value, Footprint, and DNP status
grouped = net.groupComponents(filtered_components)

# --- STEP 3: SORTING LOGIC ---
# Sort priority: 
# 1st: DNP status (Non-DNP first, DNP last)
# 2nd: Category name (Alphabetical)
def sort_logic(group):
    c = group[0]
    # is_dnp will be 0 for false, 1 for true
    is_dnp = 1 if (c.getDNPString() and c.getDNPString().strip() != "") else 0
    category = c.getField("Category").strip().lower()
    return (is_dnp, category)

grouped.sort(key=sort_logic)

# --- STEP 4: CSV OUTPUT ---
# Write CSV Header
out.writerow([
    'Item',
    'Category',
    'Value',
    'References',
    'Package',
    'Description',
    'Quantity',
    'Assembly',
    'Manufacturer',
    'Manufacturer Part',
    'Distributor',
    'Distributor Part',
    'Distributor Alternate',
    'Distributor Part Alternate',
])

item = 0
dnp_separator_added = False

for group in grouped:
    c = group[0]
    # Check if the current group is a DNP group
    is_currently_dnp = bool(c.getDNPString() and c.getDNPString().strip())

    # Insert a blank line before the first DNP component appears
    if is_currently_dnp and not dnp_separator_added:
        out.writerow([]) # Blank row
        dnp_separator_added = True

    item += 1
    refs = ", ".join([comp.getRef() for comp in group])
    clean_fp = get_clean_footprint(c.getFootprint())
    
    # Prepare data row
    row = [
        item,
        c.getField("Category"),
        c.getValue(),
        refs,
        clean_fp,
        c.getField("Description"),
        len(group),
        c.getDNPString(),
        c.getField("Manufacturer"),
        c.getField("Manufacturer Part"),
        c.getField("Distributor"),
        c.getField("Distributor Part"),
        c.getField("Distributor Alternate"),
        c.getField("Distributor Part Alternate"),
    ]
    out.writerow(row)

# Close file
f.close()
print(f"Success: BOM generated at {final_output}")
