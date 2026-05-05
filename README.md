# SummeRise — AI Article Summarizer

A Python web app that scrapes **any article URL**, summarizes it using **Groq AI (Llama 3.3)**, and stores the result in a local **SQLite** database.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Flask](https://img.shields.io/badge/Flask-Web%20App-lightgrey)
![Groq](https://img.shields.io/badge/Groq-Llama%203.3-orange)
![License](https://img.shields.io/badge/License-MIT-green)

---

## Features

- 🔗 Scrape **any article URL** and get an instant AI summary
- 🤖 Powered by **Groq AI (Llama 3.3 70B)** — free and fast
- 🗄️ Stores articles and summaries in a local **SQLite** database
- 🚫 Duplicate detection — won't re-summarize articles already stored
- 🗑️ Clear all articles with one click
- 🌍 Tested sites: BBC News, Reuters, Dev.to, Wikipedia, TechCrunch, The Verge, Ars Technica, Medium

---

## Project Structure

```
SummeRise/
├── app.py              # Flask web app — routes and entry point
├── groq_client.py      # Groq AI summarization
├── database.py         # SQLite storage and retrieval
├── templates/
│   ├── base.html       # Base layout and global styles
│   ├── index.html      # Home page — scrape and view articles
│   └── detail.html     # Article detail page
├── requirements.txt
├── .env.example        # Example environment file
├── .gitignore
└── .env                # Your API key — DO NOT commit this
```

---

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/your-username/SummeRise.git
cd SummeRise
```

### 2. Create a virtual environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create your `.env` file
```
API_KEY=gsk_your_groq_key_here
```
Get a **free** Groq API key at: https://console.groq.com

### 5. Run the app
```bash
python app.py
```

Open your browser at: **http://127.0.0.1:5000**

---

## Usage

1. Paste any article URL into the **Scrape Any URL** box
2. Click **Scrape URL**
3. The summary is generated and stored instantly
4. Click any article card to view the full summary alongside the original content

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python + Flask |
| AI Summarization | Groq API (Llama 3.3 70B) |
| URL Scraping | newspaper3k |
| Database | SQLite |
| Frontend | HTML + CSS + Vanilla JS |

---

## License
MIT
