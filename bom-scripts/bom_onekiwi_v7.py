#
# Example python script to generate a BOM from a KiCad generic netlist
#
# Example: Sorted and Grouped CSV BOM
#

"""
    @package
    Output: CSV (comma-separated)
    Grouped By: Value, Footprint, specified extra fields
    Sorted By: Reference
    Fields: Item, Category, Value, References, Package, Description, Assembly, Distributor, Distributor Part#, Manufacturer, Manufacturer Part#, Quantity
    
    Outputs components grouped by Value, Footprint, and specified extra fields.
    Extra fields can be passed as command line arguments at the end, one field per argument.

    Command line:
    python "pathToFile/bom_onekiwi_v7.py" "%I" "%O.csv" "Extra_Field1" "Extra_Field2"
"""

# Import the KiCad python helper module and the csv formatter
import kicad_netlist_reader_v7
import kicad_utils_v7
import csv
import sys
import os

# Get extra fields from the command line
extra_fields = sys.argv[3:]

def myEqu(self, other):
    """myEqu is a more advanced equivalence function for components which is
    used by component grouping. Normal operation is to group components based
    on their Value and Footprint.

    In this example of a more advanced equivalency operator we also compare the
    Footprint, Value and all extra fields passed from the command line. If 
    these fields are not used in some parts they will simply be ignored (they
    will match as both will be empty strings).

    """
    result = True
    if self.getValue() != other.getValue():
        result = False
    elif self.getFootprint() != other.getFootprint():
        result = False
    else:
        for field_name in extra_fields:
            if self.getField(field_name) != other.getField(field_name):
                result = False

    return result

# Override the component equivalence operator - it is important to do this
# before loading the netlist, otherwise all components will have the original
# equivalency operator.
kicad_netlist_reader_v7.comp.__eq__ = myEqu

# Generate an instance of a generic netlist, and load the netlist tree from
# the command line option. If the file doesn't exist, execution will stop
net = kicad_netlist_reader_v7.netlist(sys.argv[1])

# Open a file to write to, if the file cannot be opened output to stdout
# instead
try:
    dir = os.path.dirname(sys.argv[2])
    name = os.path.basename(sys.argv[2])
    name = "bom_" + name
    pathfile = os.path.join(dir, "", name)
    print ("Output: " + pathfile)

    f = kicad_utils_v7.open_file_writeUTF8(pathfile, 'w')
    #f = open(name, 'w', encoding="utf-8")
except IOError:
    e = "Can't open output file for writing: " + pathfile
    print(__file__, ":", e, sys.stderr)
    f = sys.stdout

# Create a new csv writer object to use as the output formatter
out = csv.writer(f, lineterminator='\n', delimiter=',', quotechar='\"', quoting=csv.QUOTE_ALL)

# Output a CSV header
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
        if component.isDoNotPopulate() == False and component.getField("Category") != "PCB":
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
            "",
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
        #if component.getField("Assembly") == "DNP":
        if component.isDoNotPopulate() == True:
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
            "DNP",
            c.getField("Distributor"),
            c.getField("Distributor Part#"),
            c.getField("Manufacturer"),
            c.getField("Manufacturer Part#"),
            quantity,
        ])

#f.close()