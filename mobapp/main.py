import os
import threading
import zipfile
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.filechooser import FileChooserIconView
from kivy.core.window import Window
from utils import YTD

Window.clearcolor = (0.067, 0.067, 0.067, 1)  # dark background

class DownloaderApp(App):

    def build(self):
        self.root = BoxLayout(orientation="vertical", padding=10, spacing=10)

        self.status = Label(text="Status messages will appear here...", size_hint_y=None, height=30, color=(0.6,1,0.6,1))
        self.url_input = TextInput(hint_text="Paste YouTube URL here", multiline=False, size_hint_y=None, height=40, background_color=(0,0,0,1), foreground_color=(0.23,1,0.23,1))
        
        self.root.add_widget(self.url_input)
        self.root.add_widget(self.status)

        # Buttons
        btn_layout = BoxLayout(size_hint_y=None, height=40, spacing=5)
        btn_layout.add_widget(Button(text="Download Video", on_press=self.download_video))
        btn_layout.add_widget(Button(text="Download MP3", on_press=self.download_mp3))
        self.root.add_widget(btn_layout)

        btn_layout2 = BoxLayout(size_hint_y=None, height=40, spacing=5)
        btn_layout2.add_widget(Button(text="Download Playlist Videos", on_press=self.download_playlist_videos))
        btn_layout2.add_widget(Button(text="Download Playlist MP3", on_press=self.download_playlist_mp3))
        self.root.add_widget(btn_layout2)

        # Captions
        self.caption_box = GridLayout(cols=1, size_hint_y=None)
        self.caption_scroll = ScrollView(size_hint=(1, 0.3))
        self.caption_scroll.add_widget(self.caption_box)
        self.root.add_widget(self.caption_scroll)
        self.load_captions_btn = Button(text="Load Captions", size_hint_y=None, height=40, on_press=self.load_captions)
        self.root.add_widget(self.load_captions_btn)

        self.download_captions_btn = Button(text="Download Video with Selected Captions", size_hint_y=None, height=40, on_press=self.download_video_with_captions)
        self.root.add_widget(self.download_captions_btn)

        # File chooser
        self.fc = FileChooserIconView(path=os.getcwd())
        self.root.add_widget(self.fc)

        return self.root

    def set_status(self, text):
        self.status.text = text

    def run_threaded(self, func, *args):
        threading.Thread(target=func, args=args, daemon=True).start()

    def load_captions(self, instance=None):
        url = self.url_input.text.strip()
        if not url:
            self.set_status("Enter URL")
            return
        self.set_status("Fetching captions...")
        self.caption_box.clear_widgets()
        try:
            codes = YTD.list_captions(url)
            for code in codes:
                box = BoxLayout(size_hint_y=None, height=30)
                chk = CheckBox()
                chk.value = code
                box.add_widget(chk)
                box.add_widget(Label(text=code))
                self.caption_box.add_widget(box)
            self.set_status(f"{len(codes)} captions loaded")
        except Exception as e:
            self.set_status(f"Error: {e}")

    def get_selected_captions(self):
        langs = []
        for child in self.caption_box.children:
            chk = child.children[1]
            if chk.active:
                langs.append(chk.value)
        return langs

    # Download functions
    def download_video(self, instance=None):
        self.run_threaded(self._download_video)

    def _download_video(self):
        url = self.url_input.text.strip()
        folder = self.fc.path
        self.set_status("Downloading video...")
        try:
            buffer, filename = YTD.stream_video(url)
            filepath = os.path.join(folder, filename)
            with open(filepath, "wb") as f:
                f.write(buffer.read())
            self.set_status(f"Video saved: {filepath}")
        except Exception as e:
            self.set_status(f"Error: {e}")

    def download_mp3(self, instance=None):
        self.run_threaded(self._download_mp3)

    def _download_mp3(self):
        url = self.url_input.text.strip()
        folder = self.fc.path
        self.set_status("Downloading MP3...")
        try:
            buffer, filename = YTD.stream_mp3(url)
            filepath = os.path.join(folder, filename)
            with open(filepath, "wb") as f:
                f.write(buffer.read())
            self.set_status(f"MP3 saved: {filepath}")
        except Exception as e:
            self.set_status(f"Error: {e}")

    def download_video_with_captions(self, instance=None):
        self.run_threaded(self._download_video_with_captions)

    def _download_video_with_captions(self):
        url = self.url_input.text.strip()
        folder = self.fc.path
        langs = self.get_selected_captions()
        self.set_status("Downloading video + captions...")
        try:
            buffer, vid_name = YTD.stream_video(url)
            cap_files = YTD.download_captions(url, langs)
            zip_path = os.path.join(folder, "video_with_captions.zip")
            with zipfile.ZipFile(zip_path, "w") as z:
                z.writestr(vid_name, buffer.read())
                for name, text in cap_files:
                    z.writestr(name, text)
            self.set_status(f"Video + captions saved: {zip_path}")
        except Exception as e:
            self.set_status(f"Error: {e}")

    def download_playlist_videos(self, instance=None):
        self.run_threaded(self._download_playlist_videos)

    def _download_playlist_videos(self):
        url = self.url_input.text.strip()
        folder = self.fc.path
        self.set_status("Downloading playlist videos...")
        try:
            videos = YTD.download_playlist_videos(url)
            zip_path = os.path.join(folder, "playlist_videos.zip")
            with zipfile.ZipFile(zip_path, "w") as z:
                for buffer, vid_name in videos:
                    z.writestr(vid_name, buffer.read())
            self.set_status(f"Playlist videos saved: {zip_path}")
        except Exception as e:
            self.set_status(f"Error: {e}")

    def download_playlist_mp3(self, instance=None):
        self.run_threaded(self._download_playlist_mp3)

    def _download_playlist_mp3(self):
        url = self.url_input.text.strip()
        folder = self.fc.path
        self.set_status("Downloading playlist MP3s...")
        try:
            audios = YTD.download_playlist_mp3(url)
            zip_path = os.path.join(folder, "playlist_mp3.zip")
            with zipfile.ZipFile(zip_path, "w") as z:
                for buffer, aud_name in audios:
                    z.writestr(aud_name, buffer.read())
            self.set_status(f"Playlist MP3s saved: {zip_path}")
        except Exception as e:
            self.set_status(f"Error: {e}")

if __name__ == "__main__":
    DownloaderApp().run()
