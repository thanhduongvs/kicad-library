#
# Example python script to generate a BOM from a KiCad generic netlist
#
# Example: Sorted and Grouped CSV BOM
#

"""
    @package
    Output: CSV (comma-separated)
    Grouped By: Value
    Sorted By: Ref
    Fields: Item, Category, Value, References, Package, Description, Assembly, Distributor, Distributor Part#, Manufacturer, Manufacturer Part#, Quantity
    Outputs ungrouped components first, then outputs grouped components.
    Command line:
    python "pathToFile/bom_ontech.py" "%I" "%O.csv"
"""

from __future__ import print_function

# Import the KiCad python helper module and the csv formatter
import kicad_netlist_reader
import csv
import sys

def myEqu(self, other):
    """myEqu is a more advanced equivalence function for components which is
    used by component grouping. Normal operation is to group components based
    on their value and footprint.
    In this example of a custom equivalency operator we compare the
    value, the part name and the footprint.
    """
    result = True
    if self.getValue() != other.getValue():
        result = False
    elif self.getPartName() != other.getPartName():
        result = False
    elif self.getFootprint() != other.getFootprint():
        result = False

    return result

# Override the component equivalence operator - it is important to do this
# before loading the netlist, otherwise all components will have the original
# equivalency operator.
kicad_netlist_reader.comp.__eq__ = myEqu

if len(sys.argv) != 3:
    print("Usage ", __file__, "<generic_netlist.xml> <output.csv>", file=sys.stderr)
    sys.exit(1)


# Generate an instance of a generic netlist, and load the netlist tree from
# the command line option. If the file doesn't exist, execution will stop
net = kicad_netlist_reader.netlist(sys.argv[1])

# Open a file to write to, if the file cannot be opened output to stdout
# instead
try:
    name = sys.argv[2]
    cnt = name.rfind('/')
    name1 = name[:cnt+1]
    name2 = name[cnt+1:]
    name = name1 + 'bom_' + name2
    f = open(name, 'w', encoding="utf-8")
except IOError:
    e = "Can't open output file for writing: " + sys.argv[2]
    print( __file__, ":", e, sys.stderr )
    f = sys.stdout

# Create a new csv writer object to use as the output formatter
out = csv.writer( f, lineterminator='\n', delimiter=',', quotechar='\"', quoting=csv.QUOTE_ALL )

# Write CSV
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

item = 0
grouped = net.groupComponents()
for group in grouped:
    refs = ""

    for component in group:
        # remove DNP and PCB
        if component.getField("Assembly") != "DNP" and component.getField("Category") != "PCB":
            refs += component.getRef() + ", "
            c = component
    cnt = len(refs)
    refs = refs[:cnt-2]
    footprint = net.getGroupFootprint(group).split(":")[1]
    
    if cnt > 0:
        item += 1
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
            len(group),
        ])

out.writerow([
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
])

# add DNP
for group in grouped:
    refs = ""
    for component in group:
        if component.getField("Assembly") == "DNP":
            refs += component.getRef() + ", "
            c = component
    cnt = len(refs)
    refs = refs[:cnt-2]
    
    if cnt > 0:
        item += 1
        out.writerow([
            item,
            c.getField("Category"),
            c.getValue(),
            refs,
            net.getGroupFootprint(group),
            c.getField("Description"),
            c.getField("Assembly"),
            c.getField("Distributor"),
            c.getField("Distributor Part#"),
            c.getField("Manufacturer"),
            c.getField("Manufacturer Part#"),
            len(group),
        ])

f.close()