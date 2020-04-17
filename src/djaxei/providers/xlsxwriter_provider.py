from xlsxwriter import Workbook


class WorkbookImpl(Workbook):
    _preferred_suffix = ".xlsx"

    def __init__(self, filename=None, options=None):
        super(WorkbookImpl, self).__init__(filename, options)

    def write_data(self, data):
        for ws_name, rows in data.items():
            ws = self.add_worksheet(ws_name)
            for i, row in enumerate(rows):
                ws.write_row(i, 0, row)
        self.close()
