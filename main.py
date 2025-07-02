from os import getcwd

# from time import sleep as thread_sleep

from ChromePageRender import (
    # something else
    Options as ChromeOptions,
    ChromePageRender
)

from dominate import document as HTMLDocument, tags as HTMLTags, util as HTMLUtils
from bs4 import BeautifulSoup

# import os, sys
# os.add_dll_directory(os.path.join(sys.exec_prefix, "Library", "bin"))
from weasyprint import HTML, CSS

# '''
#     You must properly set up this <__chrome_driver_filepath> to run this script..!
# '''
__chrome_driver_filepath: str = "./chromedrivers/chromedriver-win64-v138.0.7204.92/chromedriver.exe"

new_document: HTMLDocument = HTMLDocument(title="国内外知名智库精选数据", lang='zh')
with new_document.head:
    HTMLTags.meta(
        charset='utf-8',
        name='viewport',
        content='width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no'
    )
    HTMLTags.link(
        rel='stylesheet',
        href='./index.css'
    )


def handler1(site_name: str, site_url: str, html_content: str):
    # written for '中国人民大学国家发展与战略研究院（学者观点）'
    # this function adds site_name and html_content into new_document in an elegant way
    # get search for HTML elements in html_content
    soup = BeautifulSoup(html_content, "html.parser")
    # apply CSS selector
    briefItems = soup.select('div.briefItem')
    # edit original information
    for briefItem in briefItems:
        briefItem['class'] = ['page-board-item']
        commonAs = briefItem.select('a.commonA')
        for commonA in commonAs:
            commonA.attrs.pop('class', None)
            commonA['href'] = f"{site_url[:site_url.rfind('/')]}/{commonA['href']}"
    # add information into new_document body
    with new_document.body:
        with HTMLTags.div(cls='page-board'):
            with HTMLTags.a(href=site_url):
                HTMLTags.h2(site_name)
            for briefItem in briefItems:
                HTMLUtils.raw(str(briefItem))


URLData = {
    '中国人民大学国家发展与战略研究院（学者观点）': {
        'URL': 'http://nads.ruc.edu.cn/zkdt/xzgd/index.htm',
        'SelectorType': 'css',
        'RulesAwaitingSelectors': ['div.commonRight', 'div.commonRightTitle', 'div.Brief', 'div.briefItem',
                                   'a.commonA'],
        'HTMLContentHandler': handler1
    },
}
for url_name in URLData.keys():
    chrome_options = ChromeOptions()
    # chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--ignore-ssl-errors")
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--disable-site-isolation-trials")
    chrome_options.add_argument("--test-type")
    chrome_options.set_capability("acceptInsecureCerts", True)
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    )
    chrome_page_render = ChromePageRender(
        chrome_driver_filepath=__chrome_driver_filepath,
        options=chrome_options
    )
    url_data = URLData[url_name]
    url = url_data['URL']
    (html_content, is_timed_out) = chrome_page_render.get_html_text_awaiting_selector(
        url=url,
        selector_type='css' if url_data['SelectorType'] == 'css' else 'xpath',
        rules_awaiting_selectors=url_data['RulesAwaitingSelectors'],
        timeout_seconds=30,
        print_error_log_to_console=True
    )
    chrome_page_render.close()
    if is_timed_out:
        continue
    url_data['HTMLContentHandler'](
        site_name=url_name,
        site_url=url,
        html_content=html_content
    )

html_content = new_document.render(pretty=True)
# with open("./generated_html/index.html", "w", encoding="utf-8") as html_file:
#     html_file.write(html_content)  # pretty makes the HTML file human-readable
#     html_file.close()
# print("combined.html has been generated!")

HTML(string=html_content, base_url=getcwd()).write_pdf(
    './generated_html/index.pdf',
    # stylesheets=[CSS(filename='./generated_html/index.css')]
)