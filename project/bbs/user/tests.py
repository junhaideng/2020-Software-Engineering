from django.urls import reverse
from .models import User, AuthUser  # AuthUser 是django提供的
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
        self.assertEqual(self.browser.find_element_by_xpath('/html/body/div/nav/div/a[1]').text, "登录")  # 登出之后，会出现登出二字

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

    def test_reset_password(self):
        pass

    def tearDown(self) -> None:
        self.browser.close()

    def test_profile(self):
        """
        用户资料显示
        author: 吴嘉锐
        """
        url = self.live_server_url + reverse("user:signup")  # 先进行注册
        self.browser.get(url)
        self.browser.find_element_by_xpath('//*[@id="username"]').send_keys("hello")  # 输入用户名
        self.browser.find_element_by_xpath('//*[@id="email"]').send_keys("123@qq.com")  # 输入邮箱
        self.browser.find_element_by_xpath('//*[@id="password"]').send_keys("123456")  # 输入密码
        self.browser.find_element_by_xpath('//*[@id="confirm"]').send_keys("123456")  # 确认密码
        self.browser.find_element_by_xpath('//*[@id="btn"]').click()  # 点击注册

        url = self.live_server_url + reverse("user:profile")  # 再测试用户信息
        self.browser.get(url)
        # 获取显示的用户各项资料
        name = self.browser.find_element_by_xpath('/html/body/div/div/div/div[2]/div/div[2]/text()').text
        sex = self.browser.find_element_by_xpath('/html/body/div/div/div/div[2]/div/div[3]/text()').text
        academy = self.browser.find_element_by_xpath('/html/body/div/div/div/div[2]/div/div[4]/text()').text
        grade = self.browser.find_element_by_xpath('/html/body/div/div/div/div[2]/div/div[5]/text()').text
        self.assertEqual(name, "hello")
        self.assertEqual(sex, "男")
        self.assertEqual(academy, "您还没有设置学院哦！")
        self.assertEqual(grade, "未知")

    def test_modify(self):
        """
            用户资料修改
            author: 吴嘉锐
        """
        url = self.live_server_url + reverse("user:signup")  # 先进行注册
        self.browser.get(url)
        self.browser.find_element_by_xpath('//*[@id="username"]').send_keys("hello")  # 输入用户名
        self.browser.find_element_by_xpath('//*[@id="email"]').send_keys("123@qq.com")  # 输入邮箱
        self.browser.find_element_by_xpath('//*[@id="password"]').send_keys("123456")  # 输入密码
        self.browser.find_element_by_xpath('//*[@id="confirm"]').send_keys("123456")  # 确认密码
        self.browser.find_element_by_xpath('//*[@id="btn"]').click()  # 点击注册

        url = self.live_server_url + reverse("user:modify")  # 修改个人资料
        self.browser.get(url)
        name = self.browser.find_element_by_id("nick")  # 修改用户名“modify_test”
        name.send_keys("modify_test")
        self.browser.find_element_by_xpath("/html/body/div/div/div/div[2]/div/form/div[2]/div").click()  # 修改性别为女
        self.browser.find_element_by_xpath("/html/body/div/div/div/div[2]/div/form/div[2]/div/select/option[3]").click()
        self.browser.find_element_by_xpath("/html/body/div/div/div/div[2]/div/form/div[3]/div").click()  # 修改学院船建
        self.browser.find_element_by_xpath("/html/body/div/div/div/div[2]/div/form/div[3]/div/select/option[2]").click()
        self.browser.find_element_by_xpath("/html/body/div/div/div/div[2]/div/form/div[4]/div").click()  # 修改年级大二
        self.browser.find_element_by_xpath("/html/body/div/div/div/div[2]/div/form/div[4]/div/select/option[3]").click()
        self.browser.find_element_by_xpath("/html/body/div/div/div/div[2]/div/form/div[6]/button").click()  # 确认修改

        url = self.live_server_url + reverse("user:profile")  # 是否修改成功
        self.browser.get(url)
        # 获取显示的用户各项资料
        name = self.browser.find_element_by_xpath('/html/body/div/div/div/div[2]/div/div[2]/text()').text
        sex = self.browser.find_element_by_xpath('/html/body/div/div/div/div[2]/div/div[3]/text()').text
        academy = self.browser.find_element_by_xpath('/html/body/div/div/div/div[2]/div/div[4]/text()').text
        grade = self.browser.find_element_by_xpath('/html/body/div/div/div/div[2]/div/div[5]/text()').text
        self.assertEqual(name, "modify_test")
        self.assertEqual(sex, "女")
        self.assertEqual(academy, "船舶海洋与建筑工程学院")
        self.assertEqual(grade, "大二")
