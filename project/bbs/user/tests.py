from django.urls import reverse
from .models import User, AuthUser, Files  # AuthUser 是django提供的
from post.models import Post
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver


class Test(StaticLiveServerTestCase):
    """
    author: Edgar
    """

    def setUp(self) -> None:
        auth = AuthUser(username="test", email="test@qq.com")
        auth.set_password("123456")  # 设置密码，不能够直接设置
        auth.save()
        user = User(user=auth, sex=True, question="tests", answer="answer")  # 用户写入数据库，并设置密保
        user.save()
        # 文件
        Files.objects.create(name="test", path="/media/files/test.png", user_id=1, type="软件工程", download_times=0,
                             desc="测试")
        # 帖子记录
        Post.objects.create(topic="test", counter=0, author_user_id=1, content="test content", course="软件工程")

        self.browser = webdriver.Firefox()

    def test_login_and_logout(self):
        """用户的登录和登出"""
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
        self.browser.find_element_by_xpath('/html/body/div/nav/div/div/div/a').click()  # 点击头像，出现选项
        self.browser.find_element_by_xpath('/html/body/div/nav/div/div/div/div/a[3]').click()  # 登出
        self.assertEqual(self.browser.find_element_by_xpath('/html/body/div/nav/div/a[1]').text, "登录")   # 登出之后，会出现登出二字

    def test_signup(self):
        """用户的注册"""
        url = self.live_server_url + reverse("user:signup")
        self.browser.get(url)
        self.browser.find_element_by_xpath('//*[@id="username"]').send_keys("hello")  # 输入用户名
        self.browser.find_element_by_xpath('//*[@id="email"]').send_keys("123@qq.com")  # 输入邮箱
        self.browser.find_element_by_xpath('//*[@id="password"]').send_keys("123456")  # 输入密码
        self.browser.find_element_by_xpath('//*[@id="confirm"]').send_keys("123456")  # 确认密码
        self.browser.find_element_by_xpath('//*[@id="btn"]').click()  # 点击注册
        result = self.browser.find_element_by_xpath("/html/body/div/nav/div/div/div/div")  # 注册之后会自动登录，登录之后会出现个人中心
        self.assertIsNotNone(result.get_attribute("innerHTML"))


    def test_forget(self):
        """密码忘记根据密保找回"""
        url = self.live_server_url + reverse("user:forget")
        self.browser.get(url)
        self.browser.find_element_by_xpath('//*[@id="username"]').send_keys("test")  # 输入用户名
        self.browser.find_element_by_xpath('//*[@id="btn"]').click()  # 点击提交到另一个界面
        self.browser.find_element_by_xpath('//*[@id="answer"]').send_keys("answer")  # 回答问题
        self.browser.find_element_by_xpath('//*[@id="btn"]').click()  # 提交
        message = self.browser.find_element_by_xpath('/html/body/div/div/div')  # 重置成功之后会有提示信息
        self.assertEqual(message.text, "您的密码已经重置为:123456 请返回主页重新登陆")

    def test_set_pwdquestion(self):
        """密保修改"""
        self.login('test', '123456')
        url = self.live_server_url + reverse("user:setquestion")
        self.browser.get(url)
        self.browser.find_element_by_xpath('//*[@id="oldAnswer"]').send_keys('answer')  # 输入旧答案
        self.browser.find_element_by_xpath('//*[@id="newQuestion"]').send_keys('NewTest')  # 输入新问题
        self.browser.find_element_by_xpath('//*[@id="newAnswer"]').send_keys('Answer')  # 输入新答案
        self.browser.find_element_by_xpath('//*[@id="btn"]').click()  # 确定
        user=User.objects.get(user__username='test')
        answer=user.answer
        self.assertEqual(answer, 'Answer')

    def tearDown(self) -> None:
        self.browser.close()

