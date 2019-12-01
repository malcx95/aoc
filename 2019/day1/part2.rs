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

fn calc_fuel(mass: i32) -> i32 {
    (((mass as f32)/3.).floor() as i32) - 2
}

fn calc_accumulated_fuel(mass: i32) -> i32 {
    let mut total_fuel = calc_fuel(mass);
    let mut curr_mass = total_fuel;
    loop {
        let fuel = calc_fuel(curr_mass);
        curr_mass = fuel;
        if curr_mass < 0 {
            return total_fuel;
        }
        total_fuel += fuel;
    }
}

fn main() {
    let masses: Vec<i32> = read_file("input").iter()
        .map(|m| m.parse::<i32>().unwrap()).collect();
    let total_fuel = masses.iter().fold(0, |tot, next| tot + calc_accumulated_fuel(*next));
    println!("Total fuel: {}", total_fuel);
}
