import importlib


def get_workbook_impl():
    errors = []
    try:
        provider = importlib.import_module('djaxei.providers.xlsxwriter_provider')
        return provider.WorkbookImpl
    except Exception as e1:
        errors.append(e1)

    try:
        provider = importlib.import_module('djaxei.providers.xlwt_provider')
        return provider.WorkbookImpl
    except Exception as e2:
        errors.append(e2)

    errors = "\n".join(map(str, errors))
    raise RuntimeError(f'No provider found\n{errors}')
