package main

import (
	"crypto/rand"
	"encoding/hex"
	"fmt"
	"os"

	ecies "github.com/ecies/go/v2"
)

func check(e error) {
	if e != nil {
		fmt.Println("Hacker detected!")
		os.Exit(1)
	}
}

func main() {

	flag, err := os.ReadFile("flag.txt")
	if err != nil {
		panic(err)
	}

	d := make([]byte, 16)
	rand.Read(d)
	serverKey := ecies.NewPrivateKeyFromBytes(d)
	if err != nil {
		panic(err)
	}

	ciphertext, err := ecies.Encrypt(serverKey.PublicKey, flag)
	if err != nil {
		panic(err)
	}
	fmt.Print("Encrypted flag: ")
	fmt.Println(hex.EncodeToString(ciphertext))

	banner := `
[1] Generate key pair
[2] Encrypt message
[3] Decrypt message
[0] Exit
`

	var input int
	for {
		fmt.Println(banner)
		fmt.Print("> ")
		fmt.Scan(&input)

		if input == 1 {
			k, err := ecies.GenerateKey()
			check(err)
			fmt.Print("Private key: ")
			fmt.Println(k.Hex())
			fmt.Print("Public key: ")
			fmt.Println(k.PublicKey.Hex(true))

		} else if input == 2 {
			var pubinput string
			var msginput string
			fmt.Print("Enter your public key: ")
			fmt.Scan(&pubinput)
			fmt.Print("Enter the message you want to encrypt (hex): ")
			fmt.Scan(&msginput)

			plaintext, err := hex.DecodeString(msginput)
			check(err)

			userPub, err := ecies.NewPublicKeyFromHex(pubinput)
			check(err)

			ephemeralSecret, err := serverKey.ECDH(userPub)
			check(err)

			fmt.Print("Shared ephemeral secret: ")
			fmt.Println(hex.EncodeToString(ephemeralSecret))

			ciphertext, err := ecies.Encrypt(userPub, plaintext)
			check(err)

			fmt.Print("Encrypted message: ")
			fmt.Println(hex.EncodeToString(ciphertext))

		} else if input == 3 {
			var privinput string
			var msginput string
			fmt.Print("Enter your private key: ")
			fmt.Scan(&privinput)
			fmt.Print("Enter the ciphertext you want to decrypt (hex): ")
			fmt.Scan(&msginput)

			ciphertext, err := hex.DecodeString(msginput)
			check(err)

			userPriv, err := ecies.NewPrivateKeyFromHex(privinput)
			check(err)

			ephemeralSecret, err := userPriv.ECDH(serverKey.PublicKey)
			check(err)

			fmt.Print("Shared ephemeral secret: ")
			fmt.Println(hex.EncodeToString(ephemeralSecret))

			plaintext, err := ecies.Decrypt(userPriv, ciphertext)
			if err != nil {
				fmt.Println("Invalid private key/ciphertext")
			} else {
				fmt.Print("Decrypted message: ")
				fmt.Println(hex.EncodeToString(plaintext))
			}

		} else {
			break
		}

	}
}
