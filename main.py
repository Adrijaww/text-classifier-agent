from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()

class InputText(BaseModel):
    text: str

def classify_text(text):
    text = text.lower()

    if text.endswith("?"):
        return "Question 🤔"
    elif text.startswith(("please", "do", "go")):
        return "Command ⚡"
    else:
        return "Statement 💬"

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Text Classifier</title>
        <style>
            body {
                font-family: Arial;
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                text-align: center;
                padding-top: 100px;
            }
            .box {
                background: rgba(255,255,255,0.1);
                padding: 30px;
                border-radius: 15px;
                width: 350px;
                margin: auto;
                box-shadow: 0 10px 25px rgba(0,0,0,0.3);
            }
            input {
                width: 90%;
                padding: 10px;
                border-radius: 8px;
                border: none;
                margin-top: 10px;
            }
            button {
                margin-top: 15px;
                padding: 10px 20px;
                border: none;
                border-radius: 8px;
                background: #ff7eb3;
                color: white;
                font-weight: bold;
                cursor: pointer;
            }
            button:hover {
                background: #ff4f9a;
            }
            #result {
                margin-top: 20px;
                font-size: 20px;
                font-weight: bold;
            }
        </style>
    </head>
    <body>

        <div class="box">
            <h2>🤖 AI Text Classifier</h2>
            <p>Enter a sentence:</p>
            <input id="textInput" placeholder="Type something..." />
            <br>
            <button onclick="classify()">Classify</button>

            <div id="result"></div>
        </div>

        <script>
            async function classify() {
                let text = document.getElementById("textInput").value;

                let response = await fetch('/classify', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ text: text })
                });

                let data = await response.json();
                document.getElementById("result").innerText = data.category;
            }
        </script>

    </body>
    </html>
    """

@app.post("/classify")
def classify(input: InputText):
    result = classify_text(input.text)
    return {"category": result}