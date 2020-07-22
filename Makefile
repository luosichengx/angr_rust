.PHONY: all
all: hello.rs
	rustc -C panic="abort" hello.rs
	rustc --emit llvm-ir -o hello.ll hello.rs
	cd my_lang_start && cargo build --release && cp target/release/libmy_rust_std.so .. && cargo clean
clean:
	rm hello hello.ll
