package main

import (
	"fmt"
	"strings"
)

func test(value string) string {
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
func main() {
	strs := []string{
		"0.025mΩ",
		"1mΩ",
		"1.3mΩ",
		"380mΩ",
		"1Ω",
		"2.3Ω",
		"280.4Ω",
		"1kΩ",
		"56.7kΩ",
		"2MΩ",
		"5.89MΩ",
	}
	for _, v := range strs {
		a := test(v)
		fmt.Println(v, a)
	}

}
