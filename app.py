import os
import logging
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, redirect, url_for
from database import (
    create_articles_table, store_article,
    get_all_summaries_data, get_article_by_id,
    article_exists, clear_all_articles, delete_article_by_id,
)
from groq_client import summarize_text

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

load_dotenv()
if not os.getenv("API_KEY"):
    raise EnvironmentError(
        "\n[ERROR] API_KEY is missing!\n"
        "Create a .env file in the project root with:\n"
        "  API_KEY=gsk_your_groq_key_here\n"
        "Get a free key at: https://console.groq.com\n"
    )

app = Flask(__name__)


@app.route("/")
def index():
    """Home page — shows all stored articles."""
    articles = get_all_summaries_data()
    return render_template("index.html", articles=articles)


@app.route("/article/<int:article_id>")
def article_detail(article_id):
    """Detail page for a single article."""
    article = get_article_by_id(article_id)
    if not article:
        return redirect(url_for("index"))
    return render_template("detail.html", article=article)


@app.route("/scrape-url", methods=["POST"])
def scrape_url():
    """Scrape a custom URL with newspaper3k and summarise it with Groq."""
    from newspaper import Article as NewspaperArticle

    url = request.form.get("url", "").strip()
    if not url or not url.startswith("http"):
        return jsonify({"error": "Please enter a valid URL starting with http/https"}), 400

    if article_exists(url):
        return jsonify({"success": True, "stored": 0, "skipped": 1,
                        "message": "Article already exists"})

    try:
        na = NewspaperArticle(url)
        na.download()
        na.parse()

        title   = na.title or "Untitled"
        author  = ", ".join(na.authors) if na.authors else "Unknown"
        content = na.text

        if not content or len(content.strip()) < 100:
            return jsonify({"error": (
                "Could not extract enough content from this URL. "
                "The site may be behind a paywall or require JavaScript."
            )}), 400

        summary = summarize_text(content[:3000])

        stored = store_article({
            "title":      title,
            "author":     author,
            "content":    content,
            "summary":    summary,
            "source_url": url,
        })

        if stored:
            return jsonify({"success": True, "stored": 1, "skipped": 0, "title": title})
        return jsonify({"success": True, "stored": 0, "skipped": 1})

    except Exception as e:
        logger.error(f"Scrape error: {e}")
        return jsonify({"error": f"Failed to scrape: {str(e)}"}), 500


@app.route("/delete/<int:article_id>", methods=["POST"])
def delete_article(article_id):
    """Delete a single article by ID."""
    try:
        deleted = delete_article_by_id(article_id)
        if deleted:
            return jsonify({"success": True})
        return jsonify({"error": "Article not found"}), 404
    except Exception as e:
        logger.error(f"Delete error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/clear", methods=["POST"])
def clear():
    """Delete all stored articles."""
    try:
        deleted = clear_all_articles()
        return jsonify({"success": True, "deleted": deleted})
    except Exception as e:
        logger.error(f"Clear error: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    create_articles_table()
    app.run(debug=True, port=5000)
