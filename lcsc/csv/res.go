package csv

import (
	"lcsc/response"
	"reflect"
	"strconv"
	"strings"
)

type Resistor struct {
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
	Resistance       string `csv:"Resistance"`
	Power            string `csv:"Power"`
	Tolerance        string `csv:"Tolerance"`
	Stock            string `csv:"Stock"`
	Datasheet        string `csv:"Datasheet"`
}

func edit(value string) string {
	result := ""
	if strings.HasSuffix(value, "mΩ") {
		str := strings.Replace(value, "mΩ", "", -1)
		if strings.Contains(str, ".") {
			s := strings.Split(str, ".")
			result = s[0] + "m" + s[1] + "R"
		} else {
			result = str + "mR"
		}
	} else if strings.HasSuffix(value, "kΩ") {
		str := strings.Replace(value, "kΩ", "", -1)
		if strings.Contains(str, ".") {
			s := strings.Split(str, ".")
			result = s[0] + "K" + s[1]
		} else {
			result = str + "K"
		}
	} else if strings.HasSuffix(value, "MΩ") {
		str := strings.Replace(value, "MΩ", "", -1)
		if strings.Contains(str, ".") {
			s := strings.Split(str, ".")
			result = s[0] + "M" + s[1]
		} else {
			result = str + "M"
		}
	} else {
		str := strings.Replace(value, "Ω", "", -1)
		if strings.Contains(str, ".") {
			s := strings.Split(str, ".")
			result = s[0] + "R" + s[1]
		} else {
			result = str + "R"
		}
	}
	return result
}

func (c *Resistor) MapValue(size string, product response.ProductData) {
	c.PartID = product.ProductCode
	c.Description = product.ProductIntroEn
	c.Category = "Resistor"
	c.Symbol = "symbol:R0402"
	c.Footprint = "footprint:R" + size
	c.Distributor = "LCSC"
	c.DistributorPart = product.ProductCode
	c.Manufacturer = product.BrandNameEn
	c.ManufacturerPart = product.ProductModel
	c.Package = "C" + product.EncapStandard
	c.Datasheet = product.PdfURL
	c.Stock = strconv.Itoa(product.StockNumber)

	for _, v := range product.ParamVOList {
		if v.ParamNameEn == "Power(Watts)" {
			c.Power = v.ParamValueEn
		}
		if v.ParamNameEn == "Resistance" {
			c.Value = edit(v.ParamValueEn)
			c.Resistance = v.ParamValueEn
		}
		if v.ParamNameEn == "Tolerance" {
			c.Tolerance = v.ParamValueEn
		}
	}
}
func (c Resistor) GetTags() []string {
	headers := []string{}
	//e := reflect.ValueOf(c)
	e := reflect.ValueOf(&c).Elem()

	for i := 0; i < e.NumField(); i++ {
		tag := e.Type().Field(i).Tag.Get("csv")
		headers = append(headers, tag)
	}
	return headers
}

func (c Resistor) GetValues() []string {
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
