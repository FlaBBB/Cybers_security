package v1

import (
	"crypto/sha256"
	"fmt"
	"math/rand"
	"sync"
	"time"
)

var (
	found      bool
	totalCount uint64
	startTime  time.Time
)

func checkZeroPadding(digest []byte, difficulty int) bool {
	for i := 0; i < difficulty/2; i++ {
		if digest[i] != 0 {
			return false
		}
	}
	if difficulty%2 == 1 {
		return digest[difficulty/2] <= 0x0f
	}
	return digest[difficulty/2] > 0x0f
}

func worker(start, end uint64, difficulty, id int, wg *sync.WaitGroup) {
	defer wg.Done()

	hash := sha256.New()

	for i := start; i < end && !found; i++ {
		hash.Reset()
		hash.Write([]byte(fmt.Sprintf("%d", i)))
		digest := hash.Sum(nil)

		hash.Reset()
		hash.Write(append(digest, []byte(fmt.Sprintf("%d", i))...))
		digest = hash.Sum(nil)

		if checkZeroPadding(digest, difficulty) {
			fmt.Printf("\nThread %d found the Ticket: %d\n", id, i)
			fmt.Printf("Average speed: %.2f H/s\n", float64(totalCount)/time.Now().Sub(startTime).Seconds())
			found = true
		}

		totalCount++
	}
}

func printSpeed(range_ uint64) {
	begin := time.Now()
	lastCount := totalCount

	for !found {
		time.Sleep(time.Second)
		now := time.Now()
		currentCount := totalCount
		speed := float64(currentCount-lastCount) / now.Sub(begin).Seconds()
		progress := float64(currentCount) / float64(range_) * 100
		fmt.Printf("\rProgress: %d/%d\t%.2f%%\tTotal speed: %.2f H/s", currentCount, range_, progress, speed)
		begin = now
		lastCount = currentCount
	}
}

func Run_v1() {
	var difficulty int
	fmt.Print("Difficulty: ")
	_, err := fmt.Scan(&difficulty)
	if err != nil {
		panic(err)
	}

	if difficulty < 1 || difficulty > 32 {
		panic("Difficulty must be between 1 and 32")
	}

	x := uint64(100000000 + rand.Intn(200000000000))
	range_ := uint64(20000000000)
	var numThreads uint64
	fmt.Print("Number of threads: ")
	_, err = fmt.Scan(&numThreads)
	if err != nil {
		panic(err)
	}

	var wg sync.WaitGroup
	wg.Add(int(numThreads))

	startTime = time.Now()
	for i := uint64(0); i < numThreads; i++ {
		go worker(x+i*range_/numThreads, x+(i+1)*range_/numThreads, difficulty, int(i), &wg)
	}

	go printSpeed(range_)

	wg.Wait()
}
