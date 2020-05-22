from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium.common.exceptions import NoSuchElementException


class Test(StaticLiveServerTestCase):
    """
    author: Edgar
    """
    def setUp(self) -> None:
        self.browser = webdriver.Firefox()

    def test_home(self):
        url = self.live_server_url + reverse("home:index")  # 主页
        self.browser.get(url)
        try:
            element = self.browser.find_element_by_xpath('//*[@id="search"]')  # 搜索框
        except NoSuchElementException:
            element = None
        self.assertIsNotNone(element)  # 正常情况下是可以找到搜索框的

    def tearDown(self) -> None:
        self.browser.close()
