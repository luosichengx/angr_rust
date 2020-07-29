### 编译rust examples（默认已经编译好，无需操作，需要安装rustc nightly）
`cd rust-examples && make`
### 编译动态库并生成反汇编文件
`make`(或者`make shared_lib && make txt`)  
### 运行old_rust_example/hello的分析程序
`cd src && ./analyse_hello.py`(需要安装pypy3) 或者  
`cd src && python3 analyse_hello.py`