# -*- coding: gb2312 -*-


import xlwt


def write_excel(filename, D_content, order_sheet=False):
    workbook = xlwt.Workbook(encoding='gb2312')
    if not order_sheet:
        L_sheet_name = D_content.keys()
    else:
        L_sheet_name = order_sheet
    for sheet_name in L_sheet_name:
        try:
            booksheet = workbook.add_sheet(sheet_name, cell_overwrite_ok=True)
            for ii, row in enumerate(D_content[sheet_name]):
                for jj, col in enumerate(row):
                    booksheet.write(ii, jj, col)  
            if not D_content[sheet_name]:
                booksheet.write(0, 0, "None")  
        except KeyError:
            print "KeyError of write_excel : ", sheet_name
    workbook.save(filename + ".xls")
    return







