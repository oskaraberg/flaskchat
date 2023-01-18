import os

import openai
from flask import Flask, redirect, render_template, request, url_for
from time import time, sleep

app = Flask(__name__, static_url_path='')
openai.api_key = os.getenv("OPENAI_API_KEY")
messages = []  # List to store previous messages


@app.route('/', methods=['GET', 'POST'])
def generate_text():
    if request.method == 'POST':
        # Get the input text from the user
        input_text = request.form['input_text']

        # Add the input text to the list of previous messages
        messages.append(f"User: {input_text}")

        # Build the prompt for the API
        prompt = "\n".join([m.replace("Bot: ", "") for m in messages])

        # Use the OpenAI API to generate text
        openai.api_key_path = "openk.txt"
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=1024
        )

        # Extract the generated text from the API response
        generated_text = response["choices"][0]["text"]

        # Add the generated text to the list of previous messages
        messages.append(f"Bot: {generated_text}")

        return render_template('index.html', messages=messages)
    else:
        return render_template('index.html', messages=[])


if __name__ == '__main__':
    app.run()
