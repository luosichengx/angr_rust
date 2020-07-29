## **代码文件**
+ 对于大部分rust-examples/build中的文件，修改`analyse.py`中的binary_file为对应的文件名即可
+ 有些文件hook的函数不同，需要单独进行hook, 对于每一个这样的二进制文件，都有一个对应的`analyse_*.py`  
#### 下表中是测试的完成情况：  
|文件名|二进制文件|进行状况|运行时间(s)|说明|
|:-:|:-:|:-:|:-:|:-:|
|`analyse_hello.py`|*|**<font color=Blue>已完成</font>**|18|环境变量的初始化与读取|
|`analyse_minimal_hook.py`|*|进行中|-|测试最小hook内容|
|`analyse.py`|api-collections-hashmap|***<font color=Green>跑不完</font>***|-|hashmap|
|`analyse_api_getopts.py`|*|**<font color=Blue>已完成</font>**|60|读取命令行参数|
|`analyse_api_rand.py`|*|***<font color=Red>无结果</font>***|4|rand;调用外部crate|
|`analyse_api_std_from_str.py`|*|**<font color=Blue>已完成</font>**|7|字符串转数字|
|`analyse.py`|api_std_vec|**<font color=Blue>已完成</font>**|18|数组|
|`analyse_gueseeing_game.py`|*|***<font color=Red>无结果</font>***|17|标准输入|
|`analyse.py`|book-3_2-dining_philosophers|**<font color=Blue>已完成</font>**|11|结构体|
|`analyse.py`|book-5_6-threads|***<font color=Red>无结果</font>***|-|线程|
|`analyse.py`|design_pattern-chain_of_command|**<font color=Blue>已完成</font>**|8|trait;Box访问堆|
|`analyse.py`|design_pattern-command|**<font color=Blue>已完成</font>**|5|Box;生命周期|
|`analyse.py`|design_pattern-decorator|**<font color=Blue>已完成</font>**|42|trait;输出格式|
|`analyse.py`|design_pattern-decorator2|**<font color=Blue>已完成</font>**|13|Box;输出格式|
|`analyse.py`|design_pattern-observer|**<font color=Blue>已完成</font>**|10|生命周期;trait|
|`analyse.py`|design_pattern-strategy|**<font color=Blue>已完成</font>**|5|trait|
|`analyse.py`|design_pattern-templatemethod|**<font color=Blue>已完成</font>**|14|trait;cmp|
|`analyse.py`|design_pattern-visitor|**<font color=Blue>已完成</font>**|10|trait;范型|
|`analyse.py`|find_max|**<font color=Blue>已完成</font>**|9|trait;范型;闭包;数组|
|`analyse.py`|lang-generics|**<font color=Blue>已完成</font>**|5|trait;结构体|
|`analyse.py`|lang-interface|**<font color=Blue>已完成</font>**|10|trait;结构体;范型|
|`analyse.py`|lang-lambda|**<font color=Blue>已完成</font>**|4|操作符重载|
|`analyse.py`|lang-overloading|**<font color=Blue>已完成</font>**|5|闭包|
|`analyse.py`|lang-pointers|**<font color=Blue>已完成</font>**|9|解引用操作符|
|`analyse.py`|linked_list|**<font color=Blue>已完成</font>**|6|链表|
|`analyse.py`|phantom_type|**<font color=Blue>已完成</font>**|6|PhantomData（幽灵数据）|
|`analyse.py`|tutorial-02_1-hello|**<font color=Blue>已完成</font>**|4|Print|
|`analyse.py`|tutorial-03-syntax_basics|**<font color=Blue>已完成</font>**|5|静态变量;let|
|`analyse.py`|tutorial-04_3-loops|**<font color=Blue>已完成</font>**|5|循环|
|`analyse.py`|tutorial-04_2-pattern-matching|***<font color=Red>无结果</font>***|-|rand；引用外部crate|
|`analyse.py`|tutorial-05_1-structs|**<font color=Blue>已完成</font>**|4|结构体|
|`analyse.py`|tutorial-05_2-enum|**<font color=Blue>已完成</font>**|5|枚举|
|`analyse.py`|tutorial-05_3-tuples|**<font color=Blue>已完成</font>**|4|元组结构|
|`analyse.py`|tutorial-15-closure|**<font color=Blue>已完成</font>**|5|闭包|
|`analyse.py`|tutorial-16-methods|***<font color=Red>无结果</font>***|4|PI;方法|
|`analyse.py`|tutorial-17-generics|**<font color=Blue>已完成</font>**|12|范型|
|`analyse.py`|tutorial-tasks-02_1-communication|***<font color=Red>无结果</font>***|10|线程;channel|
|`analyse.py`|tutorial-tasks-02_3-arc|***<font color=Red>无结果</font>***|8|线程;原子变量|
|`analyse.py`|what_it_looks_like|***<font color=Red>无结果</font>***|9|线程、闭包|
|`analyse.py`|what_it_looks_like2|**<font color=Blue>已完成</font>**|7|match语法|
|`analyse.py`|what_it_looks_like3|**<font color=Blue>已完成</font>**|8|unicode字符|
#### 下表中是跳过的文件  
|文件名|说明|跳过原因|
|:-:|:-:|:-:|
|`api-std-fs-file`|读取文件内容|编译出来的binary无法跑通|
|`fibonacci`|测试模块|objdump遇到无法识别的文件格式|
|`date`|测试模块|objdump遇到无法识别的文件格式|
|`lang-question_mark`|读取文件内容|编译出来的binary无法跑通|



