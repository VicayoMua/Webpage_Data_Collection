from ChromePageRender import (
    # something else
    Options as ChromeOptions,
    ChromePageRender
)

# '''
#     You must properly set up this <__chrome_driver_filepath> to run this script..!
# '''
__chrome_driver_filepath: str = "./chromedrivers/chromedriver-win64-v138.0.7204.92/chromedriver.exe"

from dominate import document as HTMLDocument
from dominate.tags import h1, p, a
from dominate.util import raw

# from bs4 import BeautifulSoup

# from time import sleep as thread_sleep

new_document: HTMLDocument = HTMLDocument(title="国内外知名智库精选数据")

def handler1(site_name: str, html_content: str):
    pass

URLData = {
    '中国人民大学国家发展与战略研究院': {
        'URL': 'http://nads.ruc.edu.cn/zkdt/xzgd/index.htm',
        'SelectorType': 'css',
        'SelectorRules': ['div.commonRight', 'div.commonRightTitle', 'div.Brief', 'div.briefItem', 'a.commonA'],
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
    (html_content, is_timed_out) = chrome_page_render.get_html_text_awaiting_selector(
        url=url_data['URL'],
        selector_type=url_data['SelectorType'],
        selector_rules=url_data['SelectorRules'],
        timeout_seconds=30,
        print_error_log_to_console=True
    )
    chrome_page_render.close()
    if is_timed_out:
        continue
    url_data['HTMLContentHandler'](
        url_name=url_name,
        html_content=html_content
    )

