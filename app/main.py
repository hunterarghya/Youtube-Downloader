from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

from pytubefix import Playlist
from app.utils import YTD

import io
import zipfile

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")


app.add_middleware( 
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"]
# )

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/captions")
def captions(url: str):
    return {"captions": YTD.list_captions(url)}


@app.get("/playlist-captions")
def playlist_captions(url: str):
    p = Playlist(url)
    langs = set()
    for link in p.video_urls:
        langs.update(YTD.list_captions(link))
    return {"captions": sorted(list(langs))}


@app.get("/download-video")
def download_video(url: str):
    buffer, filename = YTD.stream_video(url)
    return StreamingResponse(buffer, media_type="video/mp4",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'})


@app.get("/download-mp3")
def download_mp3(url: str):
    buffer, filename = YTD.stream_mp3(url)
    return StreamingResponse(buffer, media_type="audio/mpeg",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'})


@app.get("/download-video-captions")
def download_video_captions(url: str, langs: str):
    langs = langs.split(",")
    buffer, vid_name = YTD.stream_video(url)
    cap_files = YTD.download_captions(url, langs)

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as z:
        z.writestr(vid_name, buffer.read())
        for name, text in cap_files:
            z.writestr(name, text)

    zip_buffer.seek(0)
    return StreamingResponse(zip_buffer, media_type="application/zip",
        headers={"Content-Disposition": 'attachment; filename="video_with_captions.zip"'})


@app.get("/download-playlist")
def download_playlist(url: str):
    p = Playlist(url)
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w") as z:
        for link in p.video_urls:
            buffer, vid_name = YTD.stream_video(link)
            z.writestr(vid_name, buffer.read())

    zip_buffer.seek(0)
    return StreamingResponse(zip_buffer, media_type="application/zip",
        headers={"Content-Disposition": 'attachment; filename="playlist_videos.zip"'})


@app.get("/download-playlist-mp3")
def download_playlist_mp3(url: str):
    p = Playlist(url)
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w") as z:
        for link in p.video_urls:
            buffer, aud_name = YTD.stream_mp3(link)
            z.writestr(aud_name, buffer.read())

    zip_buffer.seek(0)
    return StreamingResponse(zip_buffer, media_type="application/zip",
        headers={"Content-Disposition": 'attachment; filename="playlist_mp3.zip"'})


@app.get("/download-playlist-captions")
def download_playlist_captions(url: str, langs: str):
    langs = langs.split(",")
    p = Playlist(url)

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as z:
        for link in p.video_urls:
            buffer, vid_name = YTD.stream_video(link)
            z.writestr(vid_name, buffer.read())

            for name, text in YTD.download_captions(link, langs):
                z.writestr(name, text)

    zip_buffer.seek(0)
    return StreamingResponse(zip_buffer, media_type="application/zip",
        headers={"Content-Disposition": 'attachment; filename="playlist_with_captions.zip"'} )

