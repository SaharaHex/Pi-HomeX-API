import re
from flask import Blueprint, request, jsonify
from utils.rss_reader import fetch_rss_items
from dateutil import parser

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

@tech_bp.route('/select', methods=['GET'])
def select_tech_item():
    try:
        index = int(request.args.get('index'))
        if index < 1 or index > 10:
            return jsonify({'error': 'Index must be between 1 and 10'}), 400
    except (TypeError, ValueError):
        return jsonify({'error': 'Index must be an integer'}), 400

    try:
        all_items = []
        for source, url in TECH_FEEDS.items():
            items = fetch_rss_items(url, 10)  # Fixed at 10 items per source
            for item in items:
                item['source'] = source
                all_items.append(item)

        all_items.sort(key=lambda x: x.get('published', ''), reverse=True)
        if index > len(all_items):
            return jsonify({'error': 'Index out of range'}), 400

        selected = all_items[index - 1]
        raw_date = selected.get('published', '')

        # Format datetime as DD/MM HH:MM
        try:
           dt = parser.parse(raw_date)
           formatted_date = dt.strftime("%d/%m %H:%M")
        except Exception:
           formatted_date = raw_date[:16] # fallback if parsing fails

        title = selected.get('title', '')
        summary = selected.get('summary', '')
        combined = f"{formatted_date} - {title} - {summary}"

        # Strip non-ASCII and double quotes, trim to 244 characters
        safe_text = re.sub(r'[^\x20-\x7E]', '', combined)
        trimmed = safe_text.replace('"', '')[:244]

        return jsonify({'item': trimmed})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
