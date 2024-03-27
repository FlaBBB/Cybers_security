package main

import (
	"crypto/rand"
	"encoding/hex"
	"errors"
	"fmt"
	"log"
	"os"
	"time"

	ecies "github.com/ecies/go/v2"
)

func xor(data []byte, key []byte) []byte {
	for i := 0; i < len(data); i++ {
		data[i] ^= key[i%len(key)]
	}
	return data
}

func alice_client(d []byte, ch chan string, e chan<- error) {
	A := ecies.NewPrivateKeyFromBytes(d)
	ch <- A.PublicKey.Hex(true)
	time.Sleep(2 * time.Second)

	recv, ok := <-ch
	if !ok {
		e <- errors.New("channel closed")
		return
	}
	B, err := ecies.NewPublicKeyFromHex(recv)
	if err != nil {
		e <- errors.New("error pubkey")
		return
	}
	ss, err := A.ECDH(B)
	if err != nil {
		e <- errors.New("error secret")
		return
	}

	for i := range alice_says {
		enc := hex.EncodeToString(xor([]byte(alice_says[i]), ss))
		ch <- enc
		time.Sleep(2 * time.Second)

		recv, ok := <-ch
		if !ok {
			e <- errors.New("channel closed")
			return
		}
		data, err := hex.DecodeString(recv)
		if err != nil {
			e <- errors.New("error decoding")
			return
		}
		data = xor(data, ss)
	}
	e <- nil
}

func bobby_client(d []byte, ch chan string, e chan<- error) {
	B := ecies.NewPrivateKeyFromBytes(d)
	recv, ok := <-ch
	if !ok {
		e <- errors.New("channel closed")
		return
	}
	A, err := ecies.NewPublicKeyFromHex(recv)
	if err != nil {
		e <- errors.New("error pubkey")
		return
	}
	ch <- B.PublicKey.Hex(true)
	time.Sleep(2 * time.Second)

	ss, err := B.ECDH(A)
	if err != nil {
		e <- errors.New("error secret")
		return
	}

	for i := range bobby_says {
		recv, ok = <-ch
		if !ok {
			e <- errors.New("channel closed")
			return
		}
		data, err := hex.DecodeString(recv)
		if err != nil {
			e <- errors.New("error decoding")
			return
		}
		data = xor(data, ss)

		enc := hex.EncodeToString(xor([]byte(bobby_says[i]), ss))
		ch <- enc
		time.Sleep(2 * time.Second)
	}
	e <- nil
}

func main() {
	secret_of_alice := make([]byte, 16)
	secret_of_bobby := make([]byte, 16)

	_, err := rand.Read(secret_of_alice)
	if err != nil {
		log.Fatalf("error reading from random")
	}
	_, err = rand.Read(secret_of_bobby)
	if err != nil {
		log.Fatalf("error reading from random")
	}

	D := ecies.NewPrivateKeyFromBytes(append(secret_of_alice, secret_of_bobby...))
	encflag, err := ecies.Encrypt(D.PublicKey, []byte(flag))
	if err != nil {
		log.Fatalf("error encrypting flag")
	}

	var ch chan string
	var e chan error
	go func() {
		generate() // generating stuff to talk about
		i := 1
		for {
			ch = make(chan string)
			e = make(chan error)
			go alice_client(secret_of_alice, ch, e)
			go bobby_client(secret_of_bobby, ch, e)
			if err := <-e; err != nil {
				close(ch) // restarting connection
			} else {
				break
			}
			i++
		}
	}()

	for {
		fmt.Println("MiTM Interface")
		fmt.Println("> Press 1 to intercept communication")
		fmt.Println("> Press 2 to receive flag")
		fmt.Println("> Press 3 to exit interface")
		fmt.Print("# ")

		var option string
		fmt.Scanln(&option)
		switch option {
		case "1":
			fmt.Println("intercepting...")
			var data string
			data = <-ch
			fmt.Println("you recieved: ", data)
			fmt.Print("send data: ")
			fmt.Scanln(&data)
			ch <- data
		case "2":
			fmt.Println("Here's your flag: ", hex.EncodeToString(encflag))
		case "3":
			os.Exit(0)
		default:
			fmt.Println("read info properly")
		}
	}
}
