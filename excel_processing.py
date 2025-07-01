from excel_processing_lib import *

# given_workbook_filepath = "./DaiXiaQ1-2201.xlsx"
given_workbook_filepath = ask_for_excel_filepath("Please enter the excel file path: ")
given_workbook: Workbook = load_workbook(given_workbook_filepath)
given_sheet1: Worksheet = given_workbook["Sheet1"]

forbidden_substrings_in_tracking_number: list[str] = [
    "TRACK", "CANCEL", "DELIVER", "RECEIVE"
]


def value_filter(val: str) -> bool:
    if val is None:
        return False
    if not isinstance(val, str):
        return False
    if len(val) <= 5:
        return False
    if not val.isalnum():
        return False
    val = val.upper()
    for string in forbidden_substrings_in_tracking_number:
        if string in val:
            return False
    return True


column_1_dataset = set()
get_worksheet_data_by_axis(  # My Package
    data_container=column_1_dataset,
    clear_data_container=True,
    sheet=given_sheet1,
    axis='A',
    value_filter=value_filter,
    # value_post_transformer=value_post_transformer
)
column_2_dataset = set()
get_worksheet_data_by_axis(  # Warehouse Package
    data_container=column_2_dataset,
    clear_data_container=True,
    sheet=given_sheet1,
    axis='B',
    value_filter=value_filter,
    # value_post_transformer=value_post_transformer
)

incol1_but_notincol2 = column_1_dataset - column_2_dataset
incol2_but_notincol1 = column_2_dataset - column_1_dataset
inbothcols = column_1_dataset & column_2_dataset

new_workbook = Workbook()
default_sheet = new_workbook.active
default_sheet.title = "Sheet1"

column_count = max(len(column_1_dataset), len(column_2_dataset))
put_worksheet_data_by_axis(
    sheet=default_sheet,
    axis='A',
    dataset=range(1, column_count + 1),
    print_item_count=False,
    uniform_column_width=10,
    value_font=Font(name="Times New Roman", color="000000", bold=True, size=12)
)
put_worksheet_data_by_axis(
    sheet=default_sheet,
    axis='B',
    dataset=column_1_dataset,
    value_title="Trackings We Ordered"
)
put_worksheet_data_by_axis(
    sheet=default_sheet,
    axis='C',
    dataset=column_2_dataset,
    value_title="Trackings Received in Warehouse"
)
put_worksheet_data_by_axis(
    sheet=default_sheet,
    axis='D',
    dataset=inbothcols,
    value_title="Trackings Matched",
    value_font=Font(name="Times New Roman", color="006400", size=12)
)
put_worksheet_data_by_axis(
    sheet=default_sheet,
    axis='E',
    dataset=incol1_but_notincol2,
    value_title="Trackings not yet Received in Warehouse",
    value_font=Font(name="Times New Roman", color="8B0000", size=12)
)
put_worksheet_data_by_axis(
    sheet=default_sheet,
    axis='F',
    dataset=incol2_but_notincol1,
    value_title="Others' Trackings Received in Warehouse",
    value_font=Font(name="Times New Roman", color="8B0000", size=12)
)

new_workbook.save(filename=given_workbook_filepath + "__edited.xlsx")

print("\n\nSuccessfully Processed !!!\n\n")
input("Click ENTER to exit...")
