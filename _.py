import re
# kivy 引用
import MySQLdb
import kivy
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
import pymysql