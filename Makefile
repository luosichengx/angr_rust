RUST_EXAMPLE_PATH=rust_example

.PHONY: all hello minimal_hook clean 
all: hello minimal_hook
hello: ${RUST_EXAMPLE_PATH}/hello.rs
	cd ${RUST_EXAMPLE_PATH} && rustc -C panic="abort" hello.rs && rustc --emit llvm-ir -o hello.ll hello.rs && cd -
	cd rust_shared_lib/my_lang_start && cargo build --release && cp target/release/libmy_rust_std.so ../../src && cargo clean
minimal_hook: ${RUST_EXAMPLE_PATH}/minimal_hook.rs
	cd ${RUST_EXAMPLE_PATH} && rustc -C panic="abort" minimal_hook.rs
clean:
	rm ${RUST_EXAMPLE_PATH}/{hello,hello.ll,minimal_hook}
