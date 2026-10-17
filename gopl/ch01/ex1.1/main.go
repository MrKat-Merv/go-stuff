package main

// Echo1 prints its command-line arguments including the program name.

import (
	"fmt"
	"os"
)

func main() {
	var s string
	for i := 0; i < len(os.Args); i++ {
		s = os.Args[i]
	}
	fmt.Println(s)
}