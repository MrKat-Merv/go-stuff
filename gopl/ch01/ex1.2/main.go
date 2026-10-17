package main

// Ex1_2 prints its command-line arguments, one per line. with the index of the argument.

import (
	"fmt"
	"os"
)

func main() {
	var s string
	for i := 1; i < len(os.Args); i++ {
		s = os.Args[i]
		fmt.Println(i, s)
	}
}