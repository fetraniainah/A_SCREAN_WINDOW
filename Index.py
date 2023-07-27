import kivy
import os
from kivy.app import App
from kivy.config import Config
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
import threading
import pyautogui
import cv2
import numpy as np
from datetime import datetime

class CustomApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_recording = False
        self.record_thread = None
        self.start_button = None
        self.stop_button = None
        self.time_label = None
        self.start_time = None
        self.icon="icon.png"
        self.title="Fetra Software"
       

    def build(self):
        # Configuration de la taille de la fenêtre et l'empêchement de redimensionnement
        Config.set('graphics', 'width', '300')
        Config.set('graphics', 'height', '150')
        Config.set('graphics', 'resizable', '0')

        # Créer le layout principal pour la fenêtre avec une orientation verticale
        main_layout = BoxLayout(orientation='vertical')

        # Créer le label principal
        label = Label(text='TONGASOA !', size_hint=(1, None), height=50,font_name='Roboto-Bold.ttf')

        # Créer le label pour afficher le temps d'enregistrement
        self.time_label = Label(text='FOTOANA : 00:00', size_hint=(1, None), height=50,font_name='Roboto-Bold.ttf')

        # Créer le layout pour les boutons avec une orientation horizontale
        button_layout = BoxLayout(orientation='horizontal')

        # Créer les boutons avec une hauteur de 50 pixels
        self.start_button = Button(text='ATOMBOKA', size_hint=(0.5, None), height=50, background_color=(0, 1, 0, 1), font_name='Roboto-Bold.ttf')
        self.stop_button = Button(text='FARANANA', size_hint=(0.5, None), height=50, background_color=(1, 0, 0, 1), font_name='Roboto-Bold.ttf')

        # Connecter les boutons aux fonctions
        self.start_button.bind(on_release=self.start_recording)
        self.stop_button.bind(on_release=self.stop_recording)

        # Ajouter les boutons et les labels au layout correspondant
        button_layout.add_widget(self.start_button)
        button_layout.add_widget(self.stop_button)

        main_layout.add_widget(label)
        main_layout.add_widget(self.time_label)
        main_layout.add_widget(button_layout)

        return main_layout

    def on_request_close(self, *args):
        if self.is_recording:
            # Empêcher la fermeture de l'application pendant l'enregistrement
            popup = Popup(title='FOTOANA', content=Label(text='NIJANONA TEO AMINY'), size_hint=(None, None), size=(300, 150))
            popup.open()
            return True
        else:
            return False

    def start_recording(self, instance):
        if not self.is_recording:
            self.is_recording = True
            instance.disabled = True
            self.stop_button.disabled = False  # Activer le bouton Stop
            self.start_time = datetime.now()
            self.record_thread = threading.Thread(target=self.record_screen)
            self.record_thread.start()
            

    def stop_recording(self, instance):
        if self.is_recording:
            self.is_recording = False

    def record_screen(self):
        screen_width, screen_height = pyautogui.size()
        videos_folder_path = os.path.join(os.environ['USERPROFILE'], 'Desktop/Capture')
        if not os.path.exists(videos_folder_path):
            os.makedirs(videos_folder_path)
        desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop/Capture')
        codec = cv2.VideoWriter_fourcc(*"mp4v")  # Utiliser le codec H264 pour MP4
        output_filename = os.path.join(desktop_path, f"Fetra_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4")
        out = cv2.VideoWriter(output_filename, codec, 20.0, (screen_width, screen_height))

        while self.is_recording:
            img = pyautogui.screenshot()
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            out.write(frame)

            # Mettre à jour le label de temps d'enregistrement en temps réel
            elapsed_time = datetime.now() - self.start_time
            elapsed_time_str = str(elapsed_time).split(".")[0]  # Formater l'heure en "HH:MM:SS"
            self.time_label.text = f'FOTOANA LASA : {elapsed_time_str}'

        out.release()
        print("Recording stopped. Video saved as", output_filename)
        self.start_button.disabled = False  # Activer le bouton Start
        self.stop_button.disabled = True   # Désactiver le bouton Stop

if __name__ == '__main__':
    CustomApp().run()
