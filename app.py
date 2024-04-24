import requests
import json
import gradio as gr

url = "http://localhost:11434/api/generate"

headers = {
    'Content-Type': 'application/json'
}

conversation_history = []

def generate_response(prompt):
    conversation_history.append("You: " + prompt)

    full_prompt = "\n".join(conversation_history)

    data = {
        "model": "llama2",
        "stream": False,
        "prompt": full_prompt
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_txt = response.text
        data = json.loads(response_txt)
        actual_response = data["response"]
        conversation_history.append("AI: " + actual_response)
        return "\n".join(conversation_history)
    else:
        error_message = "Error: " + str(response.status_code) + " " + response.text
        conversation_history.append("AI: " + error_message)
        return "\n".join(conversation_history)

iface = gr.Interface(
    fn=generate_response,
    inputs=["text"],
    outputs=["text"]
)

if __name__ == "__main__":
    iface.launch()
