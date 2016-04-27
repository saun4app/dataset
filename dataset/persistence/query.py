from collections_extended import setlist
import sqlize  # sql query builder
from dataset.persistence.util import get_select_result
import pprint as pp

class DatasetSelect(object):
    def __init__(self, db, limit=None, offset=None, distinct=False):
        self.select_object = sqlize.Select(limit=limit, offset=offset)
        self.db = db
        self.distinct(distinct)
        self._init_param_list_dict()

    def _init_param_list_dict(self):
        item_list = ['table', 'column', 'where', 'where_and', 'where_or', 'group_by', 'order_by']

        self.param_list_dict = {}
        for item in item_list:
            self.param_list_dict[item] = setlist()

    def _append_param_item(self, key, param_item):
        try:
            if isinstance(param_item, list):
                for value in param_item:
                    self.param_list_dict[key].append(value)
            else:
                self.param_list_dict[key].append(param_item)
        except:
            pass

    def table(self, table_name):
        self._append_param_item('table', table_name)
        return (self)

    def column(self, column_name):
        self._append_param_item('column', column_name)
        return (self)

    def where(self, column_name):
        self._append_param_item('where', column_name)
        return (self)

    def where_and(self, column_name):
        self._append_param_item('where_and', column_name)
        return (self)

    def where_or(self, column_name):
        self._append_param_item('where_or', column_name)
        return (self)

    def group_by(self, column_name):
        self._append_param_item('group_by', column_name)
        return (self)

    def order_by(self, column_name):
        self._append_param_item('order_by', column_name)
        return (self)

    def limit(self, value):
        self.select_object.limit = value
        return (self)

    def offset(self, value):
        self.select_object.offset = value
        return (self)

    def distinct(self, value):
        self.distinct_value = value
        return (self)


    def get_query_string(self):

        def get_result_value(value_set_list, default_value=None):
            value_list = list(value_set_list)
            value_list.sort()
            result_value = (default_value, value_list)[len(value_list) > 0]
            return (result_value)

        def get_query_string():
            query_string = str(self.select_object)
            if True == self.distinct_value:
                query_string = query_string.replace('SELECT ', 'SELECT DISTINCT ')
            pp.pprint(query_string)
            return(query_string)

        self.select_object.sets = get_result_value(self.param_list_dict['table'])
        self.select_object.what = get_result_value(self.param_list_dict['column'], ['*'])
        self.select_object.where = get_result_value(self.param_list_dict['where'])
        self.select_object.where.and_ = get_result_value(self.param_list_dict['where_and'])
        self.select_object.where.or_ = get_result_value(self.param_list_dict['where_or'])
        self.select_object.group = get_result_value(self.param_list_dict['group_by'])
        self.select_object.order = get_result_value(self.param_list_dict['order_by'])

        q_string = get_query_string()
        return (q_string)

    def select(self, result_type='dict_list'):
        query_string = self.get_query_string()
        query_result = self.db.query(query_string)

        return get_select_result(query_result, result_type)
