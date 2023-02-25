use std::env;
use std::process::Command;

fn main() {
    let args: Vec<String> = env::args().collect();
    
    if args.len() < 2 {
        return;
    }
    if args[1] == "init" {
        dfm_init(args);
    }

}

fn dfm_init(args: Vec<String>) {
    let output = Command::new("sh")
        .arg("-c")
        .arg("echo hello")
        .output()
        .expect("failed to execute process");
    println!("{:?}",output.stdout);
}
