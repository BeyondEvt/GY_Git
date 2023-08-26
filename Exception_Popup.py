from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.text import LabelBase

class Exception_Pupup(FloatLayout):
    def __init__(self, text=None, **kwargs):
        super(Exception_Pupup, self).__init__(**kwargs)
        self.text = text
        self.popup = Popup(title="Error",
                           content=self,
                           size_hint=(None, None),
                           size=(400, 240))
        self.popup.open()
        LabelBase.register(name='Font_Hanzi', fn_regular='kvcn.ttc')  # 导入字体文件
        self.add_widget(Label(text="%s" % self.text,
                              font_name='Font_Hanzi',
                              size_hint=(0.045, 0.05),
                              pos_hint={"x": 0.5, "top": 0.5}))
        self.add_widget((Button(text="×",
                                font_size=21,
                                background_color=[1, 0, 0, 1],
                                size_hint=(0.05, 0.05),
                                pos_hint={"x": 0.95, "top": 1},
                                on_press=self.popup.dismiss)))
