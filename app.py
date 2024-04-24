import requests
import json
import gradio as gr

url = "http://localhost:11434/api/generate"

headers = {
    'Content-Type': 'application/json'
}

conversation_history_4_gradle = []
conversation_history_4_llama = []

def generate_response(prompt):
    # Append user message
    conversation_history_4_gradle.append([prompt, None])  # User message with no bot response yet
    conversation_history_4_llama.append("prompt: " + prompt)

    full_prompt = "\n".join(conversation_history_4_llama) + "\nresponse: "
    print(full_prompt)

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
        conversation_history_4_gradle[-1][1] = actual_response  # Update the latest pair with the bot's response
        print(conversation_history_4_gradle)
        conversation_history_4_llama.append("response: " + actual_response)
    else:
        error_message = "Error: " + str(response.status_code) + " " + response.text
        conversation_history_4_gradle[-1][1] = error_message  # Update the latest pair with the error message

    return conversation_history_4_gradle

iface = gr.Interface(
    fn=generate_response,
    inputs=gr.Textbox(lines=2, placeholder="Type here..."),
    outputs=gr.Chatbot(),
    examples=[["Hello"], ["How are you?"]]
)

if __name__ == "__main__":
    iface.launch()
