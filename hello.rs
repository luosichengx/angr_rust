use std::env;
fn main(){
    let env_args= env::args();

    let args:Vec<String> = env_args.collect();
    let first_arg = &args[2];

    if first_arg == "1" {
        println!("Hello world");
    }else {
        println!("First arg is not 1");
    }
}
