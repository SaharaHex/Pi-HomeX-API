from flask import Blueprint, jsonify

help_bp = Blueprint('help', __name__)

@help_bp.route('/help', methods=['GET'])
def all_help():
    news_endpoints = {
        "/api/skynews": {
            "description": "Fetch latest Sky News world headlines",
            "parameters": { "limit": "Optional. Number of items to return (default: 10)" },
            "example": "/api/skynews?limit=5",
            "rss_source": "https://feeds.skynews.com/feeds/rss/world.xml"
        },
        "/api/aljazeera": {
            "description": "Fetch latest Al Jazeera headlines",
            "parameters": { "limit": "Optional. Number of items to return (default: 10)" },
            "example": "/api/aljazeera",
            "rss_source": "https://www.aljazeera.com/xml/rss/all.xml"
        },
        "/api/france24": {
            "description": "Fetch latest France24 headlines",
            "parameters": { "limit": "Optional. Number of items to return (default: 10)" },
            "example": "/api/france24?limit=3",
            "rss_source": "https://www.france24.com/en/rss"
        },
        "/api/all": {
            "description": "Merge all feeds into one response",
            "parameters": { "limit": "Optional. Total number of items to return across all feeds (default: 10)" },
            "example": "/api/all?limit=20"
        },
        "/api/select": {
            "description": "Return a single news item with formatted datetime and summary, optimized for MMBasic",
            "parameters": { "index": "Required. Integer between 1 and 10 to select the item position" },
            "example": "/api/select?index=3"
        }
    }

    tech_endpoints = {
        "/api/tech/techradar": {
            "description": "Fetch latest TechRadar news articles",
            "parameters": { "limit": "Optional. Number of items to return (default: 10)" },
            "example": "/api/tech/techradar?limit=5",
            "rss_source": "https://www.techradar.com/uk/feeds/articletype/news"
        },
        "/api/tech/techrepublic": {
            "description": "Fetch latest TechRepublic articles",
            "parameters": { "limit": "Optional. Number of items to return (default: 10)" },
            "example": "/api/tech/techrepublic",
            "rss_source": "https://www.techrepublic.com/rssfeeds/articles/"
        },
        "/api/tech/wired": {
            "description": "Fetch latest Wired AI articles",
            "parameters": { "limit": "Optional. Number of items to return (default: 10)" },
            "example": "/api/tech/wired",
            "rss_source": "https://www.wired.com/feed/tag/ai/latest/rss"
        },
        "/api/tech/all": {
            "description": "Merge all tech feeds into one response",
            "parameters": { "limit": "Optional. Total number of items to return across all feeds (default: 10)" },
            "example": "/api/tech/all?limit=7"
        },
        "/api/tech/select": {
            "description": "Return a single tech news item with formatted datetime and summary, optimized for MMBasic",
            "parameters": { "index": "Required. Integer between 1 and 10 to select the item position" },
            "example": "/api/tech/select?index=2"
        }
    }

    return jsonify({
        "message": "Welcome to Pi-HomeX-API. These are all available endpoints and their parameters:",
        "news": news_endpoints,
        "tech": tech_endpoints,
        "meta": {
            "/": { "description": "Root status check", "example": "/" },
            "/api/help": { "description": "Help route with examples and parameters", "example": "/api/help" }
        }
    })

