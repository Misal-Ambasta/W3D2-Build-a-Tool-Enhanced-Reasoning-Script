# Q: 3
## 🔧 Problem 3: Build a Tool-Enhanced Reasoning Script

Create a Python script that takes natural language queries and uses an LLM to:

- Interpret the query using chain-of-thought (CoT) style reasoning
- Call external tools (e.g., a calculator function or string counter) when necessary
- Combine results to produce a final answer

The script should decide when a tool is needed (based on prompt output) and call the appropriate function.

### Example queries:

- "What's the square root of the average of 18 and 50?"
- "How many vowels are in the word 'Multimodality'?"
- "Is the number of letters in 'machine' greater than the number of vowels in 'reasoning'?"

## 🧠 Key Concepts:
- Tool-calling with LLMs (manual implementation via string parsing or function mapping)
- Prompt-based reasoning (CoT prompting)
- Decision logic (basic if-else based on LLM outputs)

## 🏗️ Requirements:
- You don't need agents, LangChain, or frameworks
- Tools (like calculator, string counter) should be functions
- Use OpenAI API or any open LLM API to generate reasoning steps
- Output should include:
  - The LLM's reasoning step
  - Whether a tool was used
  - The final answer

## 📝 Submission Guidelines:

Push your code to a GitHub repository

**Structure:**
```
├── main.py
├── tools/
│   ├── math_tools.py
│   └── string_tools.py
├── README.md
└── requirements.txt
```

Your README.md should include:

- How to install and run the script
- Examples of at least 5 test queries and their output
- A note on how your prompt helps decide tool usage
- Provide API key instructions in .env.example