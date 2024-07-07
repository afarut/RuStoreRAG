import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from flask import Flask, request, jsonify
from huggingface_hub.hf_api import HfFolder
from .model import get_answer

device = "cuda"

HfFolder.save_token("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")
app = Flask(__name__)

print(device)

@app.route('/', methods=['GET'])
def gate():
    return jsonify({"result": "OK"})


@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    print(data)
    prompt = data.get('prompt', '')
    print(prompt)

    #inputs = tokenizer(prompt, return_tensors='pt').to(device)

    #print(inputs)

    #with torch.no_grad():
    #    outputs = model.generate(**inputs, max_new_tokens=50)
    #print("(((((")

    generated_text = get_answer(prompt)

    return jsonify({'answer: ': generated_text})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)

