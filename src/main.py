import pyrebase
from kivy.lang import Builder
from kivy.uix.button import Button
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from firebase_admin import firestore
import firebase_admin
from firebase_admin import credentials
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
class SearchScreen(Screen):
    pass
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
            userdb.collection('users').document(token).collection('workouts').document("Monday").set({"name": "Monday",'yourExercises':{}}, merge = True)
            userdb.collection('users').document(token).collection('workouts').document("Tuesday").set({"name": "Tuesday",'yourExercises':{}}, merge = True)
            userdb.collection('users').document(token).collection('workouts').document("Wednesday").set({"name": "Wednesday",'yourExercises':{}}, merge = True)
            userdb.collection('users').document(token).collection('workouts').document("Thursday").set({"name": "Thursday",'yourExercises':{}}, merge = True)
            userdb.collection('users').document(token).collection('workouts').document("Friday").set({"name": "Friday",'yourExercises':{}}, merge = True)
            userdb.collection('users').document(token).collection('workouts').document("Saturday").set({"name": "Saturday",'yourExercises':{}}, merge = True)
            userdb.collection('users').document(token).collection('workouts').document("Sunday").set({"name": "Sunday",'yourExercises':{}}, merge = True)
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
    layouts2 = []
    day = "Monday"
    def userId(self):
        print(auth.current_user['localId'])
    def setDay(self, day):
        self.day = day
    def addExercise(self,instance):
        userdb.collection('users').document(auth.current_user['localId']).collection('workouts').document(self.day).set({
            "yourExercises": {
                instance.text: {
                'reps' : "",
                'sets': ""}}}, merge = True)
    def displayWorkout(self):
        print("THIS IS WORKING")
        word = userdb.collection("users").document(auth.current_user['localId']).collection('workouts').where("name" ,"==" ,self.day).get()
        print(word)
        for words in word:
            txt = words.get("yourExercises")
            for txts in txt:
                button = Button(text=txts, size_hint_y=None, height=100)
                self.ids.widget_list.add_widget(button)
                self.layouts.append(button)
        add_button = Button(text = "add",size_hint_y=None, height=100)
        self.ids.widget_list.add_widget(add_button)
        self.layouts.append(add_button)
    def addButton(self):
        searchText = self.ids.search.text.lower()
        if(self.ids.search.text[0] == "#"):
                word = userdb.collection("exercises").where("tags", "array_contains", searchText).get()
        else:
            word = userdb.collection("exercises").where("name", "==", searchText).get()
        for words in word:
            txt = str(words.get('name'))
            button = Button(text = txt, size_hint_y = None, height = 100,on_press=self.addExercise)
            self.ids.search_list.add_widget(button)
            self.layouts2.append(button)
    def delButton(self):
        for i in self.layouts:
            self.ids.widget_list.remove_widget(i)
        for i in self.layouts2:
            self.ids.search_list.remove_widget(i)
class WindowManager(ScreenManager):
    pass
class KivyApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        return Builder.load_file('new_window.kv')


if __name__ == '__main__':
    KivyApp().run()