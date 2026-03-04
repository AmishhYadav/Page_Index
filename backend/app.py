from flask import Flask, request, jsonify
from flask_cors import CORS
from scraper import scrape_page
from indexer import Indexer
from search import SearchEngine
import validators
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

indexer = Indexer()
search_engine = SearchEngine(indexer)

@app.route("/api/index", methods=["POST"])
def index_page():
    try:
        data = request.get_json(silent=True)
        if not data or "url" not in data:
            return jsonify({"error": "Missing 'url' field in request body"}), 400

        url = data["url"].strip()
        if not url:
            return jsonify({"error": "URL cannot be empty"}), 400

        # Validate URL format
        if not validators.url(url):
            # Try prepending https://
            if validators.url("https://" + url):
                url = "https://" + url
            else:
                return jsonify({"error": f"Invalid URL format: {url}"}), 400

        # Check if already indexed
        if indexer.is_indexed(url):
            return jsonify({"message": f"URL already indexed: {url}", "status": "exists"}), 200

        # Scrape the page
        page_data = scrape_page(url)
        if not page_data:
            return jsonify({"error": f"Failed to scrape URL: {url}. Site may be unreachable or blocking requests."}), 422

        if not page_data.get("content") and not page_data.get("title"):
            return jsonify({"error": f"No meaningful content found at: {url}"}), 422

        # Index the page
        indexer.add_document(page_data)
        logger.info(f"Successfully indexed: {url}")

        return jsonify({
            "message": "Page indexed successfully",
            "title": page_data.get("title", "Untitled"),
            "url": url,
            "word_count": len(page_data.get("content", "").split())
        }), 201

    except Exception as e:
        logger.error(f"Error indexing page: {str(e)}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


@app.route("/api/search", methods=["GET"])
def search():
    try:
        query = request.args.get("q", "").strip()
        if not query:
            return jsonify({"error": "Search query cannot be empty", "results": []}), 400

        if len(query) > 500:
            return jsonify({"error": "Query too long (max 500 characters)", "results": []}), 400

        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)

        # Clamp per_page
        per_page = max(1, min(per_page, 50))
        page = max(1, page)

        results = search_engine.search(query)

        # Paginate
        start = (page - 1) * per_page
        end = start + per_page
        paginated = results[start:end]

        return jsonify({
            "query": query,
            "total_results": len(results),
            "page": page,
            "per_page": per_page,
            "results": paginated
        }), 200

    except Exception as e:
        logger.error(f"Error searching: {str(e)}")
        return jsonify({"error": f"Search failed: {str(e)}", "results": []}), 500


@app.route("/api/stats", methods=["GET"])
def stats():
    try:
        return jsonify({
            "total_documents": indexer.get_document_count(),
            "total_terms": indexer.get_term_count()
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/documents", methods=["GET"])
def list_documents():
    try:
        docs = indexer.get_all_documents()
        return jsonify({"documents": docs, "total": len(docs)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/index/<path:url>", methods=["DELETE"])
def delete_document(url):
    try:
        if indexer.remove_document(url):
            return jsonify({"message": f"Removed: {url}"}), 200
        else:
            return jsonify({"error": f"URL not found: {url}"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
