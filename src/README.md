## **代码文件**
由于每个二进制中的函数签名不同，需要单独进行hook, 对于每一个rust-examples中的二进制文件，都有一个对应的`analyse_*.py`  
#### 下表中是测试的完成情况：  
|文件名|二进制文件|进行状况|运行时间(s)|说明|
|:-:|:-:|:-:|:-:|:-:|
|`analyse_hello.py`|hello|**<font color=Blue>已完成</font>**|18|环境变量的初始化与读取|
|`analyse_minimal_hook.py`|*|进行中|-|测试最小hook内容|
|`analyse_api_collections_hashmap.py`|*|***<font color=Green>跑不完</font>***|-|hashmap|
|`analyse_api_getopts.py`|*|**<font color=Blue>已完成</font>**|60|读取命令行参数|
|`analyse_api_rand.py`|*|***<font color=Red>无结果</font>***|4|rand;调用外部crate|
|`analyse_api_std_from_str.py`|*|**<font color=Blue>已完成</font>**|7|字符串转数字|
|`analyse_api_std_vec.py`|*|***<font color=Blue>已完成</font>**|17|数组|
|`analyse_gueseeing_game.py`|*|***<font color=Red>无结果</font>***|17|标准输入|
|`analyse_dining_philosophers.py`|*|**<font color=Blue>已完成</font>**|11|结构体|
|`analyse_threads.py`|*|***<font color=Red>无结果</font>***|-|线程|
|`analyse_chain_of_commands.py`|*|**<font color=Blue>已完成</font>**|-|trait;Box访问堆|
|`analyse_what_it_looks_like.py`|*|***<font color=Green>跑不完</font>***|9|线程、闭包|
|`analyse_what_it_looks_like2.py`|*|**<font color=Blue>已完成</font>**|6|match语法|
|`analyse_what_it_looks_like3.py`|*|**<font color=Blue>已完成</font>**|7|unicode字符|
#### 下表中是跳过的文件  
|文件名|说明|跳过原因|
|:-:|:-:|:-:|
|`api-std-fs-file`|读取文件内容|编译出来的binary无法跑通|
|`fibonacci`|测试模块|objdump遇到无法识别的文件格式|
|`date`|测试模块|objdump遇到无法识别的文件格式|




