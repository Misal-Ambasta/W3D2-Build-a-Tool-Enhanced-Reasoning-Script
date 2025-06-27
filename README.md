# W3D2-Build-a-Tool-Enhanced-Reasoning-Script

## Overview

This project is a Python CLI tool that takes natural language queries and uses an LLM (OpenAI GPT-3.5-turbo) to:
- Interpret the query using chain-of-thought (CoT) style reasoning
- Call external tools (e.g., calculator functions, string counters, comparators) when necessary
- Combine results to produce a final answer

The script decides when a tool is needed (based on LLM output) and calls the appropriate function. It displays the LLM's reasoning, which tools were used, and the final answer.

## Features
- Tool-calling with LLMs (manual implementation via string parsing and function mapping)
- Prompt-based chain-of-thought reasoning
- Decision logic for tool usage
- Interactive CLI
- Tools supported: add, subtract, multiply, divide, square_root, average, count_vowels, count_letters, compare

## Project Structure
```
├── main.py
├── tools/
│   ├── math_tools.py
│   └── string_tools.py
├── README.md
├── requirements.txt
├── .env.example
└── .gitignore
```

## Setup
1. **Clone the repository**
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up your OpenAI API key**
   - Copy `.env.example` to `.env` and add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     ```

## Usage
Run the CLI:
```bash
python main.py
```
Type your query at the prompt. Type `exit` or `quit` to stop.

## Example Queries and Outputs

### 1. Square root of the average
**Query:**
```
What's the square root of the average of 18 and 50?
```
**Output:**
```
--- Reasoning ---
First, calculate the average of 18 and 50.
TOOL: average(18, 50)
Next, take the square root of the result.
TOOL: square_root(34.0)
The square root of 34 is approximately 5.830.

--- Tools Used ---
average, square_root

--- Final Answer ---
Tool results: {'average': 34.0, 'square_root': 5.830951894845301}
The square root of the average of 18 and 50 is approximately 5.83.
```

### 2. Count vowels in a word
**Query:**
```
How many vowels are in the word 'Multimodality'?
```
**Output:**
```
--- Reasoning ---
Count the vowels in 'Multimodality'.
TOOL: count_vowels('Multimodality')
There are 6 vowels in 'Multimodality'.

--- Tools Used ---
count_vowels

--- Final Answer ---
Tool results: {'count_vowels': 6}
There are 6 vowels in 'Multimodality'.
```

### 3. Compare letters and vowels
**Query:**
```
Is the number of letters in 'machine' greater than the number of vowels in 'reasoning'?
```
**Output:**
```
--- Reasoning ---
Count the letters in 'machine'.
TOOL: count_letters('machine')
Count the vowels in 'reasoning'.
TOOL: count_vowels('reasoning')
Compare the two results.
TOOL: compare(7, 4, '>')
7 is greater than 4, so the answer is yes.

--- Tools Used ---
count_letters, count_vowels, compare

--- Final Answer ---
Tool results: {'count_letters': 7, 'count_vowels': 4, 'compare': True}
Yes, the number of letters in 'machine' is greater than the number of vowels in 'reasoning'.
```

### 4. Basic arithmetic
**Query:**
```
What is 15 divided by 3?
```
**Output:**
```
--- Reasoning ---
Divide 15 by 3.
TOOL: divide(15, 3)
The result is 5.

--- Tools Used ---
divide

--- Final Answer ---
Tool results: {'divide': 5.0}
15 divided by 3 is 5.
```

### 5. Multiple operations
**Query:**
```
What is the sum of the square root of 16 and the average of 10, 20, and 30?
```
**Output:**
```
--- Reasoning ---
First, calculate the square root of 16.
TOOL: square_root(16)
Next, calculate the average of 10, 20, and 30.
TOOL: average(10, 20, 30)
Add the two results.
TOOL: add(4.0, 20.0)
The sum is 24.

--- Tools Used ---
square_root, average, add

--- Final Answer ---
Tool results: {'square_root': 4.0, 'average': 20.0, 'add': 24.0}
The sum of the square root of 16 and the average of 10, 20, and 30 is 24.
```

## How the Prompt Decides Tool Usage
The prompt instructs the LLM to reason step by step and to output each tool call in the format `TOOL: tool_name(args)`. If multiple tools are needed, the LLM is told to output each tool call on a new line, in the order they should be executed, and never to nest tool calls. This allows the script to parse and execute each tool in sequence, and to display all tools used for transparency.

## API Key Instructions
- Copy `.env.example` to `.env` and add your OpenAI API key as shown above.
- Never commit your real API key to version control.

## License
MIT