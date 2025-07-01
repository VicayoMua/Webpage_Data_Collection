from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

import undetected_chromedriver
from typing import Literal


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

    def get_html_text_with_selector(
            self,
            url: str,
            selector_type: Literal["css", "xpath"],
            selector_rules: list[str],
            timeout_seconds: float,
            print_error_log_to_console: bool = False
    ) -> (str, bool):  # (page_cource: str, is_timed_out: bool)
        if not isinstance(url, str) or url.find("http") != 0:
            return ""
        self.__browser.get(url)
        try:
            patched_timeout_seconds = 1 / len(selector_rules)
            if selector_type == "css":
                for selector_rule in selector_rules:
                    WebDriverWait(self.__browser, timeout_seconds).until(
                        expected_conditions.presence_of_element_located((By.CSS_SELECTOR, selector_rule))
                    )
                    timeout_seconds = patched_timeout_seconds
            elif selector_type == "xpath":
                for selector_rule in selector_rules:
                    WebDriverWait(self.__browser, timeout_seconds).until(
                        expected_conditions.presence_of_element_located((By.XPATH, selector_rule))
                    )
                    timeout_seconds = patched_timeout_seconds
            else:
                raise Exception(
                    "ChromePageRender: get_html_text_with_selector: Error. Invalid selector_type. Use 'css' or 'xpath'.")
        except TimeoutException:
            if print_error_log_to_console:
                print(
                    f"ChromePageRender: get_html_text_with_selector: Timeout ({timeout_seconds} sec). Element with {selector_type} \"{selector_rule}\" is not found."
                )
            return (self.__browser.page_source, True)
        return (self.__browser.page_source, False)

    # def take_screenshot(self, save_path: str):
    #     self.__browser.save_screenshot(save_path)

    def close(self):
        if self.__browser:
            self.__browser.quit()
