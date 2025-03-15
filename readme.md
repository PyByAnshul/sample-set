# 📦 Module Structure: `smlib` (SampleSet Library)

## 🗂 Folder Overview

The `smlib` module consists of three main folders:

### 1️⃣ Instagram
Scripts related to Instagram data scraping:
- **`comments_section_scrapper.py`**: Scrapes comments from Instagram posts.
- **`post_scrapper.py`**: Scrapes post details like captions, media, and metadata.

### 2️⃣ Twitter
Scripts for Twitter automation:
- **`post_twit.py`**: Posts content directly to Twitter.

### 3️⃣ Ollama
Scripts for AI-generated content:
- **`caption_creater.py`**: Uses the Gemini model to generate a summary based on Instagram captions.

---

## 🌐 Flask Web Application (`app.py`)

This module includes a Flask-based web app that acts as a control center:

- **📋 Data Table:** Displays all Instagram post records.
- **📥 Fetch Posts Button:** Scrapes Instagram posts and saves them into a MongoDB database.
- **📝 Summarize & Tweet Button:** Generates a caption summary and tweets it instantly.

---

## 🛠 Tech Stack
- **Backend:** Python, Flask
- **Database:** MongoDB
- **Scraping:** Custom-built scrapers for Instagram
- **AI Integration:** Gemini for caption summarization
- **Social Media API:** Twitter API

---

## 🚀 How to Run
1. Clone the repository.
2. Ensure Docker is running and start services using:
    ```bash
    docker-compose up --build
    ```
3. Access the web app at `http://localhost:5000`.
4. Open Mongo Express at `http://localhost:8081` to view stored data.

---

## 📝 Future Enhancements
- Add user authentication and session management.
- Implement better error handling and logging.
- Improve UI with pagination and search features.
- Enhance AI capabilities with more models.

---
