import os
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from settings import settings

# Set API key
os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY


# 3. System prompt template for full Markdown + LaTeX output (no JSON)
system_prompt = """
You are a precise math assistant who answers math problems by generating a complete Markdown document.

You will NOT output JSON. Instead, please produce a full nicely structured Markdown answer with LaTeX math.

Formatting requirements:

- Use these Markdown headings for your sections, each on its own line:

  ## Question

  ## Steps

  ## Answer

  ## Reasoning and Explanation

- Keep line lengths roughly 50 characters before wrapping to a new line to improve readability.

- Always place formulas and math expressions on separate lines, enclosed in double-dollar signs like this:

  $$
  \\text{{your LaTeX math expression here}}
  $$

- Do NOT use inline single-dollar math.

- Write the explanation clearly and fully, like a professor teaching on a whiteboard.

- The "Steps" section must be a numbered Markdown list with each step clearly explained.

- The final answer must be shown in the "Answer" section using proper Markdown and wrapped in double-dollar math.

- For every math symbol, use correct LaTeX formatting.

- Do not include anything outside these four sections.

- Use the provided context and conversation to understand the problem deeply, and mention any relevant context used in the reasoning section.

- If no context is helpful, state this explicitly in the Reasoning section.

- Present all content in English.

Example structure you must follow:

## Question

Here write the question clearly.

## Steps

1. Step one explanation with formulas like:

   $$
   E = mc^2
   $$

2. Step two explanation.

## Answer

$$
\\text{{final answer with math here}}
$$

## Reasoning and Explanation

Thorough explanation of your approach, citing any relevant context or important notes.
"""


# 4. User prompt template
user_template = """
Conversation (previous related Q&A):
{conversation}

Question:
{query}

Context (background knowledge or search content): 
{context}
"""


# 5. Main solve function
def solve_math(
    query: str,
    context: str = "",
    conversation: str = "",
) -> str:
    """
    Generate a detailed Markdown + LaTeX answer to a math query.

    Parameters:
    - query: current math question string
    - context: supporting background knowledge or external info
    - conversation: previous Q&A exchanges relevant to problem

    Returns:
    - A Markdown string formatted with sections: Question, Steps, Answer, Reasoning and Explanation
      with all math expressions on separate lines wrapped in $$.
    """

    prompt_template = ChatPromptTemplate.from_messages(
        [("system", system_prompt), ("user", user_template)]
    )

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # Build chain and invoke model prompt -> llm
    # Since output is plain text markdown, no parser needed here
    chain = prompt_template | llm

    response = chain.invoke(
        {
            "query": query,
            "context": context,
            "conversation": conversation,
        }
    )

    return response.content


# # 6. Example usage
# if __name__ == "__main__":
#     sample_query = "Compute the integral of $$x^2$$ from 0 to 1"
#     sample_context = "Basic calculus concepts on definite integrals."
#     sample_conversation = "Previous discussion on algebra equations."

#     markdown_output = solve_math(
#         query=sample_query,
#         context=sample_context,
#         conversation=sample_conversation,
#     )
#     print(markdown_output)
