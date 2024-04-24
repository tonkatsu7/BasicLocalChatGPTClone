import requests
import json
import gradio as gr

url = "http://localhost:11434/api/generate"

headers = {
    'Content-Type': 'application/json'
}

conversation_history = []

def generate_response(prompt):
    # Append user message to history with a placeholder for the response
    conversation_history.append({"user": prompt, "bot": None})

    # Generate the full prompt for llama2
    full_prompt = "\n".join(f"prompt: {entry['user']}\nresponse: {entry['bot']}" for entry in conversation_history if entry['bot'])
    full_prompt += f"\nprompt: {prompt}\nresponse: "

    print(full_prompt)  # For debugging

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
        # Update the latest entry with the bot's response
        conversation_history[-1]["bot"] = actual_response
    else:
        error_message = "Error: " + str(response.status_code) + " " + response.text
        # Update the latest entry with the error message
        conversation_history[-1]["bot"] = error_message

    # Prepare the data in the format expected by Gradio Chatbot
    gradio_format = [[entry['user'], entry['bot']] for entry in conversation_history if entry['bot'] is not None]
    return gradio_format

iface = gr.Interface(
    fn=generate_response,
    inputs=gr.Textbox(lines=2, placeholder="Type here..."),
    outputs=gr.Chatbot(),
    examples=[["Hello"], ["How are you?"]]
)

if __name__ == "__main__":
    iface.launch()
