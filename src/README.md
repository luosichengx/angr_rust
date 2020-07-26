## **代码文件**
由于每个二进制中的函数签名不同，需要单独进行hook, 对于每一个rust-examples中的二进制文件，都有一个对应的`analyse_*.py`  
#### 下表中是测试的完成情况：  
|文件名|二进制文件|进行状况|时间(s)|说明|
|:-:|:-:|:-:|:-:|:-:|
|`analyse_utils.py`|hello|**已完成**|18|环境变量的初始化与读取|
|`analyse_minimal_hook.py`|*|进行中|-|测试最小hook内容|
|`analyse_api_collections_hashmap.py`|*|进行中|-|hashmap|
|`analyse_what_it_looks_like.py`|*|***无结果***|9|线程、闭包|
|`analyse_what_it_looks_like2.py`|*|**已完成**|6|match语法|
|`analyse_what_it_looks_like3.py`|*|**已完成**|-|unicode字符|





