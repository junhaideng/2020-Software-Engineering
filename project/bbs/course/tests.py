from django.test import Client
from course.models import Course, CourseCom
from user.models import User, AuthUser
from django.urls import reverse
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class Test(StaticLiveServerTestCase):
    """
    author: Edgar
    """

    def setUp(self) -> None:
        Course.objects.create(name="数据结构", school="电子信息与电气工程学院", type="CO")  # 创建数据库
        Course.objects.create(name="高等数学", school="数学科学院", type="CO")

        # 用来测试评论
        course = Course.objects.create(name="软件工程", school="电子信息与电气工程学院", type="CO")
        auth = AuthUser(username="test")
        auth.set_password("123456")
        auth.save()
        User.objects.create(user=auth)
        # 如果不关联对应的用户，则会报错！ 这是由于views.py 查询comment的问题
        CourseCom.objects.create(courseid=course, com="Test", user_name="test")
        self.client = Client()
        self.browser = webdriver.Firefox()

    def test_get_all_course(self):
        """测试获取所有的课程"""
        url = reverse("course:get_all")
        res = self.client.get(url)
        self.assertIn("数据结构", res.json().get("data"))

    def test_get_course_satisfy(self):
        """选择条件之后满足条件的课程"""
        url = self.live_server_url + reverse("course:details",
                                             args=["CO", "1", "1"])  # 对应满足条件的界面
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

    def test_comment(self):
        """测试课程评论系统"""
        url = self.live_server_url + reverse("course:coursedes", args=[3])  # 这里1表示的是id为1的课程，也就是 `数据结构`
        self.browser.get(url)
        comment = self.browser.find_element_by_xpath('/html/body/div/div[1]/div[2]/div[2]')  # 找到对应评论
        self.assertEqual(comment.text, "Test")


