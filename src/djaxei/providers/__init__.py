import importlib


def get_workbook_impl():
    try:
        provider = importlib.import_module('djaxei.providers.xlsxwriter_provider')
        return provider.WorkbookImpl
    except:
        pass

    try:
        provider = importlib.import_module('djaxei.providers.xlwt_provider')
        return provider.WorkbookImpl
    except:
        pass