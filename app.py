from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
import torch

app = Flask(__name__)
CORS(app)

model_id = "meta-llama/Llama-3.2-1B"
try:

    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        torch_dtype=torch.float32,
        device_map="cpu"
    )
    tokenizer = AutoTokenizer.from_pretrained(model_id)

    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer
    )
except Exception as e:
    pipe = None
    print(f"Erro ao carregar o modelo: {e}")


@app.route('/generate', methods=['POST'])
def generate_text():
    if not pipe:
        return jsonify({"error": "Modelo não carregado corretamente."}), 500

    data = request.json
    prompt = data.get('prompt', '')
    max_length = data.get('max_length', 100)

    try:
        result = pipe(prompt, max_length=max_length)
        return jsonify({"generated_text": result[0]["generated_text"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
