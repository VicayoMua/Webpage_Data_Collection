from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

import undetected_chromedriver
from typing import Literal

from urllib.parse import urlparse as url_parse

def is_valid_url(url):
    parsed = url_parse(url)
    return (parsed.scheme in ["http", "https"]) and (parsed.netloc != "")

class SafeChrome(webdriver.Chrome):
    def __del__(self):
        """Suppress __del__ cleanup to avoid invalid handle errors."""
        pass


class SafeChromeUndetected(undetected_chromedriver.Chrome):
    def __del__(self):
        """Suppress __del__ cleanup to avoid invalid handle errors."""
        pass


class ChromePageRender:
    def __init__(self, chrome_driver_filepath: str, options: Options, use_undetected_chromedriver: bool = False):
        self.__browser = SafeChrome(
            service=Service(chrome_driver_filepath),
            options=options
        ) if not use_undetected_chromedriver else SafeChromeUndetected(
            service=Service(chrome_driver_filepath),
            options=options
        )

    def get_page_source(self) -> str:
        return self.__browser.page_source

    def goto_url_awaiting_selectors(
            self,
            url: str,
            selector_types_rules: list[tuple[Literal['css', 'xpath'], str]],
            waiting_timeout_in_seconds: float,
            print_error_log_to_console: bool = False
    ) -> bool:  # is_timed_out: bool
        if not isinstance(url, str):
            raise TypeError('Given url is not a string.')
        if not is_valid_url(url):
            raise ValueError('Given url is invalid, or it does not start with http or https.')
        self.__browser.get(url)
        try:
            patched_timeout_in_seconds = waiting_timeout_in_seconds / len(selector_types_rules)
            for (selector_type, selector_rule) in selector_types_rules:
                by = None
                if selector_type == 'css':
                    by = By.CSS_SELECTOR
                elif selector_type == 'xpath':
                    by = By.XPATH
                else:
                    raise TypeError(f"Selector type {selector_type} is not supported.")
                WebDriverWait(self.__browser, patched_timeout_in_seconds).until(
                    expected_conditions.presence_of_element_located((by, selector_rule))
                )
            return False
        except TimeoutException:
            if print_error_log_to_console:
                print(
                    f"ChromePageRender: get_html_text_with_selector: Timeout ({waiting_timeout_in_seconds} sec)."
                )
            return True

    def click_on_html_element(
            self,
            selector_type: Literal["css", "xpath"],
            selector_rule: str,
            waiting_timeout_in_seconds: float,
            use_javascript: bool,
            print_error_log_to_console: bool = False
    ) -> bool:
        """
        Clicks the first matching element by selector.
        Returns True if successful, False if timeout.
        """
        try:
            by = None
            if selector_type == 'css':
                by = By.CSS_SELECTOR
            elif selector_type == 'xpath':
                by = By.XPATH
            else:
                raise TypeError(f"Selector type {selector_type} is not supported.")
            html_element = WebDriverWait(self.__browser, waiting_timeout_in_seconds).until(
                expected_conditions.element_to_be_clickable((by, selector_rule))
            )
            if use_javascript:
                self.__browser.execute_script('arguments[0].click();', html_element)
            else:
                html_element.click()
            return True
        except TimeoutException:
            if print_error_log_to_console:
                print(f"ChromePageRender: click_element: Timeout after {waiting_timeout_in_seconds} seconds.")
            return False

    # def take_screenshot(self, save_path: str):
    #     self.__browser.save_screenshot(save_path)

    def close(self) -> None:
        if self.__browser:
            self.__browser.quit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()