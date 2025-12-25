package main

import (
	"fmt"
	"os"
	"power/data"
)

func main() {
	args := os.Args[1:]
	fmt.Println(args)
	if len(args) == 0 {
		fmt.Println("exit")
		return
	}

	for _, s := range args {
		data.CreatePower(data.PATH_POWER, data.PowerText, s)
		data.CreatePower(data.PATH_POWER_IN, data.PowerInText, s)
		data.CreatePower(data.PATH_POWER_OUT, data.PowerOutText, s)
	}
}
