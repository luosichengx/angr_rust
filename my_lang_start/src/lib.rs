//#![feature(termination_trait_lib)]

//use std::process;
//pub fn my_lang_start<T: process::Termination + 'static>(
//    main: fn() -> !,
//    argc: isize,
//    argv: *const *const u8,
//) -> isize{
//    main();
//    0
//}
use std::ffi::OsString;
use std::marker::PhantomData;
use std::vec;

pub struct RustArgs{
    iter: vec::IntoIter<OsString>,
    _dont_send_or_sync_me: PhantomData<*mut ()>,
}

impl Iterator for RustArgs {
    type Item = OsString;
    fn next(&mut self) -> Option<OsString> {
        self.iter.next()
    }
    fn size_hint(&self) -> (usize, Option<usize>) {
        self.iter.size_hint()
    }
}

impl ExactSizeIterator for RustArgs {
    fn len(&self) -> usize {
        self.iter.len()
    }
}

impl DoubleEndedIterator for RustArgs {
    fn next_back(&mut self) -> Option<OsString> {
        self.iter.next_back()
    }
}

#[no_mangle]
pub fn rust_args()->RustArgs{
    rust_imp::args()
}

#[no_mangle]
pub fn rust_init(argc: isize, argv: *const *const u8){
    unsafe{
        rust_imp::init(argc, argv);
    }
}

#[no_mangle]
pub fn add_one_test(argc: isize, argv: *const *const u8) -> isize{
    argc + 1
}

#[no_mangle]
pub fn mock_my_lang_start(
    main: fn() -> (),
    argc: isize,
    argv: *const *const u8
) -> isize{
    unsafe{
        rust_init(argc, argv);
    }
    main();
    0
}

pub mod rust_env{
    use super::*;
    #[no_mangle]
    pub struct StdArgs{
        inner: StdArgsOs,
    }

    impl Iterator for StdArgs {
        type Item = String;
        fn next(&mut self) -> Option<String> {
            self.inner.next().map(|s| s.into_string().unwrap())
        }
        fn size_hint(&self) -> (usize, Option<usize>) {
            self.inner.size_hint()
        }
    }

    impl DoubleEndedIterator for StdArgs {
        fn next_back(&mut self) -> Option<String> {
            self.inner.next_back().map(|s| s.into_string().unwrap())
        }
    }

    impl ExactSizeIterator for StdArgs {
        fn len(&self) -> usize {
            self.inner.len()
        }
    }

    pub struct StdArgsOs{
        inner: RustArgs,
    }

    impl Iterator for StdArgsOs {
        type Item = OsString;
        fn next(&mut self) -> Option<OsString> {
            self.inner.next()
        }
        fn size_hint(&self) -> (usize, Option<usize>) {
            self.inner.size_hint()
        }
    }

    impl ExactSizeIterator for StdArgsOs {
        fn len(&self) -> usize {
            self.inner.len()
        }
    }

    impl DoubleEndedIterator for StdArgsOs {
        fn next_back(&mut self) -> Option<OsString> {
            self.inner.next_back()
        }
    }
    
    #[no_mangle]
    pub fn std_args()->StdArgs{
        StdArgs { inner: std_args_os() }
    }

    #[no_mangle]
    pub fn std_args_os()->StdArgsOs{
        StdArgsOs { inner:rust_args() }
    }
}



mod rust_imp{
    use super::RustArgs;
    use std::sync::atomic::{AtomicIsize, AtomicPtr, Ordering};
    use std::ptr;
    use std::ffi::{CStr, OsString};
    use std::os::unix::prelude::*;
    use std::marker::PhantomData;
    static ARGC: AtomicIsize = AtomicIsize::new(0);
    static ARGV: AtomicPtr<*const u8> = AtomicPtr::new(ptr::null_mut());

    pub unsafe fn init(argc: isize, argv: *const *const u8) {
        ARGC.store(argc, Ordering::Relaxed);
        ARGV.store(argv as *mut _, Ordering::Relaxed);
    }

    pub unsafe fn cleanup() {
        ARGC.store(0, Ordering::Relaxed);
        ARGV.store(ptr::null_mut(), Ordering::Relaxed);
    }

    pub fn args() -> RustArgs {
        RustArgs { iter: clone().into_iter(), _dont_send_or_sync_me: PhantomData }
    }

    fn clone() -> Vec<OsString> {
        unsafe {
            let argc = ARGC.load(Ordering::Relaxed);
            let argv = ARGV.load(Ordering::Relaxed);
            (0..argc)
                .map(|i| {
                    let cstr = CStr::from_ptr(*argv.offset(i) as *const libc::c_char);
                    OsStringExt::from_vec(cstr.to_bytes().to_vec())
                })
                .collect()
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn it_works() {
        assert_eq!(2 + 2, 4);
    }

    #[test]
    fn test_mock(){
        
    }
}
