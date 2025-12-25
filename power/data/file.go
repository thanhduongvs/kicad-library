package data

import (
	"bufio"
	"bytes"
	"fmt"
	"log"
	"os"
	"strings"
)

func DeleteLastLine(path string) {
	f, err := os.Open(path)
	if err != nil {
		log.Fatal(err)
	}
	defer f.Close()

	var bs []byte
	buf := bytes.NewBuffer(bs)

	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		if scanner.Text() != ")" {
			_, err := buf.Write(scanner.Bytes())
			if err != nil {
				log.Fatal(err)
			}
			_, err = buf.WriteString("\n")
			if err != nil {
				log.Fatal(err)
			}
		}
	}
	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	err = os.WriteFile(path, buf.Bytes(), 0666)
	if err != nil {
		log.Fatal(err)
	}
}

func CreatePower(path string, texts string, name string) {
	DeleteLastLine(path)
	text := strings.Replace(texts, "POWER_NAME", name, -1)
	file, err := os.OpenFile(path, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	filename := ""
	if strings.Contains(path, "symbol_power_in") {
		filename = "symbol_power_in"
	} else if strings.Contains(path, "symbol_power_out") {
		filename = "symbol_power_out"
	} else {
		filename = "symbol_power"
	}

	if err != nil {
		fmt.Println("Could not open file")
		return
	}

	defer file.Close()

	_, err2 := file.WriteString(text)

	if err2 != nil {
		fmt.Println("Could not write text to file")

	} else {
		//fmt.Println("Operation successful! Text has been appended to file")
		fmt.Printf("POWER_NAME: %s added to %s\n", name, filename)
	}
}
