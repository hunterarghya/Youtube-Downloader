import re
import io
import zipfile
from pytubefix import YouTube, Playlist

class YTD:

    @staticmethod
    def clean_title(title: str) -> str:
        return re.sub(r'[\\/*?:"<>|]', "", title).replace(" ", "_")

    @staticmethod
    def list_captions(url: str):
        yt = YouTube(url)
        return [c.code for c in yt.captions]

    @staticmethod
    def stream_video(url: str):
        yt = YouTube(url)
        stream = yt.streams.filter(file_extension="mp4").get_lowest_resolution()
        buffer = io.BytesIO()
        stream.stream_to_buffer(buffer)
        buffer.seek(0)
        filename = YTD.clean_title(yt.title) + ".mp4"
        return buffer, filename

    @staticmethod
    def stream_mp3(url: str):
        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()
        buffer = io.BytesIO()
        stream.stream_to_buffer(buffer)
        buffer.seek(0)
        filename = YTD.clean_title(yt.title) + ".mp3"
        return buffer, filename

    @staticmethod
    def download_captions(url: str, langs):
        yt = YouTube(url)
        results = []
        for lang in langs:
            cap = yt.captions.get_by_language_code(lang)
            if cap:
                try:
                    text = cap.generate_srt_captions()
                    name = YTD.clean_title(yt.title) + f".{lang}.srt"
                    results.append((name, text))
                except:
                    continue
        return results

    @staticmethod
    def download_playlist_videos(url: str):
        p = Playlist(url)
        results = []
        for link in p.video_urls:
            buffer, filename = YTD.stream_video(link)
            results.append((buffer, filename))
        return results

    @staticmethod
    def download_playlist_mp3(url: str):
        p = Playlist(url)
        results = []
        for link in p.video_urls:
            buffer, filename = YTD.stream_mp3(link)
            results.append((buffer, filename))
        return results

    @staticmethod
    def download_playlist_captions(url: str, langs):
        p = Playlist(url)
        results = []
        for link in p.video_urls:
            buffer, filename = YTD.stream_video(link)
            caps = YTD.download_captions(link, langs)
            results.append((buffer, filename, caps))
        return results
