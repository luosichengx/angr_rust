.PHONY: all
all: hello.rs
	rustc -C panic="abort" hello.rs
	rustc --emit llvm-ir -o hello.ll hello.rs
clean:
	rm hello hello.ll
