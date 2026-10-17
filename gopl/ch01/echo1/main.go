package main

// Echo1 prints its command-line arguments.

import (
	"fmt"
	"os"
)

func main() {
	var s string
	for i := 1; i < len(os.Args); i++ {
		s = os.Args[i]
	}
	fmt.Println(s)
}
