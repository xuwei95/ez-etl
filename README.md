## 简介
ez-etl是一个用Python编写的开源数据集成模块。用于将各类型数据源抽象为数据模型，只需配置一个任务字典，即可完成从各种数据模型读取数据。使用代码或内置的转换算法将数据转换为目标数据格式，并将其写入目标数据模型的流程。

## 安装与使用
可以使用pip来进行安装：
```
pip install ez-etl
```
### etl任务配置示例
> 以下示例使用任务配置字典分批读取mysql，内置函数转换数据，写入目标kafka数据源，更多数据源配置方式可参考examples下代码。
```
from ezetl.etl_task import etl_task_process

task_params = {
    'extract': {
        'source': {
            "type": "mysql",  # 数据源类型 mysql
            "conn_conf": {  # mysql链接信息
                "host": "127.0.0.1",
                "port": 3306,
                "username": "root",
                "password": "123456",
                "database_name": "test"
            }
        },
        'model': {
            "type": "mysql_table",  # 数据模型类型 mysql表
            "model_conf": {  # 数据模型信息，表名btc_history
                "name": "btc_history",
            }
        },
        'extract_info': {
            'extract_type': "batch",  # 读取方式，分批读取  
            'batch_size': 100,  # 每批读取数量
            'extract_rules': {  # 读取过滤条件 close >= 30000 and high < 40000
              "gte[close]": 30000, 
              "lt[high]": 40000
            }
        }
    },
    'process_rules': [  # 转换流程列表及参数
        {
            "code": "gen_records_list",
            "name": "获取内容列表",
            "rule_dict": {
                "fields": "time,symbol,close,high"
            }
        }
    ],
    'load': {
        'source': {
            "type": "kafka",  # 数据源类型 kafka
            "conn_conf": {  # kafka 连接信息
                "bootstrap_servers": "127.0.0.1:9092",
            }
        },
        'model': {
            "type": "kafka_topic",  # 数据模型类型 kafka topic
            "model_conf": {  # 模型信息，topic名btc_history
                "name": "btc_history",
            }
        },
        'load_info': {
            'load_type': 'insert'  # 写入方式，直接写入  
        }
    }
}
etl_task_process(task_params, run_load=True)
```

### 拆分使用
 > 对于复杂的etl任务，内置算法可能不满足需求，此时可将读取器和写入器分别在代码中使用，以满足各种需求
 > 示例如下 
 
