from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from django.urls import reverse
from post.models import Post
from django.test import Client, TransactionTestCase
from user.models import AuthUser, User


class Test(StaticLiveServerTestCase):
    """
    author: Edgar
    """

    def setUp(self) -> None:
        Post.objects.create(topic="test", counter=0, content="test content", course="软件工程", author_user_id=1)  # 创建帖子
        self.browser = webdriver.Firefox()

    def test_post_detail(self):
        """测试帖子的详情页"""
        url = self.live_server_url + reverse("community:detail", args=[1])  # id为1的帖子详情页
        self.browser.get(url)
        element = self.browser.find_element_by_xpath('/html/body/div/div[1]/div/div[1]/div/span')  # 课程标签
        self.assertEqual(element.text, "软件工程")


class Test2(TransactionTestCase):
    """
    author: Edgar
    测试其他的网页，因为其返回的类型为json，下面的测试方式较好
    """

    def setUp(self) -> None:
        Post.objects.create(topic="test", counter=0, content="test content", course="软件工程", author_user_id=1)  # 创建帖子
        auth = AuthUser.objects.create(username="test")  # 创建用户
        auth.set_password("123456")
        auth.save()
        User.objects.create(user=auth)
        self.client = Client()

    def test_reply_post(self):
        """回答帖子内容"""
        self.client.login(username="test", password="123456")
        res = self.client.post(reverse("community:reply"),
                               data={"id": 1, "content": "test reply"})  # 对id为1的帖子进行回答，也就是定义的帖子
        self.assertEqual(res.json().get("message"), "回答成功")

    def test_comment_reply(self):
        """评论回答"""
        self.client.login(username="test", password="123456")
        res = self.client.post(reverse("community:comment"),
                               data={"id": 1, "content": "test comment"})  # 对id为1的回答进行评论，也就是上面的回答
        self.assertEqual(res.json().get("message"), "评论成功")
