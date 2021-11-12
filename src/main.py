import pyrebase
from kivy.core.image import Image
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from firebase_admin import firestore
import firebase_admin
from firebase_admin import credentials
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.card import MDCard

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
userdb = firestore.client()
Window.size = (550, 800)
firebaseConfig = {
    'apiKey': "AIzaSyCLaRtvwLMheJOJU2BrRtRAef_ogPn0yrQ",
    'authDomain': "smartstrength-ae966.firebaseapp.com",
    'databaseURL': "https://smartstrength-ae966-default-rtdb.firebaseio.com",
    'projectId': "smartstrength-ae966",
    'storageBucket': "smartstrength-ae966.appspot.com",
    'messagingSenderId': "910004572815",
    'appId': "1:910004572815:web:0d379a3035a6c5f2ddd6fa",
    'measurementId': "G-N3QTMB57PK"
}
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()


class LoginWindow(Screen):
    def login(self):
        email = self.ids.user.text
        password = self.ids.password.text
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
    def debug(self):
        auth.sign_in_with_email_and_password("ian@mail.com", "123456")
        return True

class SignUpWindow(Screen):
    def create_account(self):
        email = self.ids.user.text
        password = self.ids.password.text
        print(self.ids.user.text, self.ids.password.text)
        try:
            auth.create_user_with_email_and_password(email, password)
            user = auth.sign_in_with_email_and_password(email, password)
            token = user['localId']
            print(token)
            userdb.collection('users').document(token).set({'email': email, 'password': password, 'bio':'','picture':''})
            print("Success!" + auth.current_user['localId'])
            return True
        except:
            print("Email already exists or invalid email")
            self.ids.invalid_email_label.text = "Email already exists or invalid email. Try again"
            return False
    def clear(self):
        self.ids.user.text = ""
        self.ids.password.text = ""
class MainWindow(Screen):
    layouts = []
    def userId(self):
        print(auth.current_user['localId'])
    def addButton(self):
        if(self.ids.search.text[0] == "#"):
            word = userdb.collection("exercises").where("tags", "array_contains", self.ids.search.text).get()
        else:
            word = userdb.collection("exercises").where("name", "==", self.ids.search.text).get()
        for words in word:
            layout = Button(text = str(words.get('name')), size_hint_y = None, height = 100)
            self.ids.widget_list.add_widget(layout)
            self.layouts.append(layout)
    def delButton(self):
        for i in self.layouts:
            self.ids.widget_list.remove_widget(i)
    def addToWorkout(self):
        pass
class WindowManager(ScreenManager):
    pass
class KivyApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        return Builder.load_file('new_window.kv')


if __name__ == '__main__':
    KivyApp().run()

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
# people=db.child("people").order_by_child("age").start_at("3").get()
# print(people.val())

# people=db.child("people").order_by_child("name").start_at("John").get()
# for person in people.each():
#   print(person.val()["address"])
