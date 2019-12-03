use std::fs::File;
use std::io::{self, prelude::*, BufReader};
use std::collections::{HashMap, HashSet};

enum WireStep {
    Up(i32),
    Down(i32),
    Left(i32),
    Right(i32),
}

fn read_file(name: &str) -> Vec<Vec<WireStep>> {
    let mut wires = vec!();

    let file = File::open(name).unwrap();
    let reader = BufReader::new(file);

    for l in reader.lines() {
        let line = l.unwrap();
        let split = line.as_str().split(",");
        let mut path = vec!();
        for step in split {
            // create WireSteps
            let dir_char = step.chars().next().unwrap();
            let amount = &step[1..].parse::<i32>().unwrap();
            if dir_char == 'U' {
                path.push(WireStep::Up(*amount));
            } else if dir_char == 'D' {
                path.push(WireStep::Down(*amount));
            } else if dir_char == 'L' {
                path.push(WireStep::Left(*amount));
            } else if dir_char == 'R' {
                path.push(WireStep::Right(*amount));
            }
        }
        wires.push(path);
    }
    wires
}

fn main() {
    let wires = read_file("input");

    let mut sets = vec!();

    for wire in &wires {
        let mut used_positions = HashMap::new();
        let mut curr = (0, 0);
        let mut dist = 0;
        for step in wire {
            let (dx, dy, a) = match step {
                WireStep::Up(amount) => (0, -1, amount),
                WireStep::Down(amount) => (0, 1, amount),
                WireStep::Left(amount) => (-1, 0, amount),
                WireStep::Right(amount) => (1, 0, amount),
            };
            let (cx, cy) = curr;
            for s in 1..(a+1) {
                dist += 1;
                curr = (cx + dx*s, cy + dy*s);
                used_positions.insert(curr, dist);
            }
        }
        sets.push(used_positions);
    }

    let positions1 = &sets[0];
    let positions2 = &sets[1];

    let set1: HashSet<&(i32, i32)> = positions1.keys().collect();
    let set2: HashSet<&(i32, i32)> = positions2.keys().collect();

    let intersections: HashSet<&&(i32, i32)> = set1.intersection(&set2).collect();

    let mut lowest_dist = std::i32::MAX;
    for ints in intersections.iter() {
        let dist1 = positions1.get(**ints).unwrap();
        let dist2 = positions2.get(**ints).unwrap();
        if dist1 + dist2 < lowest_dist {
            lowest_dist = dist1 + dist2;
        }
    }

    println!("Distance: {}", lowest_dist);
}
