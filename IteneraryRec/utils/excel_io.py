from pyexcel_xls import get_data, save_data

def read_xls_file(path):
    xls_data = get_data(path)
    return xls_data['Sheet 1']

