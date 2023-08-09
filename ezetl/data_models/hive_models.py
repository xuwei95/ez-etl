from ezetl.data_models import DataModel
from ezetl.utils.common_utils import gen_json_response
from ezetl.libs.hive import HiveClient


class HiveSqlModel(DataModel):

    def __init__(self, model_info):
        super().__init__(model_info)
        self.db_type = self._source.get('type')
        conn_conf = self._source['conn_conf']
        model_conf = self._model.get('model_conf', {})
        self.sql = model_conf.get('sql', 'show tables')
        self.default_sql = self.sql
        self.auth_types = model_conf.get('auth_type', '').split(',')
        self._client = HiveClient(**conn_conf)

    def connect(self):
        '''
        连通性测试
        '''
        try:
            flag, res = self.read_page(pagesize=1)
            if flag:
                return True, '连接成功'
            else:
                return False, '连接失败'
        except Exception as e:
            return False, f'{e}'

    def get_res_fields(self):
        '''
        获取字段列表
        '''
        flag, res = self.read_page(pagesize=1)
        if flag and res.get('code') == 200:
            records = res['data']['records']
            if records != []:
                record = records[0]
                fields = []
                for k in record:
                    field_dic = {
                        'field_name': k,
                        'field_value': k,
                        'ext_params': {}
                    }
                    fields.append(field_dic)
                return fields
        return []

    def get_search_type_list(self):
        '''
        获取可用高级查询类型
        '''
        return [{
            'name': 'sql',
            'value': 'sql',
            "default": self.sql
        }]

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
        sql_rules = [i for i in self.extract_rules if i['field'] == 'search_text' and i['rule'] == 'sql' and i['value']]
        if sql_rules != []:
            self.sql = sql_rules[0].get('value')

    def read_page(self, page=1, pagesize=20):
        '''
        分页读取数据
        :param page:
        :param pagesize:
        :return:
        '''
        self.gen_extract_rules()
        if 'custom_sql' not in self.auth_types and self.sql != self.default_sql:
            return False, '无修改sql权限'
        cursor = self.session.execute(self.sql)
        results = cursor.fetchall()
        total = len(results)
        results = results[(page - 1) * pagesize:page * pagesize]
        data_li = [dict(zip(result.keys(), result)) for result in results]
        res_data = {
            'records': data_li,
            'total': total
        }
        return True, gen_json_response(data=res_data)

    def read_batch(self):
        '''
        生成器分批读取数据
        :return:
        '''
        self.gen_extract_rules()
        if 'custom_sql' not in self.auth_types and self.sql != self.default_sql:
            return False, '无修改sql权限'
        cursor = self._client.execute(self.sql)
        results = cursor.fetchall()
        total = len(results)
        data_li = [dict(zip(result.keys(), result)) for result in results]
        pagesize = self._extract_info.get('batch_size', 1000)
        total_pages = total // pagesize + 1
        n = 0
        while n < total_pages:
            page = n + 1
            n += 1
            li = data_li[(page - 1) * pagesize:page * pagesize]
            res_data = {
                'records': li,
                'total': total
            }
            yield True, gen_json_response(data=res_data)