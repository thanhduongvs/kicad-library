package bom

import (
	"fmt"
	"lcsc/api"
	"lcsc/csv"
	"lcsc/response"
)

const (
	CeramicCapacitors  = 313
	TantalumCapacitors = 314
	AluminumCapacitors = 418
)

func GetProductCapacitor(capValue string) {
	totalPage := 5
	results := []response.ProductData{}

	for i := 1; i <= totalPage; i++ {
		fmt.Printf("capacitor %s loading page %d\n", capValue, i)
		data, total := api.GetProductSearch(i, CeramicCapacitors, capValue)
		totalPage = total
		results = append(results, data...)
	}

	cap := []csv.Capacitor{}
	for _, v := range results {
		//c := new(csv.Capacitor)
		var c csv.Capacitor
		c.MapValue(capValue, v)
		cap = append(cap, c)
	}
	name := "Cap" + capValue + ".csv"
	csv.CreateCapacitorFile(name, cap)
}

func CreateCapacitorData() {
	smds := []string{"0201", "0402", "0603", "0805", "1206", "1210"}
	for _, v := range smds {
		GetProductCapacitor(v)
	}

}
