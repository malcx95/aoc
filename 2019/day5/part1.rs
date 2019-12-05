use std::fs::File;
use std::io::{self, prelude::*, BufReader};

fn read_file(name: &str) -> Vec<i32> {
    let file = File::open(name).unwrap();
    let reader = BufReader::new(file);
    let line = reader.lines().next().unwrap().unwrap();
    line.as_str().split(",").map(|m| m.parse::<i32>().unwrap()).collect()
}

fn execute_instruction(program: &mut Vec<i32>, program_counter: usize) -> bool {
    if program[program_counter] == 99 {
        false
    } else {
        let op1 = program[program_counter + 1];
        let op2 = program[program_counter + 2];
        let dest = program[program_counter + 3];
        if program[program_counter] == 1 {
            program[dest as usize] = program[op1 as usize] + program[op2 as usize];
        } else if program[program_counter] == 2 {
            program[dest as usize] = program[op1 as usize] * program[op2 as usize];
        }
        true
    }
}

fn main() {
    let mut program = read_file("input");
    let mut program_counter = 0;
    while execute_instruction(&mut program, program_counter) {
        program_counter += 4;
    }
    println!("Program at position 0: {}", program[0]);
}
