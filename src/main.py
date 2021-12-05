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
cred = credentials.Certificate("serviceAccountKey.json")
firebase = pyrebase.initialize_app(firebaseConfig)
firebase_admin.initialize_app(cred)
userdb = firestore.client()
Window.size = (550, 800)
auth = firebase.auth()
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
        bio = self.ids.bio.text
        try:
            auth.create_user_with_email_and_password(email, password)
            user = auth.sign_in_with_email_and_password(email, password)
            token = user['localId']
            userdb.collection('users').document(token).set({'email': email, 'password': password, 'bio': bio,'picture':''})
            return True
        except:
            self.ids.invalid_email_label.text = "Email already exists or invalid email. Try again"
            return False
    def clear(self):
        self.ids.user.text = ""
        self.ids.password.text = ""
        self.ids.bio.text = ""
class ProfileWindow(Screen):
    def displayEmail(self):
        return ""
    def displayBio(self):
        return ""
    def sendReset(self):
        auth.send_password_reset_email((userdb.collection('users').document(auth.current_user['localId']).get().to_dict()["email"]))
        self.ids.passwordreset.text = "Password Reset Email Has Been Sent!"
    def clearText(self):
        self.ids.passwordreset.text = ""

class SettingsWindow(Screen):
    pass
class P(Popup):
    def addExercise(self):
        if self.ids.reps.text != "" and self.ids.sets.text != "":
            userdb.collection('users').document(auth.current_user['localId']).collection('workouts').document(self.day).set({
                    self.text.replace(" ","_"): {
                    'reps' :self.ids.reps.text ,
                    'sets': self.ids.sets.text}}, merge = True)
class namePopup(Popup):
    day = ""
    location = ""
    def getDay(self):
        return self.day
    def getLocation(self):
        print(self.location)
        return self.location
class MainWindow(Screen):
    def show_dictionaries(self,type):
        if(type == "favorite"):
            return userdb.collection("users").document(auth.current_user['localId']).collection('favorites')
        if (type == "explore"):
            return userdb.collection('explore')
        if (type == "workout"):
            return userdb.collection("users").document(auth.current_user['localId']).collection('workouts')
    def show_popup(self,txt, day):
        pops = P()
        pops.text = txt
        pops.day = day
        pops.open()
    def show_name_popup(self,day,location):
        pops = namePopup()
        pops.day = day
        pops.location = location
        pops.open()
    layout = []
    day = "Monday"
    def userId(self):
        print(auth.current_user['localId'])
    def setDay(self, day):
        self.day = day
    def getDay(self):
        return self.day
    def displayList(self,location):
        word = self.show_dictionaries(location).get()
        self.delButton()
        for w in word:
            button = Button(text=w.id, size_hint_y=None, height=100, on_press =lambda x: self.displayWorkout(location,x.text))
            self.ids.widget_list.add_widget(button)
            self.layout.append(button)
    def displayWorkout(self,location,text):
        txt = self.show_dictionaries(location).document(text).get()
        txt = txt.to_dict()
        self.delButton()
        if(location == "explore" or location == "favorite"):
            back_button = MDRoundFlatButton(text="back", on_release=lambda x: self.displayList(location))
            self.ids.widget_list.add_widget(back_button)
            self.layout.append(back_button)
        if(txt != None):
            for i in txt:
                reps = txt[i]["reps"]
                sets = txt[i]["sets"]
                card = MDCard(size_hint_y=None, height=100, padding=15)
                ex = i.replace("_", " ") + ":" + reps + "X" + sets
                label = MDLabel(text=ex)
                image = Image(source="icons\Weight.png")
                card.add_widget(label)
                card.add_widget(image)
                if(location == "workout"):
                    button = Button(text="trash", size_hint_y = None,size_hint_x=None, width = 50, height=50,on_release=lambda x:self.deleteExercise(x.parent,x.parent.children[2].text.partition(':')[0]))
                    card.add_widget(button)
                self.ids.widget_list.add_widget(card)
                self.layout.append(card)
        if(location == "workout"):
            add_button = Button(text="add", size_hint_y=None, height=100, on_release=lambda x: self.switchScreen("search", "left"))
            fav_button = Button(text="add to favorites", size_hint_y=None, height=100, on_release=lambda x: self.show_name_popup(self.day,"favorite"))
            upload_button = Button(text="upload", size_hint_y=None, height=100, on_release=lambda x: self.show_name_popup(self.day,"explore"))
            self.ids.widget_list.add_widget(add_button)
            self.layout.append(add_button)
            if len(self.ids.widget_list.children) > 1:
                self.ids.widget_list.add_widget(fav_button)
                self.layout.append(fav_button)
                self.ids.widget_list.add_widget(upload_button)
                self.layout.append(upload_button)
        if(location == "explore"):
            fav_button = Button(text="add to favorites", size_hint_y=None, height=100, on_release=lambda x: self.addFavorite(text,"favorite",text,"explore"))
            if len(self.ids.widget_list.children) > 1:
                self.ids.widget_list.add_widget(fav_button)
                self.layout.append(fav_button)
        if(location == "favorite"):
            trash_button = Button(text = "trash",size_hint_y= None, height=100, on_release= lambda x:self.deleteWorkout(text))
            self.ids.widget_list.add_widget(trash_button)
            self.layout.append(trash_button)
    def deleteWorkout(self,workout):
        print(self.show_dictionaries("favorite").document(workout).delete())
        self.delButton()
        self.displayWorkout("favorite",workout)
    def deleteExercise(self,workout,text):
        self.ids.widget_list.remove_widget(workout)
        userdb.collection("users").document(auth.current_user['localId']).collection('workouts').document(self.day).update({text.replace(" ","_"):firestore.DELETE_FIELD})
    def addFavorite(self,name,location,workout,dictionary):
        try:
            workout = self.show_dictionaries(dictionary).document(workout).get()
            workout = workout.to_dict()
            for i in workout:
                self.show_dictionaries(location).document(name).set({
                        i: {
                            'reps': workout[i]["reps"],
                            'sets': workout[i]["sets"]}}, merge=True)
        except:
            pass
    def switchScreen(self,screen,dir):
        self.ids.manager.current = screen
        self.ids.manager.transition.direction=dir
    def addSearchedButton(self):
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
class WindowManager(ScreenManager):
    pass
class KivyApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        return Builder.load_file('kivyfiles/new_window.kv')
if __name__ == '__main__':
    KivyApp().run()
