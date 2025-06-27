# main.py placeholder for tool-enhanced reasoning script 
import os
from openai import OpenAI
from dotenv import load_dotenv
from tools import math_tools, string_tools

# Load environment variables
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

# Tool mapping for manual function calls
tool_functions = {
    'add': math_tools.add,
    'subtract': math_tools.subtract,
    'multiply': math_tools.multiply,
    'divide': math_tools.divide,
    'square_root': math_tools.square_root,
    'average': math_tools.average,
    'count_vowels': string_tools.count_vowels,
    'count_letters': string_tools.count_letters,
    'compare': lambda a, b, op: eval(f'{a} {op} {b}')  # pseudo-tool for comparison
}

def call_openai(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        temperature=0.2,
    )
    return response.choices[0].message.content


def process_query(query):
    """
    Given a user query, use OpenAI to reason step-by-step and decide if a tool is needed.
    If so, call the tool(s) and combine the result into the final answer.
    Returns a dict with keys: reasoning, tools_used, final_answer
    """
    # Prompt for chain-of-thought reasoning and tool suggestion
    cot_prompt = f"""
You are an AI assistant that can use tools to help answer questions. Here are the available tools:
- add(a, b): Add two numbers
- subtract(a, b): Subtract b from a
- multiply(a, b): Multiply two numbers
- divide(a, b): Divide a by b
- square_root(x): Square root of x
- average(a, b, ...): Average of two or more numbers
- count_vowels(s): Count vowels in a string
- count_letters(s): Count letters in a string
- compare(a, b, op): Compare two values with an operator (>, <, ==, etc.)

Given the user query, reason step by step (chain-of-thought). If a tool is needed, specify the tool and its arguments in the format:
TOOL: tool_name(arg1, arg2, ...)
If multiple tools are needed, specify each TOOL call on a new line, one per line, in the order they should be executed. Do not nest tool calls inside each other; always show each TOOL call separately, even if one uses the result of another.
Otherwise, answer directly.

User query: {query}
Reasoning and answer:"""
    cot_response = call_openai(cot_prompt)

    import re
    tool_pattern = r'TOOL:\s*(\w+)\(([^)]*)\)'
    matches = re.findall(tool_pattern, cot_response)
    tools_used = []
    tool_results = {}
    final_answer = None
    reasoning = cot_response.strip()
    # For chaining tool calls, keep a context for intermediate results
    context = {}
    for tool_name, args_str in matches:
        args = [arg.strip().strip("'\"") for arg in args_str.split(',') if arg.strip()]
        # Convert args to appropriate types
        if tool_name in ['add', 'subtract', 'multiply', 'divide', 'square_root', 'average']:
            args = [float(arg) if arg.replace('.', '', 1).isdigit() or (arg.startswith('-') and arg[1:].replace('.', '', 1).isdigit()) else context.get(arg, arg) for arg in args]
        elif tool_name in ['count_vowels', 'count_letters']:
            args = [args[0]]
        elif tool_name == 'compare':
            # compare(a, b, op)
            if len(args) == 3:
                a = float(args[0]) if args[0].replace('.', '', 1).isdigit() else context.get(args[0], args[0])
                b = float(args[1]) if args[1].replace('.', '', 1).isdigit() else context.get(args[1], args[1])
                op = args[2]
                args = [a, b, op]
        tool_func = tool_functions.get(tool_name)
        if tool_func:
            try:
                result = tool_func(*args)
                # Store result in context for possible chaining
                context[f'{tool_name}_result'] = result
                tool_results[tool_name] = result
                if tool_name not in tools_used:
                    tools_used.append(tool_name)
            except Exception as e:
                tool_results[tool_name] = f"Error: {e}"
                if tool_name not in tools_used:
                    tools_used.append(tool_name)
        else:
            tool_results[tool_name] = "Tool not recognized."
            if tool_name not in tools_used:
                tools_used.append(tool_name)
    if matches:
        # If tools were used, append their results to the answer
        final_answer = f"Tool results: {tool_results}\n"
        # Try to extract a final answer from the LLM's output after the last TOOL line
        last_tool_idx = 0
        for m in re.finditer(tool_pattern, cot_response):
            last_tool_idx = m.end()
        after_tools = cot_response[last_tool_idx:].strip()
        if after_tools:
            final_answer += after_tools
    else:
        final_answer = cot_response.strip()
    return {
        'reasoning': reasoning,
        'tools_used': tools_used,
        'final_answer': final_answer
    }

if __name__ == "__main__":
    print("Welcome to the Tool-Enhanced Reasoning CLI! Type 'exit' or 'quit' to stop.")
    while True:
        user_query = input("\nEnter your query: ").strip()
        if user_query.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break
        result = process_query(user_query)
        print("\n--- Reasoning ---")
        print(result['reasoning'])
        print("\n--- Tools Used ---")
        print(', '.join(result['tools_used']) if result['tools_used'] else "None")
        print("\n--- Final Answer ---")
        print(result['final_answer']) 