# from tracking_status_lib import *
# from excel_processing_lib import *
# from time import sleep as thread_sleep
#
# # '''
# #     You must set up this <__chrome_driver_filepath> in order to run this script..!
# # '''
# __chrome_driver_filepath: str = "./chromedrivers/chromedriver_132_macos_arm64"
#
#
# def automation_for_sheet_1(
#         sheet_1: Worksheet,
#         apple_order_urls_axis: str = "K",
#         tracking_carrier_axis: str = "W",  # search if doesn't exist
#         tracking_urls_axis: str = "X",  # search if doesn't exist
#         tracking_main_status_axis: str = "Y",  # search anyways
#         tracking_time_status_axis: str = "Z",  # search anyways
#         access_apple_side: bool = True,
#         access_carrier_side: bool = True
# ) -> None:  # returns tracking_numbers
#     options = Options()
#     options.add_argument("--incognito")
#     options.add_argument("--disable-blink-features=AutomationControlled")
#     options.add_argument(
#         "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
#     )
#     chrome_page_render = ChromePageRender(
#         chrome_driver_filepath=__chrome_driver_filepath,
#         options=options,
#         # use_undetected_chromedriver=True
#     )
#
#     tracking_carrier_column: tuple[Cell] = sheet_1[tracking_carrier_axis]
#     tracking_urls_column: tuple[Cell] = sheet_1[tracking_urls_axis]
#
#     if access_apple_side:
#         apple_order_urls_column: tuple[Cell] = sheet_1[apple_order_urls_axis]
#         finished_apple_records: bool = False
#         iteration_count: int = 1
#         while not finished_apple_records and iteration_count <= 20:
#             apple_order_urls_to_check: list = []
#             finished_apple_records = True
#             for i in range(len(apple_order_urls_column)):
#                 apple_order_url = apple_order_urls_column[i].value
#                 apple_carrier = tracking_carrier_column[i].value
#                 if (
#                         (isinstance(apple_carrier, str) and len(apple_carrier) != 0)  # URL is checked and static
#                         or not isinstance(apple_order_url, str)  # URL is not a string
#                         or apple_order_url.find("http") != 0  # URL is not a valid http alais
#                 ):
#                     apple_order_urls_to_check.append(None)
#                 else:
#                     apple_order_urls_to_check.append(apple_order_url)
#             (apple_results, timed_out_count) = get_apple_order_tracking_urls(
#                 apple_order_urls_to_check,
#                 chrome_page_render,
#                 # print_error_log_to_console=True
#             )
#             for i in range(len(apple_order_urls_column)):
#                 if tracking_carrier_column[i].value is None:
#                     tracking_carrier_column[i].value = apple_results[i][0]
#                     tracking_urls_column[i].value = apple_results[i][1]
#             if timed_out_count > 0:
#                 print(
#                     f"\nautomation_for_sheet_1: Notice: Apple servers might have killed our {timed_out_count} access(es) to order(s).\n",
#                     end=""
#                 )
#                 finished_apple_records = False
#                 for i in tqdm(range(20), desc="Waiting for Apple Server Re-Connections"):
#                     thread_sleep(1)
#             else:
#                 print(
#                     "\nautomation_for_sheet_1: Notice: Successfully got tracking status from Apple Order Server.\n",
#                     end=""
#                 )
#             iteration_count += 1
#
#         # chrome_page_render.close()
#
#     if access_carrier_side:
#         tracking_main_status_column: tuple[Cell] = sheet_1[tracking_main_status_axis]
#         tracking_time_status_column: tuple[Cell] = sheet_1[tracking_time_status_axis]
#         ups_tracking_urls: list[str] = []
#         fedex_tracking_urls: list[str] = []
#         for i in range(len(tracking_carrier_column)):
#             if tracking_carrier_column[i].value == "ups":
#                 ups_tracking_urls.append(tracking_urls_column[i].value)
#             if tracking_carrier_column[i].value == "fedex":
#                 fedex_tracking_urls.append(tracking_urls_column[i].value)
#         (ups_results, ups_timed_out_count) = get_ups_delivery_status(
#             ups_tracking_urls,
#             chrome_page_render,
#             # print_error_log_to_console=True
#         )
#         (fedex_results, fedex_timed_out_count) = get_fedex_delivery_status(
#             fedex_tracking_urls,
#             chrome_page_render,
#             # print_error_log_to_console=True
#         )
#         if ups_timed_out_count > 0:
#             print(
#                 f"\nautomation_for_sheet_1: Notice: Failed to get {ups_timed_out_count} items from UPS Tracking Server.\n",
#                 end=""
#             )
#         else:
#             print("\nautomation_for_sheet_1: Notice: Successfully got ups status from UPS Tracking Server.\n", end="")
#         if fedex_timed_out_count > 0:
#             print(
#                 f"\nautomation_for_sheet_1: Notice: Failed to get {fedex_timed_out_count} items from Fedex Tracking Server.\n",
#                 end=""
#             )
#         else:
#             print(
#                 "\nautomation_for_sheet_1: Notice: Successfully got fedex status from Fedex Tracking Server.\n",
#                 end=""
#             )
#         tracking_url_mapping_result: dict = {None: (None, None)}
#         for i in range(len(ups_tracking_urls)):
#             tracking_url_mapping_result[ups_tracking_urls[i]] = ups_results[i]
#         for i in range(len(fedex_tracking_urls)):
#             tracking_url_mapping_result[fedex_tracking_urls[i]] = fedex_results[i]
#         for i in range(len(tracking_urls_column)):
#             r: (str, str) = tracking_url_mapping_result[tracking_urls_column[i].value]
#             if r[0] is not None:
#                 tracking_main_status_column[i].value = r[0]
#                 tracking_time_status_column[i].value = r[1]
#
#         # chrome_page_render.close()
#
#     chrome_page_render.close()
#
#
# forbidden_substrings_in_tracking_number: list[str] = [
#     "TRACK", "CANCEL", "DELIVER", "RECEIVE"
# ]
#
#
# def automation_for_sheet_2(
#         sheet_1: Worksheet,
#         sheet_2: Worksheet,
#         tracking_urls_axis_sheet_1: str = "X",
#         tracking_numbers_axis_sheet_2: str = "A"
# ) -> None:
#     def value_filter(val: str) -> bool:
#         if val is None:
#             return False
#         if not isinstance(val, str):
#             return False
#         if len(val) <= 5:
#             return False
#         if not val.isalnum():
#             return False
#         val = val.upper()
#         for string in forbidden_substrings_in_tracking_number:
#             if string in val:
#                 return False
#         return True
#
#     def get_tracking_number_from_tracking_url(tracking_url: str) -> str | None:
#         if not isinstance(tracking_url, str):
#             return None
#         leading_index = tracking_url.rfind("=") + 1
#         return tracking_url[leading_index:]
#
#     warehouse_trackings = set()
#     get_worksheet_data_by_axis(  # My Package
#         data_container=warehouse_trackings,
#         clear_data_container=False,
#         sheet=sheet_2,
#         axis=tracking_numbers_axis_sheet_2,
#         value_filter=value_filter,
#         # value_post_transformer=value_post_transformer
#     )
#
#     my_trackings = set()
#     for cell in sheet_1[tracking_urls_axis_sheet_1]:
#         my_tracking_number = get_tracking_number_from_tracking_url(cell.value)
#         if my_tracking_number is None:
#             continue
#         my_trackings.add(my_tracking_number)
#         if my_tracking_number in warehouse_trackings:
#             cell.fill = PatternFill()  # no_fill
#         else:
#             cell.fill = PatternFill(
#                 start_color="FFFF00", end_color="FFFF00", fill_type="solid"  # yellow_fill
#             )
#
#     is_mine_but_not_in_warehouse = my_trackings - warehouse_trackings
#     in_warehouse_but_is_not_mine = warehouse_trackings - my_trackings
#     matched_my_trackings_with_warehouse = my_trackings & warehouse_trackings
#
#     put_worksheet_data_by_axis(
#         sheet=sheet_2,
#         axis='C',
#         dataset=matched_my_trackings_with_warehouse,
#         value_title="Trackings Matched",
#         value_font=Font(name="Times New Roman", color="006400", size=12),  # Dark Green
#     )
#     put_worksheet_data_by_axis(
#         sheet=sheet_2,
#         axis='D',
#         dataset=is_mine_but_not_in_warehouse,
#         value_title="Trackings not yet Received in Warehouse",
#         value_font=Font(name="Times New Roman", color="8B0000", size=12),  # Dark Red
#         uniform_column_width=50
#     )
#     put_worksheet_data_by_axis(
#         sheet=sheet_2,
#         axis='E',
#         dataset=in_warehouse_but_is_not_mine,
#         value_title="Others' Trackings Received in Warehouse",
#         value_font=Font(name="Times New Roman", color="8B0000", size=12),  # Dark Red
#         uniform_column_width=50
#     )
#
#
# workbook_filepath = "dx.xlsx"
# # workbook_filepath = ask_for_excel_filepath("Please enter the excel file path: ")
# workbook: Workbook = load_workbook(workbook_filepath)
#
# automation_for_sheet_1(
#     workbook["Sheet1"],
#     access_carrier_side=False
# )
# workbook.save(filename=workbook_filepath)
# print("\nSuccessfully saved workbook to disk.\n", end="")
#
# automation_for_sheet_1(
#     workbook["Sheet1"],
#     access_apple_side=False
# )
# workbook.save(filename=workbook_filepath)
# print("\nSuccessfully saved workbook to disk.\n", end="")
#
# automation_for_sheet_2(
#     workbook["Sheet1"],
#     workbook["Sheet2"]
# )
# workbook.save(filename=workbook_filepath)
# print("\nSuccessfully saved workbook to disk.\n", end="")
