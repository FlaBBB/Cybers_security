use std::ops::Index;
use num_bigint::BigUint;
use crate::utils::{lcm, chinese_remainder_theorem};

#[derive(Eq, Hash, Clone)]
pub struct Permutation {
    pub mapping: Vec<usize>,
    pub cycles: Vec<Vec<usize>>,
    pub max_cycle: BigUint,
}

impl Permutation {
    pub fn new(mapping: Vec<usize>) -> Self {
        let length = mapping.len();
        assert_eq!(
            mapping
                .iter()
                .cloned()
                .collect::<std::collections::HashSet<_>>()
                .len(),
            length
        ); // ensure it contains all numbers from 0 to length-1, with no repetitions

        let mut cycles = vec![];
        let mut not_visited = (0..mapping.len()).collect::<Vec<usize>>();
        while not_visited.len() > 0 {
            let initial = not_visited[0];
            let mut cycle = vec![initial];
            let mut cur = mapping[initial];
            not_visited.retain(|&x| x != initial);
            while cur != initial {
                cycle.push(cur);
                not_visited.retain(|&x| x != cur);
                cur = mapping[cur];
            }
            cycles.push(cycle);
        }

        let cycle_num:Vec<usize> = cycles.iter().map(|x| x.len()).collect();
        let max_cycle = lcm(&cycle_num);

        Self { mapping, cycles, max_cycle }
    }

    pub fn identity(length: usize) -> Self {
        Self::new((0..length).collect())
    }

    pub fn inverse(&self) -> Self {
        let mut ans = vec![0; self.mapping.len()];
        for (i, &val) in self.mapping.iter().enumerate() {
            ans[val] = i;
        }

        let cycles = self.cycles.iter().map(|x| x.iter().cloned().rev().collect()).collect();

        return Self { mapping: ans, cycles, max_cycle: self.max_cycle.clone() };
    }

    pub fn compose(&self, other: &Permutation) -> Permutation {
        let mut ans = vec![0; self.mapping.len()];
        for (i, &val) in self.mapping.iter().enumerate() {
            ans[i] = other.mapping[val];
        }
        return Permutation::new(ans);
    }

    pub fn pow(&self, mut power: usize) -> Permutation {
        let mut ans = vec![0; self.mapping.len()];
        for cycle in &self.cycles {
            for (i, &val) in cycle.iter().enumerate() {
                ans[val] = cycle[(i + power) % cycle.len()];
            }
        }
        Self::new(ans)
    }

    pub fn log(&self, g: &Permutation) -> Option<BigUint> {
        let mut remainder = vec![];
        let mut modulus = vec![];
        for cycle in &self.cycles {
            let c = cycle[0];
            remainder.push(BigUint::from(cycle.iter().position(|&r| r==self.mapping[c]).unwrap() % cycle.len()));
            modulus.push(BigUint::from(cycle.len()));
        }
        let ans = chinese_remainder_theorem(&remainder, &modulus).unwrap();
        Some(BigUint::from(ans) % self.max_cycle.clone())
    }
}

impl PartialEq for Permutation {
    fn eq(&self, other: &Self) -> bool {
        self.mapping == other.mapping
    }
}

impl std::fmt::Display for Permutation {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{:?}", self.mapping)
    }
}

impl std::fmt::Debug for Permutation {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{:?}", self.mapping)
    }
}
