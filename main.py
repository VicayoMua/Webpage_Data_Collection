from ChromePageRender import (
    # something else
    Options as ChromeOptions,
    ChromePageRender
)
from ExcelProcessing import (
    load_excel_workbook,
    ExcelWorkbook,
    ExcelWorksheet,
    ExcelCell,
    ExcelFont,
    ExcelAlignment,
    ExcelPatternFill
)
from time import sleep as thread_sleep

# '''
#     You must set up this <__chrome_driver_filepath> in order to run this script..!
# '''
__chrome_driver_filepath: str = "./chromedriver/chromedriver_132_win64_x64.exe"


workbook_filepath = "./collected_data.xlsx"
# workbook_filepath = ask_for_excel_filepath("Please enter the excel file path: ")
workbook: ExcelWorkbook = load_excel_workbook(workbook_filepath)

# automation_for_sheet_1(
#     workbook["Sheet1"],
#     access_carrier_side=False
# )
workbook.save(filename=workbook_filepath)
print("\nSuccessfully saved workbook to disk.\n", end="")
