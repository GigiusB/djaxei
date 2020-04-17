from xlwt import Workbook


class WorkbookImpl(Workbook):
    _preferred_suffix = ".xls"

    def __init__(self, filename, **kwargs):
        encoding, style_compression = kwargs.get('encoding', None), kwargs.get('style_compression', None)
        super(WorkbookImpl, self).__init__(encoding, style_compression)
        self._filename = filename

    def write_data(self, data):
        for ws_name, rows in data.items():
            ws = self.add_sheet(ws_name)
            for i, row in enumerate(rows):
                for j, value in enumerate(row):
                    if value is not None:
                        ws.write(i, j, unicode(value))
        self.save(self._filename)
