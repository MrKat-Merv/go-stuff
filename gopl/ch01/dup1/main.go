// Dup1 prints the text of each line that appears more than
// once in the statndard input, preceded by its count.
package main

import (
	"bufio"
	"fmt"
	"os"
)

func main() {
	counts := make(map[string]int)
	input := bufio.NewScanner(os.Stdin)
	for input.Scan() {
		counts[input.Text()]++
	}
	// NOTE: ignoring potential errors from input.Err()
	// Not ignoring potential errors from input.Err() because the program is simple and for 
	// demonstration purposes. In a production environment, you should handle errors appropriately.
	// if err := input.Err(); err != nil {
	//	fmt.Fprintf(os.Stderr, "reading standard input: %v\n", err)
	//	os.Exit(1)
	//}
	fmt.Printf("\nRaw count map: %v\n\n", counts)
	for line, n := range counts {
		if n > 1 {
			fmt.Printf("%d\t%s\n", n, line)
		}
	}
}