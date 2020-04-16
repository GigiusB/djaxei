from xlwt import Workbook

_results = {}


class WorkbookImpl(Workbook):

    def write_data(self, workbookfile, data):
        for ws_name, rows in data.items():
            ws = self.add_sheet(ws_name)
            _results[ws_name] = []
            for i, row in enumerate(rows):
                _results[ws_name].append([])
                for j, value in enumerate(row):
                    _results[ws_name][i].append(value)
                    ws.write(i + 1, j, unicode(value))

        # del workbook['Sheet']
        self.save(workbookfile)


def get_workbook_impl():
    return WorkbookImpl