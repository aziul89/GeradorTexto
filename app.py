import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
import torch

# hugging face token
hf_token = os.getenv('HF_TOKEN')

from huggingface_hub import login
from huggingface_hub import InferenceClient
login(token=hf_token)

model_id = "meta-llama/Llama-3.2-1B"
client = InferenceClient(token=hf_token)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://escreveai.vercel.app"}})

@app.route('/generate', methods=['POST'])
def generate_text():
    data = request.json
    prompt = data.get('prompt', '')
    max_length = data.get('max_length', 100)

    try:      
        response = client.text_generation(
            model=model_id,
            prompt=prompt
        )
        print("Response from Inference API:", response)  # Para debugar
        return jsonify({"generated_text": response})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
