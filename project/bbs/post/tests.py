from django.test import TestCase, Client
from django.urls import reverse
from user.models import User, AuthUser


class Test(TestCase):
    """
    测试发帖的功能
    author: Edgar
    """
    def setUp(self) -> None:
        auth = AuthUser(username="test")  # 创建用户
        auth.set_password("123456")
        auth.save()
        User.objects.create(user=auth)
        self.client = Client()

    def test_post(self):
        """测试发帖的功能, 发帖请求返回类型为json"""
        self.client.login(username="test", password="123456")
        res = self.client.post(reverse("post:index"), data={"topic": "test", "course": "软件工程", "content": "test content"})
        self.assertEqual(res.json().get("status"), "提交成功")

