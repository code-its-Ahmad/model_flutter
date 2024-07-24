from flask import Flask, request, jsonify
from flask_cors import CORS
from model_train import extract_produce_info

app = Flask(__name__)
CORS(app)  

@app.route('/extract_produce', methods=['GET'])
def extract_produce():
    try:
        sentence = request.args.get('sentence', '')
        if not sentence:
            return jsonify({"error": "No sentence provided"}), 400

        result = extract_produce_info(sentence)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": f"Failed to process request: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
