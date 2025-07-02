# import re
# from bs4 import BeautifulSoup
#
# class HtmlObject:
#     def __init__(self, html: str):
#         # parse the HTML once
#         self.soup = BeautifulSoup(html, 'html.parser')
#
#     def findHTMLElement(self, query: str):
#         """
#         query should look like "<tag attr1=val1 attr2=val2>"
#         e.g. "<div class=class_name>" or "<a href='https://...'>"
#         """
#         # extract tag name and the rest (attributes)
#         m = re.match(r'<\s*(\w+)\s*([^>]*)>', query)
#         if not m:
#             raise ValueError(f"Invalid query format: {query!r}")
#         tag, attrs_str = m.group(1), m.group(2)
#
#         # parse key=value pairs (with or without quotes)
#         attrs = {}
#         for key, val in re.findall(r'(\w+)\s*=\s*["\']?([\w\-\:\/\.]+)["\']?', attrs_str):
#             attrs[key] = val
#
#         # use BeautifulSoup to find the first matching element
#         return self.soup.find(tag, attrs=attrs)
#
# def f(html_script: str) -> HtmlObject:
#     return HtmlObject(html_script)
