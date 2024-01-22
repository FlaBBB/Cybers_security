package v2

import (
	"context"
	"crypto/sha256"
	"fmt"
	"math/rand"
	"sync/atomic"
	"time"
)

var (
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

func worker(ctx context.Context, start, end uint64, difficulty, id int, found chan uint64) {
	hash := sha256.New()

	for i := start; i < end; i++ {
		select {
		case <-ctx.Done():
			return
		default:
			hash.Reset()
			hash.Write([]byte(fmt.Sprintf("%d", i)))
			digest := hash.Sum(nil)

			if checkZeroPadding(digest, difficulty) {
				fmt.Printf("\nThread %d found the Ticket: %d\n", id, i)
				fmt.Printf("Average speed: %.2f H/s\n", float64(atomic.LoadUint64(&totalCount))/time.Now().Sub(startTime).Seconds())
				found <- i
				return
			}

			atomic.AddUint64(&totalCount, 1)
		}
	}
}

func printSpeed(ctx context.Context, range_ uint64) {
	begin := time.Now()
	lastCount := atomic.LoadUint64(&totalCount)

	for {
		select {
		case <-ctx.Done():
			return
		default:
			time.Sleep(time.Second)
			now := time.Now()
			currentCount := atomic.LoadUint64(&totalCount)
			speed := float64(currentCount-lastCount) / now.Sub(begin).Seconds()
			progress := float64(currentCount) / float64(range_) * 100
			fmt.Printf("\rProgress: %d/%d\t%.2f%%\tTotal speed: %.2f H/s", currentCount, range_, progress, speed)
			begin = now
			lastCount = currentCount
		}
	}
}

func Run_v2() {
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

	startTime = time.Now()
	found := make(chan uint64, 1)
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	for i := uint64(0); i < numThreads; i++ {
		go worker(ctx, x+i*range_/numThreads, x+(i+1)*range_/numThreads, difficulty, int(i), found)
	}

	go printSpeed(ctx, range_)

	fmt.Printf("\nTicket found: %d\n", <-found)
	cancel()
}
