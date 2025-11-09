# YouTube Downloader

A lightweight and simple tool to download YouTube content. Supports single videos, playlists, audio-only extraction, and subtitle download in SRT format. Also includes a mobile application for better performance.

---

## Features

- Download single video
- Download entire playlist
- Convert video to MP3 audio
- Download playlist as MP3
- Download subtitles in SRT format (if available)
- Minimal interface
- Mobile application

## ⚙️ Tech Stack

- **FastAPI** — Modern asynchronous Python web framework
- **Python** — Core backend language
- **pytubefix** — For YouTube video processing
- **Uvicorn** — ASGI web server
- **Docker** — Containerization and deployment
- **Kivy** — Building mobile application

---

## 🚀 Setup & Run

### 1️⃣ Clone the Repository

```bash
git clone <repo-url>
cd Youtube-Downloader
```

### 2️⃣ Create a Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # For Linux/Mac
.venv\Scripts\activate     # For Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the Server

```bash
uvicorn app.main:app --reload
```

Then open your browser at:  
👉 **http://127.0.0.1:8000/**

---

---

## 🐳 Run with Docker

### Build and run directly:

```bash
docker build -t ytvd .
docker run -d -p 8000:8000 ytvd
```

---

## 🚀 Run the app

### Go to the mobapp folder and run the app

```bash
cd mobapp
python main.py
```

---

## 👤 Author

**Arghya Malakar**  
📧 arghyaapply2016@gmail.com  
💻 [GitHub](https://github.com/hunterarghya)
