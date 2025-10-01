import re
from flask import Blueprint, request, jsonify
from utils.rss_reader import fetch_rss_items
from dateutil import parser

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

from datetime import datetime

@news_bp.route('/select', methods=['GET'])
def select_item():
    try:
        index = int(request.args.get('index'))
        if index < 1 or index > 10:
            return jsonify({'error': 'Index must be between 1 and 10'}), 400
    except (TypeError, ValueError):
        return jsonify({'error': 'Index must be an integer'}), 400

    try:
        all_items = []
        for source, url in FEEDS.items():
            items = fetch_rss_items(url, 10)  # Fixed at 10 items per source
            for item in items:
                item['source'] = source
                all_items.append(item)

        # Optional: sort by published date if available
        all_items.sort(key=lambda x: x.get('published', ''), reverse=True)
        if index > len(all_items):
            return jsonify({'error': 'Index out of range'}), 400

        selected = all_items[index - 1]
        raw_date = selected.get('published', '')

        # Parse and format datetime
        try:
           dt = parser.parse(raw_date)
           formatted_date = dt.strftime("%d/%m %H:%M")
        except Exception:
           formatted_date = raw_date[:16] # fallback if parsing fails

        title = selected.get('title', '')
        summary = selected.get('summary', '')
        combined = f"{formatted_date} - {title} - {summary}"
        safe_text = re.sub(r'[^\x20-\x7E]', '', combined)  # keep only printable ASCII        
        trimmed = safe_text.replace('"', '')[:244] # remove double quotes & only 244 sharacters

        return jsonify({'item': trimmed})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
