# from kivy.app import App
# from kivy.uix.pagelayout import PageLayout
# from kivy.uix.label import Label
# from kivy.uix.button import Button
#
#
# class PageLayoutApp(App):
# 	def build(self):
# 		# 创建 PageLayout 实例并添加两个页面
# 		layout = PageLayout()
# 		layout.add_widget(Label(text='a'))
# 		layout.add_widget(Label(text='b'))
# 		layout.add_widget(Label(text='c'))
# 		layout.add_widget(Label(text='d'))
# 		return layout
#
#
# if __name__ == '__main__':
# 	PageLayoutApp().run()

#[{"0.0": [[1, 0, 6, 7, 0, 0, 0, 0.3490658503988659, 0, 0, false, 1115.0, ["1", "\u51cf\u5c0f\u4e24\u80a9\u7684\u9ad8\u4f4e\u8ddd\u79bb"]], [2, 6, 0, 0, 0, 0, 0, 1.0471975511965976, 0, 0, true, 1115.0, ["\u51cf\u5c0f\u5de6\u5c0f\u817f\u7684\u6700\u5927\u89d2\u5ea6", "", "\u589e\u5927\u5de6\u5c0f\u817f\u7684\u6700\u5927\u89d2\u5ea6", ""]], [2, 8, 0, 0, 0, 0, 0, 1.0471975511965976, 0, 0, true, 1115.0, ["\u51cf\u5c0f\u53f3\u5c0f\u817f\u7684\u6700\u5927\u89d2\u5ea6", "", "\u589e\u5927\u53f3\u5c0f\u817f\u7684\u6700\u5927\u89d2\u5ea6", ""]]], "5.0": [[2, 5, 0, 0, 0, 0, 0, 1.5707963267948966, 0, 1.0471975511965976, true, 2110.0, ["\u51cf\u5c0f\u5de6\u5927\u817f\u7684\u6700\u5927\u89d2\u5ea6", "1", "\u589e\u5927\u5de6\u5927\u817f\u7684\u6700\u5927\u89d2\u5ea6", "2"]], [2, 7, 0, 0, 0, 0, 0, 1.0471975511965976, 0, 0, true, 2110.0, ["\u51cf\u5c0f\u53f3\u5927\u817f\u7684\u6700\u5927\u89d2\u5ea6", "", "\u589e\u5927\u53f3\u5927\u817f\u7684\u6700\u5927\u89d2\u5ea6", ""]]]}, "video1.mp4", 10.0]
from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label


class ScrollableLabel(ScrollView):
    def __init__(self, **kwargs):
        super(ScrollableLabel, self).__init__(**kwargs)

        layout = FloatLayout(size_hint_y=None)

        self.add_widget(layout)

        for i in range(50):
            label = Label(text=str(i), size_hint_y=None, height=40)
            label.pos_hint = {'y': 1 - i * 0.02}
            layout.add_widget(label)


class TestApp(App):

    def build(self):
        return ScrollableLabel()


if __name__ == '__main__':
    TestApp().run()
from MySql.connect_mysql import VIDEO_data2
# 该文件用来打开训练的标准视频

video_play_data = VIDEO_data2()
print(VIDEO_data2())
video_id = VIDEO_data2()[0::3]
video_name = VIDEO_data2()[1::3]
print(video_id)
print(video_name)

# import json
# #a= [{"0.0": [[1, 0, 6, 7, 0, 0, 0, 0.3490658503988659, 0, 0, false, 1115.0, ["1", "\u51cf\u5c0f\u4e24\u80a9\u7684\u9ad8\u4f4e\u8ddd\u79bb"]], [2, 6, 0, 0, 0, 0, 0, 1.0471975511965976, 0, 0, true, 1115.0, ["\u51cf\u5c0f\u5de6\u5c0f\u817f\u7684\u6700\u5927\u89d2\u5ea6", "", "\u589e\u5927\u5de6\u5c0f\u817f\u7684\u6700\u5927\u89d2\u5ea6", ""]], [2, 8, 0, 0, 0, 0, 0, 1.0471975511965976, 0, 0, true, 1115.0, ["\u51cf\u5c0f\u53f3\u5c0f\u817f\u7684\u6700\u5927\u89d2\u5ea6", "", "\u589e\u5927\u53f3\u5c0f\u817f\u7684\u6700\u5927\u89d2\u5ea6", ""]]], "5.0": [[2, 5, 0, 0, 0, 0, 0, 1.5707963267948966, 0, 1.0471975511965976, true, 2110.0, ["\u51cf\u5c0f\u5de6\u5927\u817f\u7684\u6700\u5927\u89d2\u5ea6", "1", "\u589e\u5927\u5de6\u5927\u817f\u7684\u6700\u5927\u89d2\u5ea6", "2"]], [2, 7, 0, 0, 0, 0, 0, 1.0471975511965976, 0, 0, true, 2110.0, ["\u51cf\u5c0f\u53f3\u5927\u817f\u7684\u6700\u5927\u89d2\u5ea6", "", "\u589e\u5927\u53f3\u5927\u817f\u7684\u6700\u5927\u89d2\u5ea6", ""]]]}, "video1.mp4", 10.0]
# with open("dict.json", 'r+') as f:
# 	res_list = json.load(f)
# print(res_list)
# # video_name = res_list[1]
# # end_time = res_list[2]
#
a = "[1,2]"
print(list(a))