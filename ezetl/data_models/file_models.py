import os.path
from ezetl.data_models import DataModel
from ezetl.utils.common_utils import trans_rule_value, read_file, md5, gen_json_response
import pandas as pd
import io


class BaseFileModel(DataModel):

    def __init__(self, model_info):
        super().__init__(model_info)
        conn_conf = self._source.get('conn_conf', {})
        self.file_path = conn_conf.get('path')

    def connect(self):
        '''
        连通性测试
        '''
        try:
            file_obj = read_file(self.file_path)
            if file_obj:
                return True, '连接成功'
            else:
                return False, '连接失败'
        except Exception as e:
            return False, str(e)


class TableFileModel(BaseFileModel):

    def __init__(self, model_info):
        super().__init__(model_info)

    def connect(self):
        '''
        连通性测试
        '''
        flag, res = self.read_page(pagesize=1)
        if flag:
            return True, '连接成功'
        else:
            return False, '连接失败'

    def get_res_fields(self):
        '''
        获取字段列表
        '''
        flag, res_data = self.gen_extract_rules()
        if not flag:
            assert ValueError(res_data)
        res_fields = []
        try:
            for column in self.df.columns:
                dic = {
                    'field_name': column,
                    'field_value': column,
                }
                res_fields.append(dic)
        except Exception as e:
            print(e)
        return res_fields

    def read_file_path(self, file_path, use_cache=False, cache_size=1000):
        '''
        预览模式读取较大网络文件时缓存文件前n条直接读取
        '''
        if use_cache:
            if not os.path.exists('tmp'):
                os.mkdir('tmp')
            cache_file_path = os.path.join('tmp', f"{md5(file_path)}_{cache_size}")
            if os.path.exists(cache_file_path):
                content_value = open(cache_file_path, 'rb').read()
                file_obj = io.BytesIO(content_value)
                return file_obj
            else:
                file_obj = read_file(file_path)
                df = self.get_df(file_obj, nrows=cache_size)
                f = io.BytesIO()
                if self.file_path.endswith('.csv'):
                    df.to_csv(f, index=False)
                else:
                    df.to_excel(f, index=False)
                content_value = f.getvalue()
                cache_file = open(cache_file_path, 'wb')
                cache_file.write(content_value)
                cache_file.close()
                return f
        else:
            file_obj = read_file(file_path)
            return file_obj

    def get_df(self, file_obj, nrows=None, skiprows=None):
        '''
        获取pandas df
        '''
        df = None
        try:
            if self.file_path.endswith('.csv'):
                df = pd.read_csv(file_obj, dtype=object, nrows=nrows, skiprows=skiprows)
            else:
                df = pd.read_excel(file_obj, dtype=object, nrows=nrows, skiprows=skiprows)
            df.fillna("", inplace=True)
        except Exception as e:
            print(e)
        return df

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
        rules = [{
            'name': '等于',
            'value': 'equal'
          }, {
            'name': '不等于',
            'value': 'f_equal'
          }, {
            'name': '大于',
            'value': 'gt'
          }, {
            'name': '大于等于',
            'value': 'gte'
          }, {
            'name': '小于',
            'value': 'lt'
          }, {
            'name': '小于等于',
            'value': 'lte'
          }, {
            'name': '缓存前n条数据读取',
            'value': 'use_cache'
          }
        ]
        return rules

    def gen_extract_rules(self):
        '''
        解析筛选规则
        :return:
        '''
        cache_rules = [i for i in self.extract_rules if i.get('rule') == 'use_cache']
        cache_size = 0
        if cache_rules != []:
            try:
                cache_size = int(cache_rules[0].get('value'))
            except Exception as e:
                print(e)
        if cache_size > 0:
            self.file_obj = self.read_file_path(self.file_path, use_cache=True, cache_size=cache_size)
        else:
            self.file_obj = self.read_file_path(self.file_path, use_cache=False)
        self.df = self.get_df(self.file_obj)
        if self.df is None:
            return False, '文件读取错误'
        for i in self.extract_rules:
            print(i)
            field = i.get('field')
            rule = i.get('rule')
            value = i.get('value')
            value = trans_rule_value(value)
            if field and value:
                if rule in ['equal', 'eq']:
                    self.df = self.df[self.df[field] == value]
                elif rule in ['f_equal', 'neq']:
                    self.df = self.df[self.df[field] != value]
                elif rule == 'gt':
                    self.df = self.df[self.df[field] > value]
                elif rule == 'gte':
                    self.df = self.df[self.df[field] >= value]
                elif rule == 'lt':
                    self.df = self.df[self.df[field] < value]
                elif rule == 'lte':
                    self.df = self.df[self.df[field] <= value]
        data_li = []
        for k, row in self.df.iterrows():
            data_li.append(row.to_dict())
        return True, data_li

    def read_page(self, page=1, pagesize=20):
        '''
        分页读取数据
        :param page:
        :param pagesize:
        :return:
        '''
        flag, res_data = self.gen_extract_rules()
        if not flag:
            return False, res_data
        total = len(res_data)
        data_li = res_data[(page-1)*pagesize:page*pagesize]
        res_data = {
            'records': data_li,
            'total': total
        }
        return True, gen_json_response(data=res_data)

    def read_batch(self):
        '''
        生成器分批读取数据
        :param res_type: 返回形式
        :return:
        '''
        flag, res_data = self.gen_extract_rules()
        if not flag:
            return False, res_data
        total = len(res_data)
        pagesize = self._extract_info.get('batch_size', 1000)
        total_pages = total // pagesize + 1
        n = 0
        while n < total_pages:
            page = n + 1
            n += 1
            result = {
                'records': res_data[(page-1)*pagesize:page*pagesize],
                'total': total
            }
            yield True, gen_json_response(result)



