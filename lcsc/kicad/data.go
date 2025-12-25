package kicad

import (
	"lcsc/csv"
)

type Field struct {
	Column            string `json:"column"`
	Name              string `json:"name"`
	VisibleOnAdd      bool   `json:"visible_on_add"`
	VisibleInChooser  bool   `json:"visible_in_chooser"`
	ShowName          bool   `json:"show_name"`
	InheritProperties bool   `json:"inherit_properties,omitempty"`
}

type Property struct {
	Description      string `json:"description"`
	FootprintFilters string `json:"footprint_filters"`
	Keywords         string `json:"keywords"`
	ExcludeFromBom   string `json:"exclude_from_bom"`
	ExcludeFromBoard string `json:"exclude_from_board"`
}

type Library struct {
	Name       string   `json:"name"`
	Table      string   `json:"table"`
	Key        string   `json:"key"`
	Symbols    string   `json:"symbols"`
	Footprints string   `json:"footprints"`
	Fields     []Field  `json:"fields"`
	Properties Property `json:"properties"`
}

type Database struct {
	Meta struct {
		Version int `json:"version"`
	} `json:"meta"`
	Name        string `json:"name"`
	Description string `json:"description"`
	Source      struct {
		Type             string `json:"type"`
		Dsn              string `json:"dsn"`
		Username         string `json:"username"`
		Password         string `json:"password"`
		TimeoutSeconds   int    `json:"timeout_seconds"`
		ConnectionString string `json:"connection_string"`
	} `json:"source"`
	Libraries []Library `json:"libraries"`
}

func stringInSlice(a string, list []string) bool {
	for _, b := range list {
		if b == a {
			return true
		}
	}
	return false
}

func FieldCapacitor() []Field {
	strs := []string{"Value", "Voltage", "Material", "Tolerance"}
	fields := []Field{}
	ex := csv.Capacitor{}
	tags := ex.GetTags()
	for _, v := range tags {
		f := Field{
			Column:            v,
			Name:              v,
			VisibleOnAdd:      false,
			VisibleInChooser:  true,
			ShowName:          false,
			InheritProperties: false,
		}
		if stringInSlice(v, strs) {
			f.VisibleOnAdd = true
		}
		fields = append(fields, f)
		//fmt.Println(f)
	}
	return fields
}

func FieldResistor() []Field {
	strs := []string{"Value", "Tolerance", "Power"}
	fields := []Field{}
	ex := csv.Resistor{}
	tags := ex.GetTags()
	for _, v := range tags {
		f := Field{
			Column:            v,
			Name:              v,
			VisibleOnAdd:      false,
			VisibleInChooser:  true,
			ShowName:          true,
			InheritProperties: false,
		}
		if stringInSlice(v, strs) {
			f.VisibleOnAdd = true
		}
		fields = append(fields, f)
		//fmt.Println(f)
	}
	return fields
}

func LibraryCapacitor(names []string) []Library {
	libraries := []Library{}
	fields := FieldCapacitor()
	property := Property{
		Description:      "Description",
		FootprintFilters: "Footprint Filters",
		Keywords:         "Keywords",
		ExcludeFromBom:   "No BOM",
		ExcludeFromBoard: "Schematic Only",
	}
	for _, v := range names {
		lib := Library{
			Name:       v,
			Table:      v,
			Key:        "PartID",
			Symbols:    "Symbol",
			Footprints: "Footprint",
			Properties: property,
		}
		lib.Fields = append(lib.Fields, fields...)
		libraries = append(libraries, lib)
	}
	return libraries
}

func LibraryResistor(names []string) []Library {
	libraries := []Library{}
	fields := FieldResistor()
	property := Property{
		Description:      "Description",
		FootprintFilters: "Footprint Filters",
		Keywords:         "Keywords",
		ExcludeFromBom:   "No BOM",
		ExcludeFromBoard: "Schematic Only",
	}
	for _, v := range names {
		lib := Library{
			Name:       v,
			Table:      v,
			Key:        "PartID",
			Symbols:    "Symbol",
			Footprints: "Footprint",
			Properties: property,
		}
		lib.Fields = append(lib.Fields, fields...)
		libraries = append(libraries, lib)
	}
	return libraries
}
