from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import func  # 假设你已经写好了这个模块

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    url = data.get('url')

    if not url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        description = func.work(url)  # 调用你的Python函数
        return jsonify({'description': description})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)