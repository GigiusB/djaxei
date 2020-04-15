import importlib
from collections import OrderedDict
from contextlib import contextmanager
from tempfile import NamedTemporaryFile


class AbstractWorkbook:
    def __init__(self, tmpdir=None, dest=None):
        self.workbookfile = dest or NamedTemporaryFile(dir=tmpdir, suffix=".xlsx", delete=False)

    def write_data(self, data):
        raise Exception('Unimplemented')

    def close(self):
        pass


class OpenpyxlWorkbookImpl(AbstractWorkbook):
    def __init__(self, tmpdir=None, dest=None):
        self.Workbook = importlib.import_module('openpyxl.Workbook')
        AbstractWorkbook.__init__(self, tmpdir, dest)

    def write_data(self, data):
        workbook = self.Workbook()
        for k, v in data.items():
            worksheet = workbook.create_sheet(title=k)
            worksheet.extend(v)
        del workbook['Sheet']
        workbook.close()
        return self.workbookfile.name


class XlwtWorkbookImpl(AbstractWorkbook):
    def __init__(self, tmpdir=None, dest=None):
        self.Workbook = importlib.import_module('xlwt.Workbook')
        AbstractWorkbook.__init__(self, tmpdir, dest)

    def write_data(self, data):
        workbook = self.Workbook.Workbook()
        for k, rows in data.items():
            worksheet = workbook.add_sheet(sheetname=k)
            for line, row in enumerate(rows):
                for col, value in enumerate(row):
                    worksheet.write(line, col, value)
        workbook.save(self.workbookfile)
        return self.workbookfile.name


class XlswriterWorkbookImpl(AbstractWorkbook):
    def __init__(self, tmpdir=None, dest=None):
        self.Workbook = importlib.import_module('xlsxwriter.Workbook')
        AbstractWorkbook.__init__(self, tmpdir, dest)


IMPLEMENTATIONS = OrderedDict(
    (
        ('xlwt', XlwtWorkbookImpl),
        ('openpyxl', OpenpyxlWorkbookImpl),
        ('xlsxwriter', XlswriterWorkbookImpl),
    )
)


def get_implemetation_class(woorkbook_impl):
    return [x for x in IMPLEMENTATIONS if IMPLEMENTATIONS[x] == woorkbook_impl][0]


@contextmanager
def get_writer(implementation=None, tmpdir=None, dest=None, *args, **kwargs):
    writer = None
    try:
        if implementation:
            writer = IMPLEMENTATIONS[implementation](tmpdir, dest)
        else:
            for k, v in IMPLEMENTATIONS.items():
                try:
                    writer = v(tmpdir, dest)
                    break
                except Exception as e:
                    pass
        yield writer
    finally:
        if writer:
            writer.close()