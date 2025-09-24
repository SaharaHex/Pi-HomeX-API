from flask import Blueprint, request, jsonify
from utils.rss_reader import fetch_rss_items

tech_bp = Blueprint('tech', __name__)

TECH_FEEDS = {
    'techradar': "https://www.techradar.com/uk/feeds/articletype/news",
    'techrepublic': "https://www.techrepublic.com/rssfeeds/articles/",
    'wired': "https://www.wired.com/feed/tag/ai/latest/rss"
}

@tech_bp.route('/<source>', methods=['GET'])
def get_tech_news(source):
    if source not in TECH_FEEDS:
        return jsonify({'error': 'Invalid tech source'}), 400

    try:
        limit = int(request.args.get('limit', 10))
    except ValueError:
        return jsonify({'error': 'Limit must be an integer'}), 400

    items = fetch_rss_items(TECH_FEEDS[source], limit)
    for item in items:
        item['source'] = source
        item['rss_source'] = TECH_FEEDS[source]

    return jsonify(items)

@tech_bp.route('/all', methods=['GET'])
def get_all_tech_news():
    try:
        limit = int(request.args.get('limit', 10))
    except ValueError:
        return jsonify({'error': 'Limit must be an integer'}), 400

    all_items = []
    for source, url in TECH_FEEDS.items():
        items = fetch_rss_items(url, limit)
        for item in items:
            item['source'] = source
            item['rss_source'] = url
            all_items.append(item)

    all_items.sort(key=lambda x: x.get('published', ''), reverse=True)
    return jsonify(all_items[:limit])
