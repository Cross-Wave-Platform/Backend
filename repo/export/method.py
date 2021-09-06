import abc
import pandas


class MethodTypeError(ValueError):
    pass


class MethodInterface(abc.ABC):
    def __init__(self, method):
        self.method = method

    @abc.abstractmethod
    def concat_df(self, res, tmp, str_info):
        pass

    @abc.abstractmethod
    def concat_meta(self, res, tmp, str_info):
        pass


class Union(MethodInterface):
    def concat_df(self, res, tmp, str_info):
        tmp['wave'] = str_info
        res = pandas.concat([res, tmp], ignore_index=True)
        return res

    def concat_meta(self, res, tmp, str_info):
        tmp_org_type = tmp.original_variable_types
        tmp_var_labels = tmp.variable_value_labels

        res['org_types'].update(tmp_org_type)
        for col, labels in tmp_var_labels.items():
            if res['var_labels'].get(col):
                res['var_labels'][col].update(labels)
            else:
                res['var_labels'][col] = labels
        return res


class Join(MethodInterface):
    @staticmethod
    def repl_except(col_name, str_info):
        if col_name == 'baby_id':
            return col_name
        else:
            return f'{col_name}_{str_info}'

    def concat_df(self, res, tmp, str_info):
        tmp.columns = [self.repl_except(c, str_info) for c in tmp.columns]
        if res.empty:
            res = tmp
        else:
            res = res.merge(tmp,
                            on='baby_id',
                            how=self.method,
                            suffixes=(False, f'_{str_info}'))
        return res

    def concat_meta(self, res, tmp, str_info):
        tmp_org_type = tmp.original_variable_types
        tmp_var_labels = tmp.variable_value_labels

        for col, col_type in tmp_org_type.items():
            res['org_types'].update({f'{col}_{str_info}': col_type})

        for col, labels in tmp_var_labels.items():
            res['var_labels'][f'{col}_{str_info}'] = labels
        return res


class MethodFactory():
    def __new__(cls, method):
        method_list = ['cross', 'inner', 'outer']
        if method == 'union':
            return Union(method)
        elif method in method_list:
            return Join(method)
        else:
            raise MethodTypeError
