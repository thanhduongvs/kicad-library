package kicad

import (
	"encoding/json"
	"io/ioutil"
)

func InitData() {
	data := Database{}
	data.Name = "OneKiwi Database Library"
	data.Description = "OneKiwi database of components"
	data.Meta.Version = 0
	data.Source.Type = "odbc"
	data.Source.Dsn = ""
	data.Source.Username = ""
	data.Source.Password = ""
	data.Source.TimeoutSeconds = 10
	data.Source.ConnectionString = "Driver=SQLite3;DATABASE=/home/vanson/onekiwi-kicad-library/lcsc/onekiwi.sqlite"

	caps := []string{"Cap0201", "Cap0402", "Cap0603", "Cap0805", "Cap1206", "Cap1210"}
	ress := []string{"Res0201", "Res0402", "Res0603", "Res0805", "Res1206", "Res1210"}
	libcaps := LibraryCapacitor(caps)
	libress := LibraryCapacitor(ress)
	data.Libraries = append(data.Libraries, libcaps...)
	data.Libraries = append(data.Libraries, libress...)

	file, _ := json.MarshalIndent(data, "", "    ")

	_ = ioutil.WriteFile("onekiwi.kicad_dbl", file, 0644)
}
