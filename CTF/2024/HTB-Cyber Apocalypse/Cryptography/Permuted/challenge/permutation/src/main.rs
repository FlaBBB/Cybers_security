pub mod permutation;
pub mod utils;

use permutation::Permutation;

use std::fs;
use rand::prelude::*;
use std::time::Instant;
//
use std::arch::x86_64::*;

fn finding() {
    let content = fs::read_to_string("/mnt/d/Programming/CySec/Cyber Security/CTF/2024/HTB-Cyber Apocalypse/Cryptography/Permuted/challenge/permutation/output.txt").expect("Failed to read file");
    let content = content.trim().split("\n").collect::<Vec<&str>>();

    let pat: &[_] = &['[',']'];
    let g = Permutation::new(content[0].split(" = ").collect::<Vec<&str>>()[1].trim_matches(pat).split(", ").map(|x| x.parse::<usize>().unwrap()).collect::<Vec<usize>>());
    // let A = Permutation::new(content[2].split(" = ").collect::<Vec<&str>>()[1].trim_matches(pat).split(", ").map(|x| x.parse::<usize>().unwrap()).collect::<Vec<usize>>());
    let B = Permutation::new(content[4].split(" = ").collect::<Vec<&str>>()[1].trim_matches(pat).split(", ").map(|x| x.parse::<usize>().unwrap()).collect::<Vec<usize>>());
    let b = B.log(&g);
    println!("{:?}", b);
}

fn testing() {
    let n = 400;
    let mut g = (0..n as usize).collect::<Vec<usize>>();
    g.shuffle(&mut thread_rng());
    let g = Permutation::new(g);

    let start = Instant::now();

    let r = g.pow(233);
    let log_r = r.log(&g);
    println!("{:?}", log_r);

    let elapsed = start.elapsed();
    let elapsed_sec = elapsed.as_secs();
    let elapsed_milis = elapsed.subsec_millis();
    println!("Elapsed time: {} seconds {} milliseconds", elapsed_sec, elapsed_milis);
}

fn try_simd() {
    let input: &[u16] = &[512, 50000, 0, 1, 5224, 12535, 52637, 2332];
    let shuffler: &[u16] = &[7, 2, 5, 4, 1, 3, 0, 6];

    let mut _shuffler: &mut [u8; 16] = &mut [0; 16];
    let mut _input: &mut [u8; 16] = &mut [0; 16];
    for i in 0..8 {
        _input[2 * i] = (input[i] & 0xFF) as u8;
        _input[2 * i + 1] = ((input[i] >> 8) & 0xFF) as u8;
        _shuffler[2 * i] = (2 * shuffler[i]) as u8;
        _shuffler[2 * i + 1] = (2 * shuffler[i] + 1) as u8;
    }

    // Safety: We assume the length of the vectors and shuffle control match
    let mut _output: [u8; 16] = [0; 16];
    unsafe {
        let in1_vec = _mm_loadu_si128(_input.as_ptr() as *const __m128i);
        let shuffle_vec = _mm_loadu_si128(_shuffler.as_ptr() as *const __m128i);
        let result = _mm_shuffle_epi8(in1_vec, shuffle_vec);

        // Print the result (may require casting depending on your needs)
        _mm_storeu_si128(_output.as_mut_ptr() as *mut __m128i, result);
    }

    let mut output: [u16; 8] = [0; 8];
    for i in 0..8 {
        output[i] = (_output[2 * i] as u16) + ((_output[2 * i + 1] as u16) << 8);
    }
    println!("Permuted result: {:?}", output);
}

fn spin_words(words: &str) -> String {
    words.split(" ").collect::<Vec<&str>>().iter().map(|x| if x.len() >= 5 { x.chars().rev().collect::<String>() } else { x.to_string() }).collect::<Vec<String>>().join(" ")
}

fn main() {
    testing();
}