1，创建一个读取数据源配置字典。配置字典定义了数据源的相关参数，例如连接信息、查询语句、过滤规则等。
```
from ezetl.utils import get_reader

reader_info = {
    'source': {
        "name": "test",
        "type": "mysql",  # 数据源类型 mysql
        "conn_conf": {  # mysql链接信息
            "host": "127.0.0.1",
            "port": 3306,
            "username": "root",
            "password": "123456",
            "database_name": "test"
        },
        "ext_params": {}
    },
    'model': {
        "name": "btc_history",
        "type": "mysql_table",  # 数据模型类型 mysql表
        "model_conf": {  # 数据模型信息，表名btc_history
            "name": "btc_history",
        },
        "ext_params": {},
        "fields": []
    },
    'extract_info': {
        'batch_size': 100,  # 每批读取数量
        # 查询过滤条件 close >= 20000 and high < 40000
        # 可简化为字典形式 'extract_rules': {"gte[close]": 30000, "lt[high]": 40000}
        'extract_rules': [
            {'field': "close", "rule": "gte", "value": 20000},
            {'field': "high", "rule": "lt", "value": 40000}
        ]
    }
}
flag, reader = get_reader(reader_info)
print(flag, reader)
```
2，创建一个写入目标数据源配置字典。配置字典定义了数据源的相关参数，例如连接信息、写入规则等。
```
from ezetl.utils import get_writer
load_info = {
    'source': {
        "name": "test",
        "type": "kafka",  # 数据源类型 kafka
        "conn_conf": {  # kafka 连接信息
            "bootstrap_servers": "127.0.0.1:9092",
        },
        "ext_params": {}
    },
    'model': {
        "name": "test",
        "type": "kafka_topic",  # 数据模型类型 kafka topic
        "model_conf": {  # 模型信息，topic名btc_history
            "name": "btc_history",
        },
        "ext_params": {},
        "fields": []
    },
    'load_info': {
        'load_type': 'insert', # 写入方式 
        'only_fields': []
    }
}
_, writer = get_writer(load_info)
print(writer)
flag, res = writer.connect()
print(flag, res)
```
3，使用reader对象分批读取数据并写入目标数据源中。
```
for flag, read_data in reader.read_batch():
    print(read_data)
    if read_data['code'] == 200:
        # 转换数据逻辑
        write_data = read_data['data']['records']
        write_data = [i for i in write_data]
        # 写入目标数据源
        flg, res = writer.write(write_data)
        print(flg, res)
```
### 完整实例
```
'''
读取mysql，写入kafka
'''
from ezetl.utils import get_reader, get_writer

reader_info = {
    'source': {
        "name": "test",
        "type": "mysql",
        "conn_conf": {
            "host": "127.0.0.1",
            "port": 3306,
            "username": "root",
            "password": "123456",
            "database_name": "test"
        },
        "ext_params": {}
    },
    'model': {
        "name": "btc_history",
        "type": "mysql_table",
        "model_conf": {
            "name": "btc_history",
            "auth_type": "create,insert"
        },
        "ext_params": {},
        "fields": []
    },
    'extract_info': {
        'batch_size': 100,
        'extract_rules': []
    }
}
flag, reader = get_reader(reader_info)
print(flag, reader)
flag, res = reader.connect()
print(flag, res)
print(reader.get_res_fields())
load_info = {
    'source': {
        "name": "test",
        "type": "kafka",
        "conn_conf": {
            "bootstrap_servers": "127.0.0.1:9092",
        },
        "ext_params": {}
    },
    'model': {
        "name": "test",
        "type": "kafka_topic",
        "model_conf": {
            "name": "btc_history",
        },
        "ext_params": {},
        "fields": []
    },
    'load_info': {
        'load_type': 'insert',
        'only_fields': []
    }
}
_, writer = get_writer(load_info)
print(writer)
flag, res = writer.connect()
print(flag, res)
for flag, read_data in reader.read_batch():
    print(read_data)
    if read_data['code'] == 200:
        # 转换数据逻辑
        write_data = read_data['data']['records']
        write_data = [i for i in write_data]
        flg, res = writer.write(write_data)
        print(flg, res)
```
## 支持数据源
| 数据源类型 | 数据模型类型 | 读取 | 写入
|:-----:|:-----:|:-----:|:-----:|
| http | json api | 支持 | - |
| http | html | 支持 | - |
| 文件 | 表格文件(csv/excel) | 支持 | - |
| 文件 | json文件 | 支持 | - |
| 文件 | h5文件 | 支持 | - |
| minio对象存储 | 表格文件(csv/excel) | 支持 | 支持 |
| minio对象存储 | json文件 | 支持 | 支持 |
| minio对象存储 | h5文件 | 支持 | 支持 |
| redis | 字符串 | 支持 | 支持 |
| redis | 列表 | 支持 | 支持 |
| redis | 队列 | 支持 | 支持 |
| redis | 哈希 | 支持 | 支持 |
| mysql | mysql表 | 支持 | 支持 |
| mysql | sql | 支持 | - |
| mysql | binlog数据流 | 支持 | - |
| clickhouse | clickhouse表 | 支持 | 支持 |
| clickhouse | sql | 支持 | - |
| elasticsearch | elasticsearch索引 | 支持 | 支持 |
| mongodb | mongodb集合 | 支持 | 支持 |
| neo4j | neo4j graph | 支持 | 支持 |
| neo4j | sql | 支持 | - |
| influxdb | influxdb表 | 支持 | 支持 |
| influxdb | sql | 支持 | - |
| prometheus | promql | 支持 | - |
| kafka | kafka topic | 支持 | 支持 |
