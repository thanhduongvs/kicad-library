package main

import (
	_ "fmt"
	_ "lcsc/api"
	"lcsc/bom"
	"lcsc/kicad"
)

func main() {
	bom.CreateCapacitorData()
	bom.CreateResistorData()

	kicad.InitData()
	//api.GetProductSearch(1)

	//fmt.Println("GET Response:")
	//ex := csv.Capacitor{}
	//ex.PrintFields()
}
