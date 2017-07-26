# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.uix.dropdown import DropDown

from time import time

adverts = True
try: #'!!!! this line should be removed upon release !!!!'
  from jnius import autoclass
except ImportError: #'!!!! this line should be removed upon release !!!!'
  adverts = False #'!!!! this line should be removed upon release !!!!'

if adverts: #'!!!! this line should be removed upon release !!!!'
  PythonActivity = autoclass('org.kivy.android.PythonActivity')
  AdBuddiz = autoclass('com.purplebrain.adbuddiz.sdk.AdBuddiz')

class Countdown(Widget):
  caption = ObjectProperty(None)
  selector = ObjectProperty(None)
  

  time = time()
  time_emojimovie = 1501804800

  translations = {
    'UK': ' remaining until the emoji movie is officially released in ',
  }


  time_remaining = time_emojimovie - time
  time_str = StringProperty('%.2f' % time_remaining)
  unit = 0
  units = ['seconds','minutes','hours','days']
  

  def __init__(self, *args, **kwargs):
    super(Countdown,self).__init__(*args,**kwargs)
    Clock.schedule_interval(self.update,0)

  def update(self,t):
    self.time = time()
    self.time_remaining = self.time_emojimovie - self.time
    if -86400 < self.time_remaining < 0:
      self.time_str = 'The Emoji Movie comes out today!'
      self.caption.text = ''
    elif self.time_remaining < -86400:
      self.time_str = 'You missed the party...'
      self.caption.text = 'Come back for the sequel'
    else:
      if self.unit == 0:
        self.time_str = '%.2f' % self.time_remaining
      elif self.unit == 1:
        self.time_str = '%.2f' % (self.time_remaining/60)
      elif self.unit == 2:
        self.time_str = '%.2f' % (self.time_remaining/3600)
      else:
        self.time_str = '%.2f' % (self.time_remaining/86400)

    self.caption.text = self.units[self.unit]


  def change_units(self):
    print('change')
    self.unit += 1
    if self.unit >= 4:
      self.unit = 0


class EmojiApp(App):
  def build(self):
    if adverts:
      AdBuddiz.setPublisherKey('63e0dc24-70e2-4517-afb3-d1adb6d809a4')
      #AdBuddiz.setTestModeActive()
      AdBuddiz.cacheAds(PythonActivity.mActivity)
      AdBuddiz.showAd(PythonActivity.mActivity)

    self.main = Countdown()
    return self.main

emoji = EmojiApp()
emoji.run()
