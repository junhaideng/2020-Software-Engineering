from django.test import TestCase
from django.test import Client
from django.urls import reverse
from user.models import User, AuthUser


class Test(TestCase):
    """
    author: Edgar
    反馈界面的测试
    """
    def setUp(self) -> None:
        auth = AuthUser(username="test")  # 设置一个测试用户
        auth.set_password("123456")
        auth.save()
        User(user=auth).save()
        self.client = Client()

    def test_feedback(self):
        self.client.login(username="test", password="123456")  # 用户登录
        res = self.client.post(reverse("feedback:index"), data={"subject": "test", "content": "content", "type":0})
        self.assertEqual(res.status_code, 302)  # 反馈成功会重定向到该界面
        self.assertEqual(res.url, reverse("feedback:index"))  # 并且 url 保存不变

