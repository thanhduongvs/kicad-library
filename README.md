# kicad-library

### Config path

- **LIB_SYMBOL_DIR** : *path/to/kicad-library/symbol*
- **LIB_FOOTPRINT_DIR** : *path/to/kicad-library/footprint.pretty*
- **LIB_3DMODEL_DIR** : *path/to/kicad-library/3dmodels*
- **LIB_TEMPLATE_DIR** : *path/to/kicad-library/sheet*

## KiPart
https://github.com/devbisme/KiPart

### Installation
- `pip install kipart`
- `kipart -s name nrf52840.xlsx -o nrf52840.lib`

## BOM generator scripts
- Open **Sechematic Editor** > **Tool** > **Generate BOM...**
- Click button add a new BOM then browse to folder **bom-scripts**
- Select file **bom_onekiwi.py** or **bom_onekiwi_v2.py**

## Schematic Field name Template
- Assembly
- Category
- Description
- Distributor
- Distributor Part#
- Manufacturer
- Manufacturer Part#

- Package
- Power
- Voltage
- Current
- Tolerance
- Material
- Function

## Create Power Symbol
- `cd power`
- `go run main.go P3V3 P5V0 P12V0`
