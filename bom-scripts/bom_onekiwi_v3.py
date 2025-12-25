#
# Example python script to generate a BOM from a KiCad generic netlist
#
# Example: Sorted and Grouped CSV BOM
#

"""
    @package
    Output: CSV (comma-separated)
    Grouped By: Value, Package
    Sorted By: References
    Fields: Item, Category, Value, References, Package, Description, Assembly, Distributor, Distributor Part#, Manufacturer, Manufacturer Part#, Quantity

    Command line:
    python "pathToFile/bom_onekiwi_v3.py" "%I" "%O.csv"
"""

# Import the KiCad python helper module and the csv formatter
import kicad_netlist_reader
import kicad_utils
import csv
import sys
import os

# Generate an instance of a generic netlist, and load the netlist tree from
# the command line option. If the file doesn't exist, execution will stop
net = kicad_netlist_reader.netlist(sys.argv[1])

# Open a file to write to, if the file cannot be opened output to stdout
# instead
try:
    dir = os.path.dirname(sys.argv[2])
    name = os.path.basename(sys.argv[2])
    name = "bom_" + name
    pathfile = os.path.join(dir, "", name)
    print ("Output: " + pathfile)

    f = kicad_utils.open_file_writeUTF8(pathfile, 'w')
    #f = open(name, 'w', encoding="utf-8")
except IOError:
    e = "Can't open output file for writing: " + pathfile
    print(__file__, ":", e, sys.stderr)
    f = sys.stdout

# Create a new csv writer object to use as the output formatter
out = csv.writer(f, delimiter=',', quotechar='\"', quoting=csv.QUOTE_ALL)

# Output a set of rows for a header providing general information
out.writerow([
    'Item',
    'Category',  # E.g. Electronics, Connector, Mechanical, PCB
    'Value',  # E.g. 10k, 0.1uF
    'References',  # E.g. U1, R1
    'Package',  # E.g. SMD, 0805, SOT-23-5
    'Description',  # Auto-populated by KiCad
    'Assembly',
    'Distributor',
    'Distributor Part#',
    'Manufacturer',
    'Manufacturer Part#',
    'Quantity',  # Quantity of each part
])

# Get all of the components in groups of matching parts + values
# (see ky_generic_netlist_reader.py)
grouped = net.groupComponents()

# Output all of the component information
item = 0
for group in grouped:
    refs = ""
    item += 1
    quantity = 0

    # Add the reference of every component in the group and keep a reference
    # to the component so that the other data can be filled in once per group
    for component in group:
        if component.getField("Assembly") != "DNP" and component.getField("Category") != "PCB":
            refs += component.getRef() + ", "
            c = component
            quantity += 1

    if quantity > 0:
        footprint = ""
        try:
            footprint = net.getGroupFootprint(group).split(":")[1]
        except:
            pass
        cnt = len(refs)
        refs = refs[:cnt-2]

        out.writerow([
            item,
            c.getField("Category"),
            c.getValue(),
            refs,
            footprint,
            c.getField("Description"),
            c.getField("Assembly"),
            c.getField("Distributor"),
            c.getField("Distributor Part#"),
            c.getField("Manufacturer"),
            c.getField("Manufacturer Part#"),
            quantity,
        ])

out.writerow(["","","","","","","","","","","","",])

# add DNP
for group in grouped:
    refs = ""
    quantity = 0
    for component in group:
        if component.getField("Assembly") == "DNP":
            refs += component.getRef() + ", "
            c = component
            quantity += 1
    cnt = len(refs)
    refs = refs[:cnt-2]
    
    if cnt > quantity:
        item += 1
        footprint = net.getGroupFootprint(group).split(":")[1]
        out.writerow([
            item,
            c.getField("Category"),
            c.getValue(),
            refs,
            footprint,
            c.getField("Description"),
            c.getField("Assembly"),
            c.getField("Distributor"),
            c.getField("Distributor Part#"),
            c.getField("Manufacturer"),
            c.getField("Manufacturer Part#"),
            quantity,
        ])

#f.close()