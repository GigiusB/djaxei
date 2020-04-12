from collections import OrderedDict

from openpyxl import load_workbook


class Importer:
    def __init__(self, tmpdir=None, **kwargs):
        self.tmpdir = tmpdir

    def xls_import(self, file, models_dict, *args, **kwargs):
        wb = load_workbook(file, data_only=True)

        for ws_name, callback in models_dict.items():
            ws = wb[ws_name]
            for rownum, row in enumerate(ws.iter_rows(values_only=True)):
                if rownum == 0:
                    header = row
                else:
                    callback(OrderedDict(zip(header, row)))
        wb.close()

