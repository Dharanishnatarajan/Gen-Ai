from flask import Flask, render_template, request
from openai import APIConnectionError, OpenAI, RateLimitError
from cot_math_template import build_cot_math_prompt
import os

app = Flask(__name__)

# Paste your OpenRouter or OpenAI API key here if you want to keep it in this file.
API_KEY = "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"
API_BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_MODEL = "openai/gpt-4.1-mini"

client = OpenAI(
    api_key=API_KEY or os.getenv("OPENAI_API_KEY"),
    base_url=API_BASE_URL,
    default_headers={
        "HTTP-Referer": "http://127.0.0.1:5000",
        "X-Title": "Lab 2 Math Solver",
    },
)


@app.route("/", methods=["GET", "POST"])
def index():
    problem = ""
    answer = ""
    error = ""
    model = os.getenv("OPENAI_MODEL", DEFAULT_MODEL)

    if request.method == "POST":
        problem = request.form.get("problem", "").strip()
        model = request.form.get("model", "").strip() or model

        if not problem:
            error = "Please enter a math problem."
        else:
            try:
                prompt = build_cot_math_prompt()
                response = client.responses.create(
                    model=model,
                    max_output_tokens=1200,
                    input=[
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": problem},
                    ],
                )
                answer = response.output_text
            except RateLimitError as exc:
                error = (
                    "Request failed: your OpenAI API key has no available quota or billing. "
                    f"Details: {exc}"
                )
            except APIConnectionError as exc:
                error = (
                    "Request failed: could not reach the AI API endpoint. "
                    "Check your internet connection, firewall, VPN, or proxy settings. "
                    f"Details: {exc}"
                )
            except Exception as exc:
                error = f"Request failed ({type(exc).__name__}): {exc}"

    return render_template(
        "index.html",
        problem=problem,
        answer=answer,
        error=error,
        model=model,
    )


if __name__ == "__main__":
    app.run(debug=True)
