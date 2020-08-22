.PHONY:all hello api-collections-hashmap test_intrinsics
all:hello api-collections-hashmap test_intrinsics
hello:hello.rs
	rustc -C panic="abort" hello.rs
	objdump -d hello > hello.txt
api-collections-hashmap:api-collections-hashmap.rs
	rustc -C panic="abort" api-collections-hashmap.rs
	objdump -d api-collections-hashmap > api-collections-hashmap.txt
test_intrinsics:test_intrinsics.rs
	rustc -C panic="abort" test_intrinsics.rs
	objdump -d test_intrinsics > test_intrinsics.txt

