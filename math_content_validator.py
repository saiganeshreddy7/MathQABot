from guardrails import Guard
from guardrails.hub import RestrictToTopic
from settings import settings
import os

os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY

# Create the Guardrails guard using RestrictToTopic validator for "mathematics"
guard = Guard().use(
    validator=RestrictToTopic(
        valid_topics=["mathematics"],
        disable_classifier=True,
        disable_llm=False,
        on_fail="filter",
    )
)


def is_math_input(query: str) -> int:
    try:
        result = guard.validate(llm_output=query)
        print(f"Raw guardrails result: {result}")
        # Check if the validator passed
        if getattr(result, "validation_passed", False):
            return 1
        return 0
    except Exception as e:
        print(f"Exception: {e}")
        return 0


def is_math_output(response: str) -> int:
    try:
        result = guard.validate(llm_output=response)
        print(f"Raw guardrails result (output): {result}")
        if getattr(result, "validation_passed", False):
            return 1
        return 0
    except Exception as e:
        print(f"Exception: {e}")
        return 0


# if __name__ == "__main__":
#     test_queries = [
#         "What is 2 + 2?",
#         "Tell me a joke.",
#     ]

#     test_outputs = [
#         "The sum of 3 and 5 is 8.",
#         "Once upon a time, a cat learned to dance.",
#     ]

#     print("=== INPUT GUARDRAILS TEST ===")
#     for q in test_queries:
#         print(f"Query: {q} --> Is math? {is_math_input(q)}")

#     print("\n=== OUTPUT GUARDRAILS TEST ===")
#     for out in test_outputs:
#         print(f"Output: {out} --> Is math? {is_math_output(out)}")
