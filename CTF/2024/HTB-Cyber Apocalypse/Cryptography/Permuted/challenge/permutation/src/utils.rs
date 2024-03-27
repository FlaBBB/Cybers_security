use num_bigint::BigUint;
use num_traits::{One, ToPrimitive, Zero};


pub fn gcd(a: BigUint, b: BigUint) -> BigUint {
    if b.is_zero() {
        return a;
    }
    gcd(b.clone(), a % b.clone())
}

fn _lcm(nums: &[BigUint]) -> BigUint {
    if nums.len() == 1 {
        return nums[0].clone();
    }
    let a = nums[0].clone();
    let b = _lcm(&nums[1..]);
    a.clone() * b.clone() / gcd(a.clone(), b.clone())
}

pub fn lcm(nums: &[usize]) -> BigUint {
    let nums: Vec<BigUint> = nums.iter().map(|x| BigUint::from(*x)).collect();
    _lcm(&nums)
}

fn update_step(a: &mut BigUint, old_a: &mut BigUint, quotient: BigUint) {
    let temp = &a.clone();
    *a = old_a.clone() - quotient * temp.clone();
    *old_a = temp.clone();
}

pub fn extended_euclidean_algorithm(a: BigUint, b: BigUint) -> (BigUint, BigUint, BigUint) {
    let (mut old_r, mut rem) = (a, b);
    let (mut old_s, mut coeff_s) = (BigUint::from(1u8), BigUint::from(1u8));
    let (mut old_t, mut coeff_t) = (BigUint::from(1u8), BigUint::from(1u8));

    while !rem.is_zero() {
        let quotient = &old_r / &rem;

        update_step(&mut rem, &mut old_r, quotient.clone());
        update_step(&mut coeff_s, &mut old_s, quotient.clone());
        update_step(&mut coeff_t, &mut old_t, quotient.clone());
    }

    (old_r, old_s, old_t)
}

pub fn mod_inv(x: BigUint, n: BigUint) -> Option<BigUint> {
    let (g, x, _) = extended_euclidean_algorithm(x, n.clone());
    if g.is_one() {
        Some((x % &n + &n) % &n)
    } else {
        None
    }
}

pub fn chinese_remainder_theorem(residues: &[BigUint], modulli: &[BigUint]) -> Option<BigUint> {
    let prod = modulli.iter().product::<BigUint>();

    let mut sum = BigUint::from(0u8);

    for (&ref residue, &ref modulus) in residues.iter().zip(modulli) {
        let p:BigUint = &prod / modulus;
        sum += residue * mod_inv(p.clone(), modulus.clone())? * p
    }
    Some(sum % prod)
}