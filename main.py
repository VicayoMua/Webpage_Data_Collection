# from os import getcwd
# from time import sleep as thread_sleep

from datetime import datetime

# configure <current_time> instance object
current_time = datetime.now()

from ChromePageRender import (
    # something else
    Options as ChromeOptions,
    ChromePageRender
)

# configure chrome driver path
__chrome_driver_path: str = './chromedrivers/chromedriver-win64-v138.0.7204.92/chromedriver.exe'

from dominate import document as HTMLDocument, tags as HTMLTags, util as HTMLUtils
from bs4 import BeautifulSoup
from tqdm import tqdm as LoopMeter

# configure new HTML document header and body
new_document: HTMLDocument = HTMLDocument(title='知名智库精选数据', lang='zh')
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
with new_document.body:
    HTMLTags.h1(
        f"知名智库精选数据（更新时间：{current_time.year}/{current_time.month:02d}/{current_time.day:02d} {current_time.hour:02d}:{current_time.minute:02d}:{current_time.second:02d}）"
    )


# ---------------------------------------------------------------------------------------------------------------------
# |                                  The following code collects online data.                                         |
# ---------------------------------------------------------------------------------------------------------------------


def handler1(document: HTMLDocument, site_name: str, site_logo_path: str, site_urls_contents: dict[str, str]):
    # written for '中国人民大学国家发展与战略研究院（学者观点）'
    # this function adds <site_name> and <site_urls_contents> into <document> in an elegant way
    with document.body:
        with HTMLTags.div(cls='page-board'):  # create a new board for this url series
            HTMLTags.img(cls='site-logo', src=site_logo_path, alt='Missing Logo')
            for (index, (url, html_content)) in enumerate(site_urls_contents.items()):  # view each url-html pair
                if html_content is None:
                    continue
                with HTMLTags.a(href=url):
                    HTMLTags.h2(f"{site_name} 第{index + 1}页")
                url_root = url[:url.rfind('/')]  # compute the url root to deal with relative href links
                soup = BeautifulSoup(html_content, 'html.parser')  # create HTML parser
                for briefItem in soup.select('div.briefItem'):  # search all the HTML elements according to CSS selector
                    # edit each original HTML element -- !!! THIS STEP IS USUALLY DIFFERENT FROM WEBSITES !!!
                    briefItem['class'] = ['page-board-item']
                    commonAs = briefItem.select('a.commonA')
                    for commonA in commonAs:
                        commonA.attrs.pop('class', None)
                        commonA['href'] = f"{url_root}/{commonA['href']}"
                    # append the edited HTML element
                    HTMLUtils.raw(str(briefItem))


URLData = {
    '中国人民大学国家发展与战略研究院（学者观点）': {
        'URLs': [
            'http://nads.ruc.edu.cn/zkdt/xzgd/index.htm',
            'http://nads.ruc.edu.cn/zkdt/xzgd/index1.htm',
        ],
        'SelectorType': 'css',
        'RulesAwaitingSelectors': [
            'div.commonRight',
            'div.commonRightTitle',
            'div.Brief',
            'div.briefItem',
            'a.commonA'
        ],
        'LogoPath': './Logos/handler1.png',
        'HTMLContentHandler': handler1
    },
}
for url_name in LoopMeter(
        URLData.keys(),
        unit="site",  # should be single form in English since it's too slow
        unit_scale=False
):
    chrome_options = ChromeOptions()
    # chrome_options.add_argument('--incognito')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_argument('--allow-running-insecure-content')
    chrome_options.add_argument('--disable-web-security')
    chrome_options.add_argument('--disable-site-isolation-trials')
    chrome_options.add_argument('--test-type')
    chrome_options.set_capability('acceptInsecureCerts', True)
    chrome_options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    )
    chrome_page_render = ChromePageRender(
        chrome_driver_filepath=__chrome_driver_path,
        options=chrome_options
    )
    print(f'start collecting data from {url_name}.')
    url_data = URLData[url_name]
    urls_contents = dict()
    for url in url_data['URLs']:
        (html_content, is_timed_out) = chrome_page_render.get_html_text_awaiting_selector(
            url=url,
            selector_type='css' if url_data['SelectorType'] == 'css' else 'xpath',
            rules_awaiting_selectors=url_data['RulesAwaitingSelectors'],
            timeout_seconds=30,
            print_error_log_to_console=True
        )
        urls_contents[url] = html_content if not is_timed_out else None
    if len(urls_contents) > 0:
        url_data['HTMLContentHandler'](
            document=new_document,
            site_name=url_name,
            site_logo_path=url_data['LogoPath'],
            site_urls_contents=urls_contents
        )

# ---------------------------------------------------------------------------------------------------------------------
# |                      The following code saves collected online data to local disk.                                |
# ---------------------------------------------------------------------------------------------------------------------


new_html_content = new_document.render(pretty=True)
try:
    with open('./generated_html/index.html', 'w', encoding='utf-8') as html_file:
        html_file.write(new_html_content)  # pretty makes the HTML file human-readable
        html_file.close()
    print('successfully generated ./generated_html/index.html')
except Exception as e:
    print('failed to write "./generated_html/index.html".')
