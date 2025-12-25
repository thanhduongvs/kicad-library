package csv

import (
	"github.com/tushar2708/altcsv"
	"log"
	"os"
)

func CreateCapacitorFile(name string, data []Capacitor) {
	ex := Capacitor{}
	headers := ex.GetTags()
	fileWtr, _ := os.Create(name)
	csvWtr := altcsv.NewWriter(fileWtr)
	csvWtr.Quote = '"'      // use | as "quote"
	csvWtr.AllQuotes = true // surround each field with '|'
	csvWtr.Write(headers)
	for _, v := range data {
		row := v.GetValues()
		/*
			row := []string{v.PartID, v.Description, v.Category,
				v.Value, v.Symbol, v.Footprint, v.Distributor,
				v.DistributorPart, v.Manufacturer, v.ManufacturerPart,
				v.Package, v.Capacitance, v.Voltage,
				v.Material, v.Tolerance, v.Datasheet,
			}*/
		if err := csvWtr.Write(row); err != nil {
			log.Fatalln("error writing data to file", err)
		}
	}
	csvWtr.Flush()
	fileWtr.Close()
}

func CreateResistorFile(name string, data []Resistor) {
	ex := Resistor{}
	headers := ex.GetTags()
	fileWtr, _ := os.Create(name)
	csvWtr := altcsv.NewWriter(fileWtr)
	csvWtr.Quote = '"'      // use | as "quote"
	csvWtr.AllQuotes = true // surround each field with '|'
	csvWtr.Write(headers)
	for _, v := range data {
		row := v.GetValues()
		/*
			row := []string{v.PartID, v.Description, v.Category,
				v.Value, v.Symbol, v.Footprint, v.Distributor,
				v.DistributorPart, v.Manufacturer, v.ManufacturerPart,
				v.Package, v.Capacitance, v.Voltage,
				v.Material, v.Tolerance, v.Datasheet,
			}*/
		if err := csvWtr.Write(row); err != nil {
			log.Fatalln("error writing data to file", err)
		}
	}
	csvWtr.Flush()
	fileWtr.Close()
}
