.PHONY: all hello 
all: hello minimal_hook
hello: hello.rs
	rustc -C panic="abort" hello.rs
	rustc --emit llvm-ir -o hello.ll hello.rs
	cd ../my_lang_start && cargo build --release && cp target/release/libmy_rust_std.so .. && cargo clean
minimal_hook: minimal_hook.rs
	rustc -C panic="abort" minimal_hook.rs
clean:
	rm hello hello.ll minimal_hook
