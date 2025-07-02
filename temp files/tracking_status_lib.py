# from ChromePageRender import *
# from tqdm import tqdm
#
# # with open("./output_ups_ontheway.txt", "r", encoding="utf-8") as file:
# #     content = file.read()
# #     print(get_ups_status(content))
# # with open("./output_ups_delivered.txt", "r", encoding="utf-8") as file:
# #     content = file.read()
# #     print(get_ups_status(content))
#
#
# # '''
# #     This function uses <requests> library, but may need <playwright> library in the future...
# #     When successful, it returns:
# #         ([("fedex", <Tracking URL>), ("ups", <Tracking URL>), ("cancelled", None),...], TIMED_OUT_COUNT)
# # '''
# def get_apple_order_tracking_urls(
#         apple_order_urls: set[str] | list[str],
#         chrome_page_render: ChromePageRender,
#         print_error_log_to_console: bool = False
# ) -> (list[(str or None, str or None)], int):  # (apple_results: list[(str, str)], timed_out_count: int)
#     if apple_order_urls is None or chrome_page_render is None:
#         return ([(None, None)], 0)
#
#     def get_apple_order_info(final_html_text: str) -> (str, str):
#
#         def find_possible_tracking_url1() -> str or None:
#             leading_index = final_html_text.find("\"trackingUrls\":[\"")
#             if leading_index == -1:
#                 return None
#             leading_index += 17
#             ending_index = final_html_text.find("\"]", leading_index)
#             return final_html_text[leading_index:ending_index]
#
#         def find_possible_tracking_url2() -> str or None:
#             leading_index = final_html_text.find("\"trackingURLMap\":{\"")
#             if leading_index == -1:
#                 return None
#             leading_index += 19
#             leading_index = final_html_text.find("\":\"", leading_index) + 3
#             ending_index = final_html_text.find("\"}", leading_index)
#             return final_html_text[leading_index:ending_index]
#
#         if "Cancelled</span></h2>" in final_html_text:
#             return ("cancelled", None)
#         finders = [
#             find_possible_tracking_url1,
#             find_possible_tracking_url2
#         ]
#         for finder in finders:
#             tracking_url = finder()
#             if tracking_url is not None:
#                 if "fedex" in tracking_url:
#                     return ("fedex", tracking_url)
#                 if "ups" in tracking_url:
#                     return ("ups", tracking_url)
#                 return ("unknown", tracking_url)
#         return (None, None)
#
#     apple_results: list[(str, str)] = []
#     timed_out_count: int = 0
#     for apple_order_url in tqdm(apple_order_urls, desc="Processing Apple Order URLs"):
#         if apple_order_url is None:
#             apple_results.append((None, None))
#             continue
#         try:
#             (html_text, is_timed_out) = chrome_page_render.get_html_text_with_selector(
#                 url=apple_order_url,
#                 selector_type="css",
#                 selector_rules=['body#body-main.black'],
#                 timeout_seconds=3,
#                 print_error_log_to_console=print_error_log_to_console
#             )
#             if is_timed_out:
#                 timed_out_count += 1
#                 raise Exception("HTML page render timed out")
#             else:
#                 apple_results.append(get_apple_order_info(html_text))
#         except Exception as e:
#             if print_error_log_to_console:
#                 print(f"get_apple_order_tracking_urls: Error?? {str(e)}")
#             apple_results.append((None, None))
#
#     return (apple_results, timed_out_count)
#
#
# # '''
# #     This function uses <selenium> library with <chrome driver> via <ChromePageRender.py> file.
# #     This function will not raise any Exceptions.
# #     It returns:
# #         ([(main_delivery_status, delivery_time), ...], TIMED_OUT_COUNT)
# # '''
# def get_fedex_delivery_status(
#         fedex_tracking_urls: set[str] | list[str],
#         chrome_page_render: ChromePageRender,
#         print_error_log_to_console: bool = False
# ) -> (list[(str or None, str or None)], int):
#     if fedex_tracking_urls is None or chrome_page_render is None:
#         return ([(None, None)], 0)
#
#     def get_fedex_status(final_html_text: str) -> (str, str):
#
#         def purify_tracking_text(date_text: str, time_text: str) -> str:
#             pass
#
#         main_status_keyword = "<span data-test-id=\"delivery-date-header\" class=\"fdx-c-eyebrow--extra-small\"> "
#         leading_index_0 = final_html_text.find(main_status_keyword) + len(main_status_keyword)
#         ending_index_0 = final_html_text.find(" </span>", leading_index_0)
#         if leading_index_0 == -1 or ending_index_0 == -1:
#             return (None, None)
#         detailed_status_keyword_1 = "<span class=\"deliveryDateText\">"
#         leading_index_1 = final_html_text.find(detailed_status_keyword_1, ending_index_0) + len(
#             detailed_status_keyword_1)
#         ending_index_1 = final_html_text.find("</span>", leading_index_1)
#         if leading_index_1 == -1 or ending_index_1 == -1:
#             return (final_html_text[leading_index_0:ending_index_0], None)
#         detailed_status_keyword_2 = "<span class=\"deliveryDateTextBetween\">"
#         leading_index_2 = final_html_text.find(detailed_status_keyword_2, ending_index_1) + len(
#             detailed_status_keyword_2)
#         ending_index_2 = final_html_text.find("</span>", leading_index_2)
#         if leading_index_2 == -1 or ending_index_2 == -1:
#             return (final_html_text[leading_index_0:ending_index_0], None)
#         return (
#             final_html_text[leading_index_0:ending_index_0],
#             final_html_text[leading_index_1:ending_index_1] + " " + final_html_text[leading_index_2:ending_index_2]
#         )
#
#     fedex_results: list[(str, str)] = []
#     timed_out_count: int = 0
#     for fedex_tracking_url in tqdm(fedex_tracking_urls, desc="Processing Fedex Tracking URLs"):
#         if fedex_tracking_url is None:
#             fedex_results.append((None, None))
#             continue
#         try:
#             (html_text, is_timed_out) = chrome_page_render.get_html_text_with_selector(
#                 url=fedex_tracking_url,
#                 selector_type="css",
#                 selector_rules=['span.fdx-c-eyebrow--extra-small', 'span.deliveryDateText',
#                                 'span.deliveryDateTextBetween'],
#                 timeout_seconds=5,
#                 print_error_log_to_console=print_error_log_to_console
#             )
#             if is_timed_out:
#                 timed_out_count += 1
#                 raise Exception("HTML page render timed out")
#             else:
#                 fedex_results.append(get_fedex_status(html_text))
#         except Exception as e:
#             if print_error_log_to_console:
#                 print(f"get_fedex_delivery_status: Error?? {str(e)}")
#             fedex_results.append((None, None))
#
#     return (fedex_results, timed_out_count)
#
#
# # '''
# #     This function uses <selenium> library with <chrome driver> via <ChromePageRender.py> file.
# #     This function will not raise any Exceptions.
# #     It returns:
# #         ([(main_delivery_status, delivery_time), ...], TIMED_OUT_COUNT)
# # '''
# def get_ups_delivery_status(
#         ups_tracking_urls: set[str] | list[str],
#         chrome_page_render: ChromePageRender,
#         print_error_log_to_console: bool = False
# ) -> (list[(str or None, str or None)], int):
#     if ups_tracking_urls is None or chrome_page_render is None:
#         return ([(None, None)], 0)
#
#     def get_ups_status(final_html_text: str) -> (str, str):
#
#         def purify_tracking_text(date_text: str, time_text: str) -> str:
#
#             def eliminate_meaningless_space(text: str) -> str:
#                 new_text = ""
#                 first_time = False
#                 for char in text:
#                     if char.isalnum() or char in ":.,":
#                         new_text += char
#                         first_time = True
#                     else:
#                         if first_time:
#                             new_text += " "
#                             first_time = False
#                 return new_text[:-1] if new_text.endswith(" ") else new_text
#
#             date_text = eliminate_meaningless_space(date_text)
#             time_text = eliminate_meaningless_space(time_text)
#             combined_text = date_text + " " + time_text
#             if "span" in combined_text: combined_text = combined_text.replace("span", "")
#             return combined_text.replace("  ", " ")
#
#         delivered_on_text_index = final_html_text.find("Delivered On")
#         if delivered_on_text_index != -1:
#             delivered_date_leading_index = final_html_text.find(
#                 "id=\"st_App_PkgStsMonthNum\" class=\"ups-txt_size_xl ups-txt_teal ups-txt_bold ng-star-inserted\">",
#                 delivered_on_text_index) + len(
#                 "id=\"st_App_PkgStsMonthNum\" class=\"ups-txt_size_xl ups-txt_teal ups-txt_bold ng-star-inserted\">")
#             delivered_date_ending_index = final_html_text.find("<strong", delivered_date_leading_index)
#             delivered_time_leading_index = final_html_text.find(
#                 "id=\"st_App_PkgStsTime\" class=\"ups-txt_teal ups-text_atomic ng-star-inserted\">",
#                 delivered_date_ending_index) + len(
#                 "id=\"st_App_PkgStsTime\" class=\"ups-txt_teal ups-text_atomic ng-star-inserted\">")
#             delivered_time_ending_index = final_html_text.find("</strong>", delivered_time_leading_index)
#             return ("Delivered",
#                     purify_tracking_text(final_html_text[delivered_date_leading_index:delivered_date_ending_index],
#                                          final_html_text[delivered_time_leading_index:delivered_time_ending_index]))
#         estimated_delivery_text_index = final_html_text.find("Estimated delivery")
#         if estimated_delivery_text_index != -1:
#             estimated_delivery_date_leading_index = final_html_text.find(
#                 "id=\"st_App_PkgStsTimeDayMonthNum\" class=\"ups-txt_size_xl ups-st_heading ups-txt_teal ups-txt_bold ng-star-inserted\">",
#                 estimated_delivery_text_index) + len(
#                 "id=\"st_App_PkgStsTimeDayMonthNum\" class=\"ups-txt_size_xl ups-st_heading ups-txt_teal ups-txt_bold ng-star-inserted\">")
#             estimated_delivery_date_ending_index = final_html_text.find("<span", estimated_delivery_date_leading_index)
#             estimated_delivery_time_leading_index = final_html_text.find(
#                 "id=\"stApp_packageStatusTimeLbl_by\" class=\"ng-star-inserted\">",
#                 estimated_delivery_date_ending_index) + len(
#                 "id=\"stApp_packageStatusTimeLbl_by\" class=\"ng-star-inserted\">")
#             estimated_delivery_time_ending_index = final_html_text.find("</p>", estimated_delivery_time_leading_index)
#             return (
#                 "On the way",
#                 purify_tracking_text(
#                     final_html_text[estimated_delivery_date_leading_index:estimated_delivery_date_ending_index],
#                     final_html_text[estimated_delivery_time_leading_index:estimated_delivery_time_ending_index]))
#         return (None, None)
#
#     ups_results: list[(str, str)] = []
#     timed_out_count: int = 0
#     for ups_tracking_url in tqdm(ups_tracking_urls, desc="Processing UPS Tracking URLs"):
#         if ups_tracking_url is None:
#             ups_results.append((None, None))
#             continue
#         try:
#             (html_text, is_timed_out) = chrome_page_render.get_html_text_with_selector(
#                 url=ups_tracking_url,
#                 selector_type="css",
#                 selector_rules=['.ups-txt_size_xl.ups-txt_teal.ups-txt_bold.ng-star-inserted'],
#                 timeout_seconds=5,
#                 print_error_log_to_console=print_error_log_to_console
#             )
#             if is_timed_out:
#                 timed_out_count += 1
#                 raise Exception("HTML page render timed out")
#             else:
#                 ups_results.append(get_ups_status(html_text))
#         except Exception as e:
#             if print_error_log_to_console:
#                 print(f"get_ups_delivery_status: Error?? {str(e)}")
#             ups_results.append((None, None))
#
#     return (ups_results, timed_out_count)
