from collections_extended import setlist
import sqlize  # sql query builder
import dataset
from dataset.persistence.util import get_select_result


class SelectBuilder(object):
    def __init__(self, limit=None, offset=None):
        self.limit = limit
        self.offset = offset
        self._init_param_list_dict()

    def _init_param_list_dict(self):
        item_list = ['table', 'column', 'where', 'where_and', 'where_or', 'group_by', 'order_by']

        self.param_list_dict = {}
        for item in item_list:
            self.param_list_dict[item] = setlist()

    def _append_param_item(self, key, value_list):
        try:
            self.param_list_dict[key].append(value_list)
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

    def get_query_string(self):

        def get_result_value(value_set_list, default_value=None):
            value_list = list(value_set_list)
            value_list.sort()
            result_value = (default_value, value_list)[len(value_list) > 0]

            return (result_value)

        select_object = sqlize.Select(limit=self.limit, offset=self.offset)
        select_object.sets = get_result_value(self.param_list_dict['table'])
        select_object.what = get_result_value(self.param_list_dict['column'], ['*'])
        select_object.where = get_result_value(self.param_list_dict['where'])
        select_object.where.and_ = get_result_value(self.param_list_dict['where_and'])
        select_object.where.or_ = get_result_value(self.param_list_dict['where_or'])
        select_object.group = get_result_value(self.param_list_dict['group_by'])
        select_object.order = get_result_value(self.param_list_dict['order_by'])

        return (str(select_object))


class DatasetSelect(SelectBuilder):
    def __init__(self, db_string='sqlite:///:memory', limit=None, offset=None):
        super(self.__class__, self).__init__(limit, offset)
        self.db = dataset.connect(db_string)

    def select(self, result_type='dict_list'):
        query_string = self.get_query_string()
        query_result = self.db.query(query_string)

        return get_select_result(query_result, result_type)
