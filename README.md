# onekiwi-kicad-library

### Config path

- **ONEKIWI_SYMBOL_DIR** : *path/to/onekiwi-kicad-library/symbol*
- **ONEKIWI_FOOTPRINT_DIR** : *path/to/onekiwi-kicad-library/footprint.pretty*
- **ONEKIWI_3DMODEL_DIR** : *path/to/onekiwi-kicad-library/3dmodels*
- **ONEKIWI_TEMPLATE_DIR** : *path/to/onekiwi-kicad-library/sheet*

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
