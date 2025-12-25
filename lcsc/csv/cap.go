package csv

import (
	"lcsc/response"
	"reflect"
	"strconv"
)

type Capacitor struct {
	PartID           string `csv:"PartID"`
	Description      string `csv:"Description"`
	Category         string `csv:"Category"`
	Value            string `csv:"Value"`
	Symbol           string `csv:"Symbol"`
	Footprint        string `csv:"Footprint"`
	Distributor      string `csv:"Distributor"`
	DistributorPart  string `csv:"Distributor Part#"`
	Manufacturer     string `csv:"Manufacturer"`
	ManufacturerPart string `csv:"Manufacturer Part#"`
	Package          string `csv:"Package"`
	Capacitance      string `csv:"Capacitance"`
	Voltage          string `csv:"Voltage"`
	Material         string `csv:"Material"`
	Tolerance        string `csv:"Tolerance"`
	Stock            string `csv:"Stock"`
	Datasheet        string `csv:"Datasheet"`
}

func (c *Capacitor) MapValue(size string, product response.ProductData) {
	c.PartID = product.ProductCode
	c.Description = product.ProductIntroEn
	c.Category = "Capacitor"
	c.Symbol = "symbol:C0402"
	c.Footprint = "footprint:C" + size
	c.Distributor = "LCSC"
	c.DistributorPart = product.ProductCode
	c.Manufacturer = product.BrandNameEn
	c.ManufacturerPart = product.ProductModel
	c.Package = "C" + product.EncapStandard
	c.Datasheet = product.PdfURL
	c.Stock = strconv.Itoa(product.StockNumber)

	for _, v := range product.ParamVOList {
		if v.ParamNameEn == "Voltage Rated" {
			c.Voltage = v.ParamValueEn
		}
		if v.ParamNameEn == "Capacitance" {
			c.Value = v.ParamValueEn
			c.Capacitance = v.ParamValueEn
		}
		if v.ParamNameEn == "Temperature Coefficient" {
			c.Material = v.ParamValueEn
		}
		if v.ParamNameEn == "Tolerance" {
			c.Tolerance = v.ParamValueEn
		}
	}
}
func (c Capacitor) GetTags() []string {
	headers := []string{}
	//e := reflect.ValueOf(c)
	e := reflect.ValueOf(&c).Elem()

	for i := 0; i < e.NumField(); i++ {
		tag := e.Type().Field(i).Tag.Get("csv")
		headers = append(headers, tag)
	}
	return headers
}

func (c Capacitor) GetValues() []string {
	headers := []string{}
	//e := reflect.Indirect(reflect.ValueOf(&c))
	e := reflect.ValueOf(&c).Elem()

	for i := 0; i < e.NumField(); i++ {
		//tag := e.Type().Field(i).Tag.Get("csv")
		//varName := e.Type().Field(i).Name
		//varType := e.Field(i).Type
		v := e.Field(i).Interface().(string)
		headers = append(headers, v)
		//fmt.Printf("%v %v %v %v\n", tag, varName, varType, v)
	}
	return headers
}

func (c Capacitor) GetFields() []string {
	headers := []string{}
	//e := reflect.Indirect(reflect.ValueOf(&c))
	e := reflect.ValueOf(&c).Elem()

	for i := 0; i < e.NumField(); i++ {
		//tag := e.Type().Field(i).Tag.Get("csv")
		v := e.Type().Field(i).Name

		//v := e.Field(i).Interface().(string)
		headers = append(headers, v)
		//fmt.Printf("%v %v %v %v\n", tag, varName, varType, v)
	}
	return headers
}
