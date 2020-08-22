use std::env;
fn main(){
    let env_args= env::args();

    let args:Vec<String> = env_args.collect();
    let first_arg = &args[1];

    if first_arg == "hello" {
        println!("Hello world");
    }else {
        println!("First arg is not hello");
    }
}
