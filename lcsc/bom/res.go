package bom

import (
	"fmt"
	"lcsc/api"
	"lcsc/csv"
	"lcsc/response"
)

const (
	ResistorSMD = 439
)

func GetProductResistor(capValue string) {
	totalPage := 5
	results := []response.ProductData{}

	for i := 1; i <= totalPage; i++ {
		fmt.Printf("resistor %s loading page %d\n", capValue, i)
		data, total := api.GetProductSearch(i, ResistorSMD, capValue)
		totalPage = total
		results = append(results, data...)
	}

	cap := []csv.Resistor{}
	for _, v := range results {
		//c := new(csv.Capacitor)
		var c csv.Resistor
		c.MapValue(capValue, v)
		cap = append(cap, c)
	}
	name := "Res" + capValue + ".csv"
	csv.CreateResistorFile(name, cap)
}

func CreateResistorData() {
	smds := []string{"0201", "0402", "0603", "0805", "1206", "1210"}
	for _, v := range smds {
		GetProductResistor(v)
	}
}
