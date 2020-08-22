fn main() {
    let a = "ab";
    for b in a.as_bytes(){
        println!("{}", b);
    }

    println!("{}", a.len());

    let pointer =  a.as_ptr();
    unsafe {
        println!("{:?}", *pointer);
    }
}