from flask import Blueprint, request, jsonify
from utils.rss_reader import fetch_rss_items

news_bp = Blueprint('news', __name__)

FEEDS = {
    'skynews': "https://feeds.skynews.com/feeds/rss/world.xml",
    'aljazeera': "https://www.aljazeera.com/xml/rss/all.xml",
    'france24': "https://www.france24.com/en/rss"
}

@news_bp.route('/<source>', methods=['GET'])
def get_news(source):
    if source not in FEEDS:
        return jsonify({'error': 'Invalid source'}), 400

    try:
        limit = int(request.args.get('limit', 10))
    except ValueError:
        return jsonify({'error': 'Limit must be an integer'}), 400

    items = fetch_rss_items(FEEDS[source], limit)
    return jsonify(items)

@news_bp.route('/all', methods=['GET'])
def get_all_news():
    try:
        limit = int(request.args.get('limit', 10))
    except ValueError:
        return jsonify({'error': 'Limit must be an integer'}), 400

    all_items = []
    for source, url in FEEDS.items():
        items = fetch_rss_items(url, limit)
        for item in items:
            item['source'] = source  # Add source label
            all_items.append(item)

    # Optional: sort by published date if available
    all_items.sort(key=lambda x: x.get('published', ''), reverse=True)

    return jsonify(all_items[:limit])
