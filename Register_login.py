# main.py
import re
# kivy 引用
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.graphics import Color,Rectangle
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.core.text import LabelBase        # 统一中文字体
from kivy.uix.image import AsyncImage
from kivy.factory import Factory
from kivy.uix.popup import Popup
from kivy.clock import Clock
# 数据库 MySql引用
from MySql.connect_mysql import *
from Main_kivy import *


LabelBase.register(name='Font_Hanzi', fn_regular='kvcn.ttc')  # 导入字体文件


Window.size = (330, 570) # 窗口大小


class UserInput(TextInput): # 定义写入输入框的类型
    pat = '[A-Za-z0-9]+'

    def __init__(self, **kwargs):
        super(UserInput, self).__init__(**kwargs)

    # 输入过滤，只能输入数字或字母，每次输入一个字符都调用该方法
    def insert_text(self, s , from_undo=False):
        # print(s)
        pat=self.pat
        # 若不是数字或字母返回none
        match = re.search(self.pat, s)
        if match is None:
            s = '' # 写入空字符
        # print(s)
        # print(type(s))
        return super(UserInput, self).insert_text(s, from_undo=from_undo)

# 登陆界面
class RegisterLoginWindow(App):
    def build(self):
        self.mysql_result = user_data()
        self.user_id = user_data()[0::2]

        def update_rect(layout, *args):
            # 设置背景尺寸,可忽略
            layout.rect.pos = layout.pos
            layout.rect.size = layout.size

        self.layout = FloatLayout()  # 设置布局为浮动布局

        # 设置背景颜色和插入背景插图
        with self.layout.canvas:
            Color(89 / 255, 195 / 255, 226 / 255, 1)
            self.layout.rect = Rectangle(pos=self.layout.pos, size=self.layout.size)
            self.layout.bind(pos=update_rect, size=update_rect)
        image = AsyncImage(source='head.png', size_hint = [0.55,0.55], pos_hint ={"x": 0.225, "top": 1})
        self.layout.add_widget(image)  # 把图片加到布局里面

        self.layout.add_widget(Label(text = "用户名",
                                     font_name='Font_Hanzi',
                                     color = [0,0,0,1],
                                     size_hint = (0.06, 0.06),
                                     pos_hint = {"x": 0.15, "top": 0.5}))
        self.layout.add_widget(Label(text = "密码",
                                     font_name='Font_Hanzi',
                                     color = [0,0,0,1],
                                     size_hint = (0.06, 0.06),
                                     pos_hint = {"x": 0.15, "top": 0.38}))

        self.username = UserInput(multiline = False,
                                  size_hint=(0.6, 0.06),
                                  pos_hint = {"x":0.3, "top":0.5})
        self.layout.add_widget(self.username)
        self.password = UserInput(multiline = False,
                                  size_hint=(0.6, 0.06),
                                  pos_hint={"x": 0.3, "top": 0.38})
        self.layout.add_widget(self.password)


        # 创建登陆注册按钮并对应事件处理函数
        self.login_button = Button(text = "登录",
                                   font_name='Font_Hanzi',
                                   size_hint_max=("100dp", "40dp"),
                                   pos_hint={"x":0.16, "top":0.25},
                                   color=(0, 0, 0, 1),
                                   background_color=(136 / 255, 194 / 255, 247 / 255, 0.3)
                                   )

        self.layout.add_widget(self.login_button)
        self.login_button.bind(on_press=self.show_login_popup) # 登陆按钮绑定相关登陆提示的popup窗口

        self.register_button = Button(text = "注册",
                                   font_name='Font_Hanzi',
                                   size_hint_max=("100dp", "40dp"),
                                   pos_hint={"x":0.56, "top":0.25},
                                   color=(0, 0, 0, 1),
                                   background_color=(136 / 255, 194 / 255, 247 / 255, 0.3)
                                   )
        self.layout.add_widget(self.register_button)
        self.register_button.bind(on_press=self.show_register_window) # 注册按钮绑定相关登陆提示的popup窗口
        return self.layout


    # 登陆按钮不同情况触发的弹窗
    def show_login_popup(self, button):
        layout = FloatLayout() # 设置布局为浮动布局

        if (self.username.text.strip() != '' or self.username.text is not None) and (
                self.password.text.strip() != '' or self.password.text is not None):
            # 对其进行查找
            if self.username.text in self.user_id:
                # 若该用户名已存在
                if self.password.text == self.mysql_result[self.mysql_result.index(self.username.text) + 1]:
                    # 若密码正确，显示登陆成功，并清空输入框
                    layout.add_widget(Label(text="恭喜您登陆成功！",
                                            font_name='Font_Hanzi',
                                            size_hint=(0.045, 0.05),
                                            pos_hint={"x": 0.5, "top": 0.5}))
                    self.username.text = ''
                    self.password.text = ''
                    RegisterLoginWindow.stop(self)
                    Window.size = (1200, 900)
                    ExeMainWindow().run()



                else:
                    # 若密码错误，显示密码错误，并清空密码输入框
                    # print("密码输入错误,请重新输入！")
                    layout.add_widget(Label(text="密码输入错误，请重新输入！",
                                            font_name='Font_Hanzi',
                                            size_hint=(0.045, 0.05),
                                            pos_hint={"x": 0.5, "top": 0.5}))
                    self.password.text = ''
        #
            else:
                # 若用户名不存在，则显示用户名不存在，并清空输入框
                layout.add_widget(Label(text="该用户名不存在, 请重新输入或注册新账号！",
                                        font_name='Font_Hanzi',
                                        size_hint=(0.045, 0.05),
                                        pos_hint={"x": 0.5, "top": 0.5}))
                self.username.text = ''
                self.password.text = ''
                # print("不存在此用户名, 请您重新输入或注册一个新账号！")

        # 为登陆提示窗口增加一个关闭按钮
        closeButton = Button(text="×",
                             font_size = 21,
                             background_color=[1, 0, 0, 1],
                             size_hint = (0.05,0.05),
                             pos_hint = {"x": 0.95, "top": 1})
        layout.add_widget(closeButton)
        # 设置弹窗的属性
        popup = Popup(title="Login",
                      content=layout,
                      size_hint=(None, None),
                      size=(300, 240))
        popup.open()
        closeButton.bind(on_press=popup.dismiss) # 关闭按钮绑定关闭popup窗口的功能

    def show_register_window(self, button):
        def update_rect(layout, *args):
            # 设置背景尺寸,可忽略
            layout.rect.pos = layout.pos
            layout.rect.size = layout.size

        layout = FloatLayout()  # 设置布局为浮动布局
        # 设置背景颜色
        with layout.canvas:
            Color(89 / 255, 195 / 255, 226 / 255, 1)
            layout.rect = Rectangle(pos=layout.pos, size=layout.size)
            layout.bind(pos=update_rect, size=update_rect)
        # 注册用户名输入框
        self.register_username = UserInput(multiline=False,
                                           size_hint=(0.5, 0.08),
                                            pos_hint={"x": 0.4, "top": 0.9})
        layout.add_widget(self.register_username)

        self.register_password = UserInput(multiline=False,
                                           size_hint=(0.5, 0.08),
                                           pos_hint={"x": 0.4, "top": 0.7})
        layout.add_widget(self.register_password)
        # 再次确认账号输入框
        self.confirm_password = UserInput(multiline=False,
                                          size_hint=(0.5, 0.08),
                                            pos_hint={"x": 0.4, "top": 0.5})

        layout.add_widget(self.confirm_password)
        self.confirm_button = Button(text = "点击注册",
                                   font_name='Font_Hanzi',
                                   size_hint=(0.4, 0.08),
                                   pos_hint={"x":0.3, "top": 0.35},
                                   color=(0, 0, 0, 1),
                                   background_color=(136 / 255, 194 / 255, 247 / 255, 0.3)
                                   )
        layout.add_widget(self.confirm_button)
        self.confirm_button.bind(on_press=self.show_register_popup) # 确定注册按钮设计并绑定弹出注册提示窗口


        closeButton = Button(text="×",
                             font_size=21,
                             background_color=[1, 0, 0, 1],
                             size_hint=(0.05, 0.05),
                             pos_hint={"x": 0.95, "top": 1})
        layout.add_widget(closeButton)  # 给注册界面增添一个关闭按钮
        # 同上，通过popup设计注册窗口
        popup = Popup(title="Register",
                      content=layout,
                      size_hint=(None, None),
                      size=(330, 500))
        popup.open()
        closeButton.bind(on_press=popup.dismiss) # 关闭按钮绑定关闭注册窗口功能

        layout.add_widget(Label(text="创建用户名",
                                font_name='Font_Hanzi',
                                size_hint=(0.045, 0.05),
                                pos_hint={"x": 0.2, "top": 0.9}))
        layout.add_widget(Label(text="设置密码",
                                font_name='Font_Hanzi',
                                size_hint=(0.045, 0.05),
                                pos_hint={"x": 0.2, "top": 0.7}))
        layout.add_widget(Label(text="确认密码",
                                font_name='Font_Hanzi',
                                size_hint=(0.045, 0.05),
                                pos_hint={"x": 0.2, "top": 0.5}))
        layout.add_widget(Label(text="用户名、密码为大写、小写字母或数字",
                                font_name='Font_Hanzi',
                                size_hint=(1, 0.05),
                                pos_hint={"x": 0.01, "top": 0.2}))


    def show_register_popup(self, button):
        layout = FloatLayout() # 设置注册提示窗口布局
        if (self.register_username.text.strip() != '' or self.register_username is not None) and (
                self.register_password.text.strip() != '' or self.register_password.text is not None) and (
                self.confirm_password.text.strip() != '' or self.confirm_password.text is not None):
            # 对其进行查找
            if self.register_username.text in self.user_id:
                # 若用户名已存在于数据库中
                layout.add_widget(Label(text="该用户名已存在, 请重新注册！",
                                        font_name='Font_Hanzi',
                                        size_hint=(0.045, 0.05),
                                        pos_hint={"x": 0.5, "top": 0.5}))
                self.register_username.text = ''
                self.register_password.text = ''
                self.confirm_password.text = ''

        #
            else:
                if self.register_password.text != self.confirm_password.text:
                    # 注册时两次输入密码不同，弹出错误提示窗口
                    layout.add_widget(Label(text="两次输入密码不一致，请重新输入密码",
                                            font_name='Font_Hanzi',
                                            size_hint=(0.045, 0.05),
                                            pos_hint={"x": 0.5, "top": 0.5}))
                    self.register_password.text = ''
                    self.confirm_password.text = ''
                else:
                    # 成功注册时，则将用户信息写入云数据库,并更新此时的用户数据读取,并弹出注册成功窗口
                    insert_mysql(self.register_username.text, self.register_password.text) # 写入云数据库
                    self.mysql_result = user_data()  # 更新用户数据
                    self.user_id = user_data()[0::2]
                    layout.add_widget(Label(text="恭喜您注册成功！",
                                            font_name='Font_Hanzi',
                                            size_hint=(0.045, 0.05),
                                            pos_hint={"x": 0.5, "top": 0.5}))
                    self.register_username.text = ''
                    self.register_password.text = ''
                    self.confirm_password.text = ''


        closeButton = Button(text="×",
                             font_size=21,
                             background_color=[1, 0, 0, 1],
                             size_hint=(0.05, 0.05),
                             pos_hint={"x": 0.95, "top": 1})
        layout.add_widget(closeButton)
        popup = Popup(title="Register",
                      content=layout,
                      size_hint=(None, None),
                      size=(300, 200))
        popup.open()
        closeButton.bind(on_press=popup.dismiss)


if __name__ == '__main__':
    RegisterLoginWindow().run()
