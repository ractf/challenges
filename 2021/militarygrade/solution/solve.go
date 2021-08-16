package main

import (
	"crypto/aes"
	"crypto/cipher"
	"encoding/hex"
	"fmt"
	"io/ioutil"
	"log"
	"math/rand"
	"net/http"
	"strings"
)

func main() {
	resp, err := http.Get("http://localhost:8080/")
	if err != nil {
		log.Fatalln(err)
	}

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		log.Fatalln(err)
	}

	ctext, err := hex.DecodeString(string(body))
	if err != nil {
		panic(err)
	}

	i := int64(0)
	for i < 16781311 {
		rand.Seed(i)
		for j := 0; j < rand.Intn(32); j++ {
			rand.Seed(rand.Int63())
		}
		var key []byte
		var iv []byte

		for j := 0; j < 32; j++ {
			key = append(key, byte(rand.Intn(255)))
		}

		for j := 0; j < aes.BlockSize; j++ {
			iv = append(iv, byte(rand.Intn(255)))
		}

		block, err := aes.NewCipher(key)
		if err != nil {
			panic(err)
		}
		mode := cipher.NewCBCDecrypter(block, iv)
		out := make([]byte, len(ctext))
		mode.CryptBlocks(out, ctext)

		if strings.HasPrefix(string(out), "ractf") {
			fmt.Println(string(out))
			return
		}

		if i == 4095 {
			i = 16777216
		} else {
			i++
		}
	}
}
