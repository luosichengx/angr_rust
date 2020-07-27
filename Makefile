RUST_EXAMPLE_PATH=old_rust_example
RUST_BINARY_PATH=rust-examples/build
SRC_PATH=src

.PHONY: all hello minimal_hook clean shared_lib txt clean_all
all: shared_lib txt
txt: 
	./generate_txt
shared_lib:
	cd rust_shared_lib/my_lang_start && cargo build --release && cp target/release/libmy_rust_std.so ../../src && cargo clean
hello: ${RUST_EXAMPLE_PATH}/hello.rs
	cd ${RUST_EXAMPLE_PATH} && rustc -C panic="abort" hello.rs && rustc --emit llvm-ir -o hello.ll hello.rs && cd -
minimal_hook: ${RUST_EXAMPLE_PATH}/minimal_hook.rs
	cd ${RUST_EXAMPLE_PATH} && rustc -C panic="abort" minimal_hook.rs && cd -
clean:
	rm ${RUST_BINARY_PATH}/*.txt
	rm ${SRC_PATH}/*.so
clean_all:
	rm ${RUST_BINARY_PATH}/*.txt
	rm ${RUST_EXAMPLE_PATH}/*.ll
	rm ${RUST_EXAMPLE_PATH}/*.txt
