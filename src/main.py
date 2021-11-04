import urllib
from time import sleep

import pyrebase
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
Window.size = (550,800)
class ScrollableLabel(ScrollView):
  text = StringProperty('')
class MyGridLayout(Widget):
  pass

class LoginWindow(Screen):
  def login(self):
    auth = firebase.auth()
    email=self.ids.user.text
    password=self.ids.password.text
    try:
     auth.sign_in_with_email_and_password(email, password)
     print("Successfully signed in!")
     return True
    except:
     print("invalid user or password. Try again")
     self.ids.invalid_label.text = "invalid user or password. Try again"
     return False
  def clear(self):
    self.ids.user.text = ""
    self.ids.password.text = ""
class SignUpWindow(Screen):
  def create_account(self):
    auth = firebase.auth()
    email=self.ids.user.text
    password=self.ids.password.text
    print(self.ids.user.text, self.ids.password.text)
    try:
      auth.create_user_with_email_and_password(email,password)
      print("Success!")
      return True
    except:
      print("Email already exists or invalid email")
      self.ids.invalid_email_label.text = "Email already exists or invalid email. Try again"
      return False

  def clear(self):
    self.ids.user.text = ""
    self.ids.password.text = ""
class MainWindow(Screen):
  pass

class WindowManager(ScreenManager):
  pass

firebaseConfig={'apiKey': "AIzaSyBXuwuHpegF_nDPc1JsrMG1f8EaEit7-XI",
  'authDomain': "pyrebase-6e06e.firebaseapp.com",
  'databaseURL':"https://pyrebase-6e06e-default-rtdb.firebaseio.com/",
  'projectId': "pyrebase-6e06e",
  'storageBucket': "pyrebase-6e06e.appspot.com",
  'messagingSenderId': "156655911418",
  'appId': "1:156655911418:web:e95408e1e82fd4389c2443",
  'measurementId': "G-RJ9JQWP5LK"}

firebase = pyrebase.initialize_app(firebaseConfig)

class KivyApp(MDApp):
  def build(self):
    self.theme_cls.theme_style = "Dark"
    self.theme_cls.primary_palette = "BlueGray"
    return Builder.load_file('new_window.kv')


if __name__ == '__main__':
    KivyApp().run()





db=firebase.database()

# storage=firebase.storage()

# login
# email=input("Enter your email ")
# password=input("Enter your password ")
# try:
#   auth.sign_in_with_email_and_password(email, password)
#   print("Successfully signed in!")
# except:
#   print("invalid user or password. Try again")
#
# # Signup
# confirmpass=input("Confirm password")
# if password==confirmpass:
#   try:
#     auth.create_user_with_email_and_password(email,password)
#     print("Success!")
#   except:
#     print("Email already exists")

# Storage
# upload
# filename=input("Enter the name of the file you want to upload")
# cloudfilename=input("Enter the name of the file on the cloud")
# storage.child(cloudfilename).put(filename)
#
# print(storage.child(cloudfilename).get_url(None))
# download
# cloudfilename=input("Enter the name of the file you want to download")
# storage.child(cloudfilename).download("","downloaded.txt")

# reading file
# cloudfilename=input("Enter the name fo the file you want to read")
# url=storage.child(cloudfilename).get_url(None)
# f=urllib.request.urlopen(url).read()
# print(f)

# Database
# data={'age': 40, 'address': "New York", 'employed' : True, 'name':"John Smith"}
# db.child("people").child("ostrandi").set(data)
# db.child("people").push(data)

# #Update
# db.child("people").child("ostrandi").update({'name': "Jane"})

# people=db.child("people").get()
# for person in people.each():
#   if person.val()['name'] == "JohnSmith":
#     db.child("people").child(person.key()).update({'name':'Deez'})

# Delete
# db.child("people").child("person").remove()

# Read
people=db.child("people").order_by_child("age").start_at("3").get()
print(people.val())

# people=db.child("people").order_by_child("name").start_at("John").get()
# for person in people.each():
#   print(person.val()["address"])