# from pytubefix import Playlist, YouTube
# import moviepy
# import os
# import re

# class ytd:

#     def get_info(url):
#         y=YouTube(url)
#         title= y.title()
        

    
#     def list_subtitles(url):
#         """
#         Prints all available subtitle language codes for the given YouTube video.
#         """
#         yt = YouTube(url)
#         print("\nAvailable subtitles:\n")
#         for caption in yt.captions:
#             print(f"{caption.code}")
#         print("\nUse these codes in download_subtitles().")


#     def download_subtitles(url, save_dir, languages):
#         """
#             Downloads subtitles as .srt for given languages.
            
#             Parameters:
#                 url (str): YouTube video link
#                 save_dir (str): directory where subtitle files will be saved
#                 languages (list): list of caption codes, example: ["en", "hi", "a.en"]
            
#             Returns:
#                 list of file paths of downloaded subtitle files
#             """
#         yt = YouTube(url)

#         if not os.path.exists(save_dir):
#             os.makedirs(save_dir)

#         # Clean title for filename
#         title = re.sub(r'[\\/*?:"<>|]', "", yt.title).replace(" ", "_")

#         downloaded_files = []

#         for lang in languages:
#             caption = yt.captions.get_by_language_code(lang)
#             if not caption:
#                 print(f"Subtitle not found for: {lang}")
#                 continue

#             srt_data = caption.generate_srt_captions()
#             file_path = os.path.join(save_dir, f"{title}.{lang}.srt")

#             with open(file_path, "w", encoding="utf-8") as f:
#                 f.write(srt_data)

#             print(f"Downloaded: {file_path}")
#             downloaded_files.append(file_path)

#         return downloaded_files


#     def one_video(url, save_path):
#         try:
#             y=YouTube(url)
#             stream= y.streams.filter(file_extension='mp4').get_lowest_resolution()
#             print("Title: ", y.title)

#             filename= re.sub(r'[\\/*?:"<>|]', "", y.title)+".mp4"

#             stream.download(output_path=save_path, filename= filename)
#             print("download completed")

#         except Exception as e:
#             print(f"An error occured: {e}")


#     def playlist(url, save_path):
#         try:
#             p= Playlist(url)
#             for video_url in p.video_urls:
#                 ytd.one_video(video_url, save_path)

#         except Exception as e:
#             print(f"An error occured: {e}")


#     def song(url, save_path):
#         try:
#             y=YouTube(url)
#             stream= y.streams.filter(only_audio=True).first()
#             if not stream:
#                 print("no audio found")
#                 return
#             print("Title: ", y.title)

#             filename= re.sub(r'[\\/*?:"<>|]', "", y.title)+".mp3"

#             stream.download(output_path=save_path, filename= filename)
#             print("download completed")

#         except Exception as e:
#             print(f"An error occured: {e}")


#     def songlist(url, save_path):
#         try:
#             p= Playlist(url)
#             for video_url in p.video_urls:
#                 ytd.song(video_url, save_path)

#         except Exception as e:
#             print(f"An error occured: {e}")







import re
import io
from pytubefix import YouTube


class YTD:

    @staticmethod
    def clean_title(title: str) -> str:
        # remove illegal filename characters and replace spaces with underscores
        return re.sub(r'[\\/*?:"<>|]', "", title).replace(" ", "_")

    @staticmethod
    def list_captions(url: str):
        
        yt = YouTube(url, client="WEB_EMBED")
        # yt.captions is an iterable of caption objects
        return [c.code for c in yt.captions]
    

    @staticmethod
    def stream_video(url: str):
        yt = YouTube(url, client="WEB_EMBED")
        # lowest_res is intentional per your original logic
        stream = yt.streams.filter(file_extension="mp4").get_lowest_resolution()

        buffer = io.BytesIO()
        stream.stream_to_buffer(buffer)
        buffer.seek(0)

        filename = YTD.clean_title(yt.title) + ".mp4"
        return buffer, filename

    @staticmethod
    def stream_mp3(url: str):
        yt = YouTube(url, client="WEB_EMBED")
        stream = yt.streams.filter(only_audio=True).first()

        buffer = io.BytesIO()
        stream.stream_to_buffer(buffer)
        buffer.seek(0)

        filename = YTD.clean_title(yt.title) + ".mp3"
        return buffer, filename

    @staticmethod
    def download_captions(url: str, langs):
        yt = YouTube(url, client="WEB_EMBED")
        results = []

        for lang in langs:
            cap = yt.captions.get_by_language_code(lang)
            if cap:
                try:
                    text = cap.generate_srt_captions()
                except:
                    continue  # skip broken caption formats

                name = YTD.clean_title(yt.title) + f".{lang}.srt"
                results.append((name, text))

        return results





# import re
# import io
# import subprocess
# import requests
# from yt_dlp import YoutubeDL


# class YTD:

#     @staticmethod
#     def clean_title(title: str) -> str:
#         return re.sub(r'[\\/*?:"<>|]', "", title).replace(" ", "_")

#     @staticmethod
#     def _get_info(url: str):
#         ydl_opts = {"quiet": True}
#         with YoutubeDL(ydl_opts) as ydl:
#             return ydl.extract_info(url, download=False)

#     @staticmethod
#     def list_captions(url: str):
#         info = YTD._get_info(url)
#         subs = info.get("subtitles", {})
#         return list(subs.keys())

#     @staticmethod
#     def stream_video(url: str):
#         info = YTD._get_info(url)

#         # Pick lowest resolution MP4
#         formats = [f for f in info["formats"] if f.get("ext") == "mp4" and f.get("height")]
#         fmt = sorted(formats, key=lambda x: x["height"])[0]
#         download_url = fmt["url"]

#         buffer = io.BytesIO()
#         r = requests.get(download_url, stream=True)
#         for chunk in r.iter_content(chunk_size=1024 * 256):
#             buffer.write(chunk)
#         buffer.seek(0)

#         filename = YTD.clean_title(info["title"]) + ".mp4"
#         return buffer, filename

#     @staticmethod
#     def stream_mp3(url: str):
#         info = YTD._get_info(url)

#         # Get best audio source
#         audio_fmt = info["formats"][-1]["url"]

#         # Stream → ffmpeg → MP3 buffer
#         process = subprocess.Popen(
#             ["ffmpeg", "-i", audio_fmt, "-vn", "-acodec", "libmp3lame", "-f", "mp3", "-"],
#             stdout=subprocess.PIPE,
#             stderr=subprocess.DEVNULL
#         )

#         buffer = io.BytesIO(process.stdout.read())
#         buffer.seek(0)

#         filename = YTD.clean_title(info["title"]) + ".mp3"
#         return buffer, filename

#     @staticmethod
#     def download_captions(url: str, langs):
#         info = YTD._get_info(url)
#         subs = info.get("subtitles", {})
#         results = []

#         for lang in langs:
#             if lang not in subs:
#                 continue

#             # Choose the first available caption source
#             cap_info = subs[lang][0]
#             cap_url = cap_info["url"]

#             # Convert to SRT through ffmpeg
#             process = subprocess.Popen(
#                 ["ffmpeg", "-i", cap_url, "-f", "srt", "-"],
#                 stdout=subprocess.PIPE,
#                 stderr=subprocess.DEVNULL
#             )

#             srt_text = process.stdout.read().decode("utf-8", errors="ignore")
#             if not srt_text.strip():
#                 continue

#             name = YTD.clean_title(info["title"]) + f".{lang}.srt"
#             results.append((name, srt_text))

#         return results
