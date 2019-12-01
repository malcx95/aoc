use std::fs::File;
use std::io::{self, prelude::*, BufReader};

fn read_file(name: &str) -> Vec<String> {
    let mut lines = vec!();

    let file = File::open(name).unwrap();
    let reader = BufReader::new(file);

    for line in reader.lines() {
        lines.push(line.unwrap());
    }
    lines
}

fn calc_fuel(mass: u32) -> u32 {
    (((mass as f32)/3.).floor() as u32) - 2
}

fn main() {
    let masses: Vec<u32> = read_file("input").iter()
        .map(|m| m.parse::<u32>().unwrap()).collect();
    let total_fuel = masses.iter().fold(0, |tot, next| tot + calc_fuel(*next));
    println!("Total fuel: {}", total_fuel);
}
