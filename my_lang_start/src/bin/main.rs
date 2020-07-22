//use my_rust_std;
use std::env;
//use std::ptr;
//use std::sync::atomic::{AtomicIsize, AtomicPtr, Ordering};

fn main(){
    let args = env::args();
    println!("{:?}", args);

    //static my_ARGC: AtomicIsize = AtomicIsize::new(0);
    //static my_ARGV: AtomicPtr<*const u8> = AtomicPtr::new(ptr::null_mut());

    //let argc:isize = my_ARGC.load(Ordering::Relaxed);
    //let argv:*const *const u8 = my_ARGV.load(Ordering::Relaxed);

    println!("hello world");
}