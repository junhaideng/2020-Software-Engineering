from django.test import TestCase
from django.urls import reverse
from selenium.webdriver.support import wait

from .models import User, AuthUser  # AuthUser 是django提供的
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver


class Test(StaticLiveServerTestCase):
    def setUp(self) -> None:
        auth = AuthUser(username="test", email="test@qq.com")
        auth.set_password("123456")  # 设置密码，不能够直接设置
        auth.save()
        user = User(user=auth, sex=True)
        user.save()
        self.browser = webdriver.Firefox()

    def test_login(self):
        url = self.live_server_url + reverse("user:login")
        self.browser.get(url)
        username = self.browser.find_element_by_id("username")
        username.send_keys("test")  # 输入账号
        password = self.browser.find_element_by_id("password")
        password.send_keys("123456")  # 输入密码
        btn = self.browser.find_element_by_xpath("/html/body/div/div/form/button")
        btn.click()  # 点击登录
        self.browser.implicitly_wait(1)  # 等待1s加载
        result = self.browser.find_element_by_xpath("/html/body/div/nav/div/div/div/div")  # 登录之后会出现个人中心
        self.assertIsNotNone(result.get_attribute("innerHTML"))  # 因为该元素需要触发然后才能获取到text内容，这里直接判断存在值

    def test_signup(self):
        url = self.live_server_url + reverse("user:signup")
        self.browser.get(url)
        self.browser.find_element_by_xpath('//*[@id="username"]').send_keys("hello")  # 输入用户名
        self.browser.find_element_by_xpath('//*[@id="email"]').send_keys("123@qq.com")  # 输入邮箱
        self.browser.find_element_by_xpath('//*[@id="password"]').send_keys("123456")  # 输入密码
        self.browser.find_element_by_xpath('//*[@id="confirm"]').send_keys("123456")  # 确认密码
        self.browser.find_element_by_xpath('//*[@id="btn"]').click()  # 点击注册
        result = self.browser.find_element_by_xpath("/html/body/div/nav/div/div/div/div")  # 注册之后会自动登录，登录之后会出现个人中心
        self.assertIsNotNone(result.get_attribute("innerHTML"))

    def tearDown(self) -> None:
        self.browser.close()

