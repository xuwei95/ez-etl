import random
from ezetl.data_models import DataModel
from ezetl.utils.common_utils import gen_json_response
from pymysqlreplication import BinLogStreamReader
from pymysqlreplication.row_event import (
    DeleteRowsEvent,
    UpdateRowsEvent,
    WriteRowsEvent
)


class MysqlBinlogModel(DataModel):
    '''
    mysql binlog
    '''

    def __init__(self, model_info):
        super().__init__(model_info)
        conn_conf = self._source['conn_conf']
        self.conn_setting = {
            'host': conn_conf['host'],
            'port': conn_conf['port'],
            'user': conn_conf['username'],
            'passwd': conn_conf['password']
        }
        # 监听数据库
        database = conn_conf.get('database_name')
        self.listen_dbs = [database]
        model_conf = self._model['model_conf']
        # 监听数据表
        self.listen_tables = model_conf.get('listen_tables')
        self.only_events = []
        for event in model_conf.get('only_events'):
            if event == 'delete':
                self.only_events.append(DeleteRowsEvent)
            if event == 'write':
                self.only_events.append(WriteRowsEvent)
            if event == 'update':
                self.only_events.append(UpdateRowsEvent)
        self.stream = BinLogStreamReader(
            connection_settings=self.conn_setting,
            server_id=random.randint(10000, 99999),  # slave标识，唯一
            freeze_schema=True,
            resume_stream=True,  # 从最新事件开始监听
            blocking=True,  # 阻塞等待后续事件
            only_schemas=self.listen_dbs,  # 要监听的数据库
            only_tables=self.listen_tables,  # 要监听的表
            # 设定只监控写操作：增、删、改
            only_events=self.only_events
        )

    def connect(self):
        '''
        连通性测试
        '''
        try:
            stream = BinLogStreamReader(
                connection_settings=self.conn_setting,
                server_id=random.randint(10000, 99999),  # slave标识，唯一
                freeze_schema=True,
                resume_stream=True,  # 从最新事件开始监听
                blocking=False,  # 阻塞等待后续事件
                only_schemas=self.listen_dbs,  # 要监听的数据库
                only_tables=self.listen_tables,  # 要监听的表
                # 设定只监控写操作：增、删、改
                only_events=self.only_events
            )
            for binlogevent in stream:
                print(binlogevent)
            return True, '连接成功'
        except Exception as e:
            return False, str(e)

    def get_res_fields(self):
        '''
        获取字段列表
        '''
        return None

    def get_search_type_list(self):
        '''
        获取可用高级查询类型
        '''
        return []

    def get_extract_rules(self):
        '''
        获取可筛选项
        :return:
        '''
        rules = []
        return rules

    def gen_extract_rules(self):
        '''
        解析筛选规则
        :return:
        '''
        pass

    def read_page(self):
        '''
        分批读取数据
        :return:
        '''
        for binlogevent in self.stream:
            for row in binlogevent.rows:
                event = {"schema": binlogevent.schema, "table": binlogevent.table}
                if isinstance(binlogevent, DeleteRowsEvent):
                    event["action"] = "delete"
                    event["data"] = row["values"]
                elif isinstance(binlogevent, UpdateRowsEvent):
                    event["action"] = "update"
                    event["data"] = row["after_values"]
                elif isinstance(binlogevent, WriteRowsEvent):
                    event["action"] = "insert"
                    event["data"] = row["values"]
                res_data = {
                    'records': [event],
                    'total': 1
                }
                yield True, gen_json_response(data=res_data)

    def read_batch(self):
        '''
        生成器分批读取数据
        :return:
        '''
        for binlogevent in self.stream:
            for row in binlogevent.rows:
                event = {"schema": binlogevent.schema, "table": binlogevent.table}
                if isinstance(binlogevent, DeleteRowsEvent):
                    event["action"] = "delete"
                    event["data"] = row["values"]
                elif isinstance(binlogevent, UpdateRowsEvent):
                    event["action"] = "update"
                    event["data"] = row["after_values"]
                elif isinstance(binlogevent, WriteRowsEvent):
                    event["action"] = "insert"
                    event["data"] = row["values"]
                res_data = {
                    'records': [event],
                    'total': 1
                }
                yield True, gen_json_response(data=res_data)
