import os
import sys
# Add parent directory to path to import my_llm
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from my_llm import llm, get_content

NUM_RUNS_TIMES = 5

# TODO: Fill this in!
YOUR_SYSTEM_PROMPT = """
你是一个帮助反转单词每一个字母的助手，你需要把单词的每一个字母顺序反转

Examples:

Word: "http" (h-t-t-p)
Reversed: "ptth"

"""

USER_PROMPT = """
Reverse the order of letters in the following word. Only output the reversed word, no other text:

helloworld
"""


EXPECTED_OUTPUT = "dlrowolleh"

def test_your_prompt(system_prompt: str) -> bool:
    """Run the prompt up to NUM_RUNS_TIMES and return True if any output matches EXPECTED_OUTPUT.

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
        output_text = get_content(response).strip()
        if output_text.strip() == EXPECTED_OUTPUT.strip():
            print("SUCCESS")
            return True
        else:
            print(f"Expected output: {EXPECTED_OUTPUT}")
            print(f"Actual output: {output_text}")
    return False

if __name__ == "__main__":
    test_your_prompt(YOUR_SYSTEM_PROMPT)