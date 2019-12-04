const LOWER_BOUND: u32 = 158126;
const UPPER_BOUND: u32 = 624574;

fn extract_digits(num: u32) -> [u32; 6] {
    let mut digits = [0; 6];
    for i in 0..6 {
        digits[5 - i] = num/(10.0_f32.powi(i as i32).floor() as u32) % 10;
    }
    digits
}

fn is_correct(digits: [u32; 6]) -> bool {
    let mut prev = 0;
    let mut adj_groups = vec!();
    let mut curr_group = 1;
    for d in &digits {
        if *d < prev {
            return false;
        } else if *d == prev {
            curr_group += 1;
        } else if curr_group == 2 {
            adj_groups.push(curr_group);
            curr_group = 1;
        } else {
            curr_group = 1;
        }
        prev = *d;
    }
    adj_groups.len() > 0 || curr_group == 2
}

fn main() {
    let result = (LOWER_BOUND..=UPPER_BOUND).filter(|n| is_correct(extract_digits(*n)));
    println!("Result: {}", result.count());
}
