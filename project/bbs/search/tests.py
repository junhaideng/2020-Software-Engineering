from django.test import TestCase, Client
from course.models import Course
from post.models import Post
from django.urls import reverse
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from user.models import Files, User, AuthUser


class Test(TestCase):
    def setUp(self) -> None:
        Course.objects.create(name="数据结构", type="必修", school="电院")
        Post.objects.create(topic="测试", author_user_id=1, content="This is for test", course="数据结构", counter=0)

        # 文件下载界面的测试
        auth = AuthUser(username="test")
        auth.set_password("123456")
        auth.save()
        User.objects.create(user=auth)
        Files.objects.create(user_id=1, type="软件工程", download_times=0, path="/media/files/test.png", name="测试文件",
                             desc="暂无介绍")
        self.client = Client()

    # 如果需要下面的测试，view中对应的要取消注释，否则错误
    # def test_search_post_via_ajax(self):
    #     """测试请求满足条件返回的帖子"""
    #     data = self.client.post(reverse("search:search_post"), {"value": "测试", "type": "post"})
    #     self.assertEqual(data.json().get("data")[0].get("content"), "This is for test")
    #
    # def test_search_course_via_ajax(self):
    #     """测试请求满足条件返回的课程"""
    #     data = self.client.post(reverse("search:search_course"), {"value": "数据结构", "type": "course"})
    #     self.assertEqual(data.json().get("data")[0].get("id"), 1)

    def test_search_files_via_ajax(self):
        """测试满足条件的文件"""
        data = self.client.post("/download/", {"value": "软件"})
        self.assertEqual(data.json().get("data")[0].get("name"), "测试文件")  # 第一个文件名称


class TestTemplates(StaticLiveServerTestCase):
    def setUp(self) -> None:
        Course.objects.create(name="数据结构", type="必修", school="电院")
        Post.objects.create(topic="测试", author_user_id=1, content="This is for test", course="数据结构", counter=0)
        auth = AuthUser(username="test")
        auth.set_password("123456")
        auth.save()
        User.objects.create(user=auth)
        Files.objects.create(user_id=1, type="软件工程", download_times=0, path="/media/files/test.png", name="测试文件",
                             desc="暂无介绍")
        self.browser = webdriver.Firefox()  # 这里将webdriver放在python Script目录下

    def test_search_post_in_url(self):
        """在网页上模拟操作搜索到对应的帖子"""
        url = self.live_server_url + reverse("search:search_post") + "?keyword=测试"  # 对应的搜索
        self.browser.get(url)
        text = self.browser.find_element_by_class_name("layui-btn").text  # 右上角详情的按钮
        self.assertEqual(text.strip(), "详情>>")

    def test_search_course_in_url(self):
        """在网页上模拟操作搜索到对应的课程"""
        url = self.live_server_url + reverse("search:search_course") + "?keyword=数据结构"
        self.browser.get(url)
        element = self.browser.find_element_by_xpath('/html/body/div/div[1]/blockquote/a/button')
        self.assertEqual(element.text.strip(), "详情>>")

    def test_files_in_url(self):
        url = self.live_server_url + "/download"
        self.browser.get(url)
        element = self.browser.find_element_by_xpath('/html/body/div/div[2]/ul/div/div/div[1]/a')
        self.assertEqual(element.text.strip(), "测试文件")

    def tearDown(self) -> None:
        self.browser.close()
