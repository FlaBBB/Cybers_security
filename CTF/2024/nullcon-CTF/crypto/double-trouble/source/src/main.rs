use std::io::Write;

use aes_gcm::{
    aead::{Aead, AeadCore, KeyInit, OsRng},
    Aes256Gcm,
};

const FLAG: &str = "ENO{repl4c3_m3}";

fn encrypt(message: &[u8], key: &[u8]) -> Vec<u8> {
    message
        .iter()
        .enumerate()
        .map(|(i, m)| m ^ key[i % 32])
        .collect()
}

fn main() {
    let key = Aes256Gcm::generate_key(OsRng);
    let cipher = Aes256Gcm::new(&key);
    let nonce = Aes256Gcm::generate_nonce(&mut OsRng);

    let encrypted = cipher.encrypt(&nonce, FLAG.as_ref()).unwrap();
    println!("{:?}", encrypted);

    println!("Key: 0x{}", hex::encode(&key));
    println!("Nonce: 0x{}", hex::encode(&nonce));
    println!(
        "Ciphertext: 0x{}",
        // hex::encode(&nonce),
        hex::encode(&encrypted)
    );

    let mut message = String::new();
    print!("Let me encrypt one more thing for you: ");
    std::io::stdout().flush().unwrap();
    std::io::stdin().read_line(&mut message).unwrap();

    println!("{}", hex::encode(&message));
    if message.len() > 29 {
        println!("Woah! That's too long for me :^)");
        return;
    }

    println!("0x{}", hex::encode(encrypt(message.as_ref(), key.as_ref())));
}
