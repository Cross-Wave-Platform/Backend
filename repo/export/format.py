import abc
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
                             variable_format=meta['org_types'])


class Csv(FormatInterface):
    @staticmethod
    def write(df, meta, dest):
        pass


class FormatFactory():
    def __new__(cls, format_type):
        if format_type == 'sav':
            return Sav()
        elif format_type == 'csv':
            return Csv()
        else:
            raise FormatTypeError