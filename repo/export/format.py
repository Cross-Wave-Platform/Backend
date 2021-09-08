# from _typeshed import NoneType
import abc
import pandas
import pyreadstat
import os


class FormatTypeError(ValueError):
    pass


class FormatInterface(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def write(df, meta, dest):
        pass


class Sav(FormatInterface):
    @staticmethod
    def write(df, meta, dest):
        file_path = os.path.join(dest, 'output.sav')
        pyreadstat.write_sav(df,
                             file_path,
                             variable_value_labels=meta['var_labels'],
                             column_labels=meta['prob_topic'],
                             variable_format=meta['org_types'])


class Csv(FormatInterface):
    @staticmethod
    def write(df, meta, dest):
        csv_file_path = os.path.join( dest, 'output.csv')
        xlsx_file_path = os.path.join( dest, 'output.xlsx')

        # time convertion needed for formats in SDATE10
        bais = 141428 * 86400
        org_types = meta.get('org_types')
        for key, format in org_types.items():
            if 'DATE' in format:
                df[key] = pandas.to_timedelta( (df[key]-bais), unit='s') + pandas.Timestamp('1970-1-1')

        # print(df,meta)

        df.to_csv(csv_file_path,index=False)

        final_meta = pandas.DataFrame(columns=['變項名稱','變項標籤','數值標籤'])

        var_labels = meta.get('var_labels')
        prob_topic = meta.get('prob_topic')
        for key, item in prob_topic.items():
            sum_dict = ''
            if type(var_labels.get(key,'')) != str:
                tmp_dict = var_labels.get(key)
                sum_dict = '\n'.join('{}:{}'.format(*p) for p in tmp_dict.items())
            temp = pandas.DataFrame([[key,item,sum_dict]], columns=['變項名稱','變項標籤','數值標籤'])
            final_meta = final_meta.append(temp)

        print(final_meta)

        with pandas.ExcelWriter(xlsx_file_path) as writer:
            final_meta.to_excel(writer,sheet_name='variable_labels',index=False)

        pass


class FormatFactory():
    def __new__(cls, format_type):
        if format_type == 'sav':
            return Sav()
        elif format_type == 'csv':
            return Csv()
        else:
            raise FormatTypeError