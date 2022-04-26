#TODO work out spreadsheet incorporation
def main():

    gc_input_time = 3
    gc_input_day = 12
    gc_input_outfit = "Cowboy Outfit"

    ss_time = load_spreadsheet(file_name="../assets/spreadsheets/outfits_sheet.xlsx", sheet_name='outfits_sheet')

    ss_keys = list(ss_time[0].keys())

    indexes = [k for k in ss_keys if ss_keys.index(k) < 3]
    flag_keys = [k for k in ss_keys if k[0:4] == 'flag']


    for row in ss_time:
        flag1 = False
        flag2 = False
        flag3 = False
        all_flags_true = False
        # time
        if row[indexes[0]] == gc_input_time:
            flag1 = True

        # date
        if row[indexes[1]] == gc_input_day:
            flag2 = True

        # outfit
        if row[indexes[2]] == gc_input_outfit:
            flag3 = True

        if flag1 and flag2 and flag3 == True:
            all_flags_true = True

        if all_flags_true:
            print(row['dialogue'])

def load_spreadsheet(file_name, sheet_name):
    from openpyxl import load_workbook

    workbook = load_workbook(filename=file_name)

    sheet = workbook[sheet_name]
    # for sheet in workbook.worksheets:

    row_count = sheet.max_row
    column_count = sheet.max_column

    header = []
    for col in range(1, 5):
        header.append(sheet.cell(1, col).value)

    row_values = []

    for row in range(2, 4):
        this_row = {}
        for ind, header_name in enumerate(header):
            this_row[header_name] = sheet.cell(row, ind+1).value
        row_values.append(this_row)


    for row in row_values:
        pass
        # print(row)
    return row_values


    # for row in sheet.iter_rows():
    #     for cell in row:
    #         print(cell.value)








    # sheet = workbook.active

    # sheet["A1"] = "hello"
    # sheet["B1"] = "world!"
    #
    #
    #
    # workbook.save(filename="hello_world.xlsx")

if __name__ == "__main__":
    main()

