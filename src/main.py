import pyrebase
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from firebase_admin import firestore
import firebase_admin
from firebase_admin import credentials
from kivymd.uix.button import MDRoundFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel

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
            return True
        except:
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
        try:
            auth.create_user_with_email_and_password(email, password)
            user = auth.sign_in_with_email_and_password(email, password)
            token = user['localId']
            userdb.collection('users').document(token).set({'email': email, 'password': password, 'bio':'','picture':''})
            return True
        except:
            self.ids.invalid_email_label.text = "Email already exists or invalid email. Try again"
            return False
    def clear(self):
        self.ids.user.text = ""
        self.ids.password.text = ""

class P(Popup):
    # text = ""
    # day = ""
    def addExercise(self):
        if self.ids.reps.text != "" and self.ids.sets.text != "":
            userdb.collection('users').document(auth.current_user['localId']).collection('workouts').document(self.day).set({
                "name": self.day,
                "yourExercises": {
                    self.text.replace(" ","_"): {
                    'reps' :self.ids.reps.text ,
                    'sets': self.ids.sets.text}}}, merge = True)
class namePopup(Popup):
    day = ""
    def getDay(self):
        return self.day
class MainWindow(Screen):
    def show_popup(self,txt, day):
        pops = P()
        pops.text = txt
        pops.day = day
        pops.open()
    def show_name_popup(self,day):
        pops = namePopup()
        pops.day = day
        pops.open()
    layout = []
    day = "Monday"
    def userId(self):
        print(auth.current_user['localId'])
    def setDay(self, day):
        self.day = day
    def getDay(self):
        return self.day
    def displayWorkout(self):
        word = userdb.collection("users").document(auth.current_user['localId']).collection('workouts').document(self.day).get()
        try:
            txt = word.get("yourExercises")
            for i in txt:
                reps = txt[i]["reps"]
                sets = txt[i]["sets"]
                card = MDCard(size_hint_y=None, height=100, padding=15)
                ex = i.replace("_"," ")+":"+reps+"X"+sets
                label = MDLabel(text=ex)
                image = Image(source = "icons\Weight.png")
                button = Button(text="trash", size_hint_y = None,size_hint_x=None, width = 50, height=50,on_release=lambda x:self.deleteWorkout(x.parent,x.parent.children[2].text.partition(':')[0]))
                card.add_widget(label)
                card.add_widget(image)
                card.add_widget(button)
                self.ids.widget_list.add_widget(card)
                self.layout.append(card)
        except:
            pass
        add_button = Button(text="add", size_hint_y=None, height=100,on_release=lambda x: self.switchScreen("search", "left"))
        fav_button = Button(text="add to favorites", size_hint_y=None, height=100,on_release=lambda x:self.show_name_popup(self.day))
        self.ids.widget_list.add_widget(add_button)
        self.layout.append(add_button)
        if len(self.ids.widget_list.children) > 1:
            self.ids.widget_list.add_widget(fav_button)
            self.layout.append(fav_button)
    def displayFavoriteList(self):
        print("diplayFavoriteList")
        word = userdb.collection("users").document(auth.current_user['localId']).collection('favorites').get()
        self.delButton()
        label = MDLabel(text="FAVORITE WORKOUTS")
        self.ids.favorite_list.add_widget(label)
        self.layout.append(label)
        for w in word:
            button = Button(text=w.id, size_hint_y=None, height=100, on_press =lambda x: self.displayFavoriteWorkout(x.text))
            self.ids.favorite_list.add_widget(button)
            self.layout.append(button)
    def displayFavoriteWorkout(self,x):
        print("displayFavoriteWorkout")
        txt = userdb.collection("users").document(auth.current_user['localId']).collection('favorites').document(x).get()
        txt = txt.to_dict()
        self.delButton()
        back_button = MDRoundFlatButton(text = "back",on_release=lambda x:self.displayFavoriteList())
        self.ids.favorite_list.add_widget(back_button)
        self.layout.append(back_button)
        for i in txt:
            reps = txt[i]["reps"]
            sets = txt[i]["sets"]
            card = MDCard(size_hint_y=None, height=100, padding=15)
            ex = i.replace("_", " ") + ":" + reps + "X" + sets
            label = MDLabel(text=ex)
            image = Image(source="icons\Weight.png")
            card.add_widget(label)
            card.add_widget(image)
            self.ids.favorite_list.add_widget(card)
            self.layout.append(card)
    def deleteWorkout(self,workout,text):
        self.ids.widget_list.remove_widget(workout)
        userdb.collection("users").document(auth.current_user['localId']).collection('workouts').document(self.day).update({"yourExercises.%s"%text.replace(" ","_"):firestore.DELETE_FIELD})
        pass
    def addFavorite(self,name,day):
        workout = userdb.collection("users").document(auth.current_user['localId']).collection('workouts').document(day).get()
        workout = workout.get("yourExercises")
        for i in workout:
            userdb.collection('users').document(auth.current_user['localId']).collection('favorites').document(name).set({
                    i: {
                        'reps': workout[i]["reps"],
                        'sets': workout[i]["sets"]}}, merge=True)
    def switchScreen(self,screen,dir):
        self.ids.manager.current = screen
        self.ids.manager.transition.direction=dir
    def addButton(self):
        searchText = list(self.ids.search.text.lower().replace(" ","_"))
        if(self.ids.search.text[0] == "#"):
                word = userdb.collection("exercises").where("tags", "array_contains", "".join(searchText)).get()
        else:
            word = userdb.collection("exercises").where("name", "==", "".join(searchText)).get()
        for words in word:
            txt = str(words.get('name').replace("_", " "))
            button = Button(text = txt, size_hint_y = None, height = 100,on_press=lambda x:self.show_popup(x.text,self.day))
            self.ids.search_list.add_widget(button)
            self.layout.append(button)
    def delButton(self):
        for i in self.layout:
            self.ids.widget_list.remove_widget(i)
            self.ids.search_list.remove_widget(i)
            self.ids.favorite_list.remove_widget(i)
class WindowManager(ScreenManager):
    pass
class KivyApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        return Builder.load_file('kivyfiles/new_window.kv')
if __name__ == '__main__':
    KivyApp().run()