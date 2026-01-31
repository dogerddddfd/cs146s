import os
import re
import sys

# Add parent directory to path to import my_llm
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from my_llm import llm, get_content

NUM_RUNS_TIMES = 1

# YOUR_SYSTEM_PROMPT = """
# 你是一个专业的数学模型，擅长解决数学问题，请对给定的问题一步步进行思考。
# ---例子1：
# 问题：3^12345 (mod 100)
# 思考：
# 1. 3^12345 = 3 * 3^12344
# 2. 3^12344 = (3^2)^6172
# 3. (3^2)^6172 = (9)^6172
# 4. (9)^6172 = 81^3086
# 5. 81^3086 = (81 * 81)^1543
# 6. (81 * 81)^1543 = (6561)^1543
# 7. 6561^1543 mod 100
#    - 6561 mod 100 = 61
#    - 61^2 mod 100 = 3721 mod 100 = 21
#    - 61^4 mod 100 = 21^2 mod 100 = 441 mod 100 = 41
#    - 61^8 mod 100 = 41^2 mod 100 = 1681 mod 100 = 81
#    - 61^16 mod 100 = 81^2 mod 100 = 6561 mod 100 = 61
#    - 发现周期为4，61^(4k) mod 100 = 41，61^(4k+1) mod 100 = 61，61^(4k+2) mod 100 = 21，61^(4k+3) mod 100 = 81
#    - 1543 = 4*385 + 3，所以61^1543 mod 100 = 81
# 8. 3^12345 mod 100 = 3 * 81 mod 100 = 243 mod 100 = 43

# Answer: 43
# ---
# 最后按照给定的格式输出最终答案。
# """

YOUR_SYSTEM_PROMPT = """
你是一个专业的数学模型，擅长解决数学问题，请对给定的问题一步步进行思考。
最后按照给定的格式输出最终答案。
"""


USER_PROMPT = """
Solve this problem, then give the final answer on the last line as "Answer: <number>".

what is 3^{12345} (mod 100)?
"""


# For this simple example, we expect the final numeric answer only
EXPECTED_OUTPUT = "Answer: 43"


def extract_final_answer(text: str) -> str:
    """Extract the final 'Answer: ...' line from a verbose reasoning trace.

    - Finds the LAST line that starts with 'Answer:' (case-insensitive)
    - Normalizes to 'Answer: <number>' when a number is present
    - Falls back to returning the matched content if no number is detected
    """
    matches = re.findall(r"(?mi)^\s*answer\s*:\s*(.+)\s*$", text)
    if matches:
        value = matches[-1].strip()
        # Prefer a numeric normalization when possible (supports integers/decimals)
        num_match = re.search(r"-?\d+(?:\.\d+)?", value.replace(",", ""))
        if num_match:
            return f"Answer: {num_match.group(0)}"
        return f"Answer: {value}"
    return text.strip()


def test_your_prompt(system_prompt: str) -> bool:
    """Run up to NUM_RUNS_TIMES and return True if any output matches EXPECTED_OUTPUT.

    Prints "SUCCESS" when a match is found.
    """
    for idx in range(NUM_RUNS_TIMES):
        print(f"Running test {idx + 1} of {NUM_RUNS_TIMES}")
        response = llm(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": USER_PROMPT},
            ],
            enable_thinking=False
        )
        output_text = get_content(response)
        final_answer = extract_final_answer(output_text)
        if final_answer.strip() == EXPECTED_OUTPUT.strip():
            print("SUCCESS")
            return True
        else:
            print(f"Expected output: {EXPECTED_OUTPUT}")
            print(f"Actual output: {final_answer}")
    return False


if __name__ == "__main__":
    test_your_prompt(YOUR_SYSTEM_PROMPT)


