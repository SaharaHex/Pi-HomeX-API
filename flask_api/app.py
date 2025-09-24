from flask import Flask, jsonify
from datetime import datetime
from routes.news import news_bp
from routes.tech import tech_bp
from routes.help import help_bp

app = Flask(__name__)
app.register_blueprint(news_bp, url_prefix='/api')
app.register_blueprint(tech_bp, url_prefix='/api/tech')
app.register_blueprint(help_bp, url_prefix='/api')

@app.route('/', methods=['GET'])
def home():
    return jsonify({ 'result': 'Success from Pi-HomeX-API!', 'timestamp': datetime.utcnow().isoformat() }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)



