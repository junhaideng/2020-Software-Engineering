from django.urls import reverse
from .models import User, AuthUser, Files  # AuthUser 是django提供的
from post.models import Post
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from time import sleep


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

    def login(self, username, password):
        """用来登录，非测试函数"""
        url = self.live_server_url + reverse("user:login")
        self.browser.get(url)
        _username = self.browser.find_element_by_id("username")
        _username.send_keys(username)  # 输入账号
        _password = self.browser.find_element_by_id("password")
        _password.send_keys(password)  # 输入密码
        btn = self.browser.find_element_by_xpath("/html/body/div/div/form/button")
        btn.click()  # 点击登录

    def test_login_and_logout(self):
        """用户的登录和登出"""
        self.login('test', '123456')
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

    def test_set_pwdquestion(self):
        """密保修改
        author: qsq
        """
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

    def test_reset_password(self):
        """密码重置"""
        self.login('test', '123456')
        url = self.live_server_url + reverse("user:resetpwd")
        self.browser.get(url)
        self.browser.find_element_by_xpath('//*[@id="oldpwd"]').send_keys('123456')  # 输入旧密码
        self.browser.find_element_by_xpath('//*[@id="newpwd"]').send_keys('test')  # 输入新密码
        self.browser.find_element_by_xpath('//*[@id="confirm"]').send_keys('test')  # 确认
        self.browser.find_element_by_xpath('//*[@id="btn"]').click()  # 确定
        self.login('test', 'test')
        element = self.browser.find_element_by_xpath('/html/body/div/nav/div/div/div/div/a[1]')  # 个人中心
        self.assertEqual(element.get_attribute('innerHTML'), "个人中心")

    def test_post_history(self):
        """发帖记录测试"""
        self.login('test', '123456')
        url = self.live_server_url + reverse("user:history")
        self.browser.get(url)
        topic = self.browser.find_element_by_xpath(
            '/html/body/div/div/div/div[2]/div/table/tbody/tr/td[1]').text  # 帖子主题
        content = self.browser.find_element_by_xpath(
            '/html/body/div/div/div/div[2]/div/table/tbody/tr/td[3]').text  # 帖子内容
        self.assertEqual(topic.strip(), "test")
        self.assertEqual(content.strip(), 'test content'[0:8] + "...")

    def test_my_files(self):
        """我的文件测试"""
        self.login('test', '123456')
        url = self.live_server_url + reverse('user:file')
        self.browser.get(url)
        name = self.browser.find_element_by_xpath(
            '/html/body/div/div/div/div[2]/div/table/tbody/tr[1]/td[1]').text  # 文件名
        type = self.browser.find_element_by_xpath(
            '/html/body/div/div/div/div[2]/div/table/tbody/tr[1]/td[2]').text  # 文件类型
        download_times = self.browser.find_element_by_xpath(
            '/html/body/div/div/div/div[2]/div/table/tbody/tr[1]/td[3]').text  # 文件下载次数
        self.assertEqual(name, "test")
        self.assertEqual(type, "软件工程")
        self.assertEqual(download_times, '0')

    def tearDown(self) -> None:
        self.browser.close()

    def test_profile(self):
        """
        用户资料显示
        author: 吴嘉锐
        """
        self.login('test', '123456')  # 登录
        url = self.live_server_url + reverse("user:profile")  # 再测试用户信息
        self.browser.get(url)
        # 获取显示的用户各项资料
        name = self.browser.find_element_by_xpath('/html/body/div/div/div/div[2]/div/div[2]').text  # 用户名
        sex = self.browser.find_element_by_xpath('/html/body/div/div/div/div[2]/div/div[3]').text  # 性别
        academy = self.browser.find_element_by_xpath('/html/body/div/div/div/div[2]/div/div[4]').text  # 学院
        grade = self.browser.find_element_by_xpath('/html/body/div/div/div/div[2]/div/div[5]').text  # 年级
        self.assertEqual(name, "昵称： test")
        self.assertEqual(sex, "性别： 男")
        self.assertEqual(academy, '学院： 未知')
        self.assertEqual(grade, "年级： 未知")

    def test_modify(self):
        """
            用户资料修改
            author: 吴嘉锐
        """
        self.login('test', '123456')
        url = self.live_server_url + reverse("user:modify")  # 修改个人资料
        self.browser.get(url)
        name = self.browser.find_element_by_id("nick")  # 修改用户名“modify_test”
        name.clear()
        name.send_keys("modify_test")
        select = Select(self.browser.find_element_by_name("sex"))  # 修改性别为女
        select.select_by_visible_text("女")
        self.browser.find_element_by_xpath("/html/body/div/div/div/div[2]/div/form/div[4]/div/select/option[2]").click()  # 修改学院船建
        self.browser.find_element_by_xpath("/html/body/div/div/div/div[2]/div/form/div[5]/div/select/option[3]").click()  # 修改年级大二
        self.browser.find_element_by_xpath("/html/body/div/div/div/div[2]/div/form/div[6]/button").click()  # 确认修改

        url = self.live_server_url + reverse("user:profile")  # 是否修改成功
        self.browser.get(url)
        # 获取显示的用户各项资料
        name = self.browser.find_element_by_xpath('/html/body/div/div/div/div[2]/div/div[2]').text
        sex = self.browser.find_element_by_xpath('/html/body/div/div/div/div[2]/div/div[3]').text
        academy = self.browser.find_element_by_xpath('/html/body/div/div/div/div[2]/div/div[4]').text
        grade = self.browser.find_element_by_xpath('/html/body/div/div/div/div[2]/div/div[5]').text
        self.assertEqual(name, "昵称： modify_test")
        self.assertEqual(sex, "性别： 女")
        self.assertEqual(academy, "学院： 船舶海洋与建筑工程学院")
        self.assertEqual(grade, "年级： 大二")
