import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

num_retries = 3

def retry(func):
    def wrapper(*args, **kwargs):
        cnt = 0
        while cnt < num_retries:
            try:
                func(*args)
            except TimeoutException:
                cnt += 1
                print(f"time out. retrying... ({cnt}/{num_retries})")
            else:
                break
        else:
            raise TimeoutException(f"page was not loaded in {num_retries} times.")

    return wrapper


def init_driver(options):
    return webdriver.Chrome(options=options)


def set_wait(driver, time):
    return WebDriverWait(driver, time)


# @retry
def select_by_value_with_wait(value, wait, finder):    
    select = Select(wait.until(finder))
    select.select_by_value(value)
    # イベントハンドラによってHTMLがリロードされるため, waitする（これがない場合, element is not attached to the page documentが出る）
    # return Select(wait.until(finder))


def click_btn_with_wait(wait, finder):
    btn = wait.until(finder)
    btn.click()
    # return wait.until(finder)
