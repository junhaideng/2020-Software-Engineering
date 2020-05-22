from django.test import Client
from course.models import Course
from django.urls import reverse
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class Test(StaticLiveServerTestCase):
    """
    author: Edgar
    """

    def setUp(self) -> None:
        Course.objects.create(name="数据结构", school="电院")  # 创建数据库
        Course.objects.create(name="高等数学", school="数学院")
        self.client = Client()
        self.browser = webdriver.Firefox()

    def test_get_all_course(self):
        """测试获取所有的课程"""
        url = reverse("course:get_all")
        res = self.client.get(url)
        self.assertIn("数据结构", res.json().get("data"))

    def test_get_course_satisfy(self):
        """选择条件之后满足条件的课程"""
        url = self.live_server_url + reverse("course:coursedes", args=[])  # 对应满足条件的界面, TODO: 修改成搜索数据结构的url
        self.browser.get(url)
        self.browser.find_element_by_xpath("/html/body/div/div[2]")  # 满足条件的第一个返回内容
        element = self.browser.find_element_by_xpath('/html/body/div/div[2]/div/label[1]')  # 课程的名称
        self.assertEqual(element.text, "数据结构")

    def test_course_detail(self):
        url = self.live_server_url + reverse("course:coursedes", args=[1])  # 这里1表示的是id为1的课程，也就是 `数据结构`
        self.browser.get(url)
        element = self.browser.find_element_by_xpath('/html/body/div/table/tbody/tr[1]/td[2]')  # 找到课程的名称
        self.assertEqual(element.text, "数据结构")

    def tearDown(self) -> None:
        self.browser.close()
