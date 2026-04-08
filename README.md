# ReAct Prompt Generator App

This repo contains five separate labs/examples.

## Lab 1: ReAct Prompt Generator

**Location:** `lab1/`

### Files

- `lab1/app.py`: CLI entrypoint to print or save the generated prompt.
- `lab1/prompt_template.py`: ReAct prompt generation logic.
- `lab1/react_prompt.txt`: Example output (generated).

### Usage

Run the app and print the prompt:

```bash
python lab1/app.py
```

Save the prompt to a file:

```bash
python lab1/app.py --output lab1/react_prompt.txt
```

## Lab 2: Chain of Thought for Math Problems

**Location:** `lab2/`

### Files

- `lab2/cot_math_template.py`: Chain-of-Thought math prompt generation logic.
- `lab2/cot_math_demo.py`: Example script that calls the OpenAI API for math problems.
- `lab2/app_web.py`: Flask web app for solving math problems in a browser.
- `lab2/templates/index.html`: Web app UI template.
- `lab2/static/style.css`: Web app styles.

### Setup

Install dependencies:

```bash
pip install openai flask
```

Set your API key:

```bash
setx OPENAI_API_KEY "your_api_key_here"
```

Restart your terminal after setting the environment variable.

### Run the CLI demo

```bash
python lab2/cot_math_demo.py
```

Provide a custom problem and model:

```bash
python lab2/cot_math_demo.py --problem "A rectangle has length 12 and width 5. What is its area?" --model gpt-4.1
```

### Run the web app

```bash
python lab2/app_web.py
```

Then open `http://127.0.0.1:5000` in your browser.

## Lab 3: Self-Reflecting Python Code Review Agent

**Location:** `lab3/`

### Files

- `lab3/code_review_template.py`: Self-reflection prompt for structured Python code review.
- `lab3/code_review_demo.py`: CLI script that reviews a Python file or inline code using the API.
- `lab3/sample_buggy_code.py`: Example input file with reviewable issues.

### Setup

Install dependencies:

```bash
pip install openai
```

Set your API key:

```bash
setx OPENAI_API_KEY "your_api_key_here"
```

Optional for OpenRouter or another OpenAI-compatible provider:

```bash
setx OPENAI_BASE_URL "https://openrouter.ai/api/v1"
setx OPENAI_MODEL "openai/gpt-4.1-mini"
```

Restart your terminal after setting environment variables.

### Run the code review demo

Review a Python file:

```bash
python lab3/code_review_demo.py --file lab3/sample_buggy_code.py
```

Review inline Python code:

```bash
python lab3/code_review_demo.py --code "def add(a,b): return a+b"
```

## Lab 4: Customer Support Chatbot Prompt Pack

**Location:** `lab4/`

### Files

- `lab4/customer_support_prompts.py`: Production-ready prompts for ReAct, Self-Reflection, and Structured Output support agents.
- `lab4/app.py`: CLI entrypoint to print one of the Lab 4 prompts.

### Usage

Print the ReAct prompt:

```bash
python lab4/app.py --react
```

Print the Self-Reflection prompt:

```bash
python lab4/app.py --self-reflection
```

Print the Structured Output prompt:

```bash
python lab4/app.py --structured-output
```

## Day 2 Lab 1: Document Indexing with ChromaDB

**Location:** `day2_lab1/`

### Files

- `day2_lab1/index_manual.py`: Load a PDF product manual, split it into chunks, embed it, and store it in ChromaDB.
- `day2_lab1/query_manual.py`: Retrieve relevant chunks from ChromaDB and answer questions with grounded context.
- `day2_lab1/requirements.txt`: Python packages for the Day 2 lab.

### Setup

Install dependencies:

```bash
pip install -r day2_lab1/requirements.txt
```

Set your API configuration:

```bash
setx OPENAI_API_KEY "your_api_key_here"
```

Optional for OpenRouter or another OpenAI-compatible provider:

```bash
setx OPENAI_BASE_URL "https://openrouter.ai/api/v1"
setx OPENAI_MODEL "openai/gpt-4.1-mini"
setx OPENAI_EMBEDDING_MODEL "text-embedding-3-small"
```

Restart your terminal after setting environment variables.

### Index a product manual PDF

```bash
python day2_lab1/index_manual.py --pdf path\\to\\product_manual.pdf
```

### Query the indexed manual

```bash
python day2_lab1/query_manual.py --question "How do I reset the device to factory settings?"
```
