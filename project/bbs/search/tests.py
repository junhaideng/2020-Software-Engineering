from django.test import TestCase, Client
from course.models import Course
from post.models import Post
from django.urls import reverse
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class Test(TestCase):
    def setUp(self) -> None:
        Course.objects.create(name="数据结构", type="必修", school="电院")
        Post.objects.create(topic="测试", author_user_id=1, content="This is for test", course="数据结构", counter=0)
        self.client = Client()

    def test_search_post_via_ajax(self):
        """测试请求满足条件返回的帖子"""
        data = self.client.post(reverse("search:search"), {"value": "测试", "type": "post"})
        self.assertEqual(data.json().get("data")[0].get("content"), "This is for test")

    def test_search_course_via_ajax(self):
        """测试请求满足条件返回的课程"""
        data = self.client.post(reverse("search:search"), {"value": "数据结构", "type": "course"})
        self.assertEqual(data.json().get("data")[0].get("id"), 1)


class TestTemplates(StaticLiveServerTestCase):
    def setUp(self) -> None:
        Course.objects.create(name="数据结构", type="必修", school="电院")
        Post.objects.create(topic="测试", author_user_id=1, content="This is for test", course="数据结构", counter=0)
        self.browser = webdriver.Firefox()  # 这里将webdriver放在python Script目录下

    def test_search_post_in_url(self):
        url = self.live_server_url + reverse("search:search_post") + "?keyword=测试"
        self.browser.get(url)
        text = self.browser.find_element_by_class_name("layui-btn").text
        self.assertEqual(text.strip(), "详情>>")

    def test_search_course_in_url(self):
        url = self.live_server_url + reverse("search:search_course") + "?keyword=数据结构"
        self.browser.get(url)
        # TODO: 完成该部分内容

    def tearDown(self) -> None:
        self.browser.close()
