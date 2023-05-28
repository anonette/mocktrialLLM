#  Chain of Thought
#        /\__/\   - main.py 
#       ( o.o  )  - v0.0.1
#         >^<     - by @rUv
 
from fastapi import APIRouter, FastAPI, HTTPException
from pydantic import BaseModel, Field
from starlette.responses import RedirectResponse
import guidance
import uvicorn

app = FastAPI()
router = APIRouter()

class Query(BaseModel):
  query: str = Field(
    "The public needs a judge that will be overseeing a case involving AI/ML causing injury, under the EU AI Act and related regulations, that will personify expertise in legal interpretation and application of the complexities of the EU AI Act and other relevant regulations to the specifics of the case. You will have comprehensive understanding of the law, its context, and its implications for AI/ML scenarios, maintaining an unbiased perspective throughout the case, and ensuring fair treatment of all parties involved. This necessitates demanding and objectively evaluating the evidence, drawing conclusions purely based on the law and the facts.",
    description="The query to give to the AI.",
  )

# Set the default language model used to execute guidance programs
guidance.llm = guidance.llms.OpenAI("gpt-3.5-turbo")

# Define a list of topics in the chain of thought for consulting

topics = [
    "Understanding the Lawyers Arguments",
    "Context of EU AI act",
    "Liability Directive",
    "Risk Assessment",
    "Solution Formulation",
    "Emotional Intelligence and Empathy",
    "Implementation and Impact",
    "Continuous Improvement",
    "Ethics and Social Responsibility"
]#


# topics = [
#     "Understanding the Client's Needs",
#     "Industry Context",
#     "Internal Capabilities and Resources",
#     "Stakeholder Analysis",
#    "Risk Assessment",
#     "Solution Formulation",
#    "Emotional Intelligence and Empathy",
#    "Implementation and Impact",
#    "Continuous Improvement",
#    "Ethics and Social Responsibility"
#]



# Define a guidance program for consulting
program = guidance('''
{{#system~}}
You are an impartial and knowlegable judge.
{{~/system}}

{{#user~}}
I have a question on how to rule in this particular case:
{{query}}
Name 3 relevant articles from the EU AI act and the AI liability directive that would be great at addressing this?
Don't answer the question yet.
{{~/user}}

{{#assistant~}}
{{gen 'client_needs_strategies' temperature=0 max_tokens=300}}
{{~/assistant}}

{{#user~}}
Great, now please answer the question as if these strategies had been implemented.
{{~/user}}

{{#assistant~}}
{{gen 'client_needs' temperature=0 max_tokens=500}}
{{~/assistant}}

''')

# Execute the guidance program with the provided query
for topic in topics:
    print(f"Processing topic: {topic}")
    result = program(query=topic)
    
    # Convert the result to a string
    result_str = str(result)

    # Extract the assistant's messages
    response_parts = result_str.split('\nassistant\n')

    # Get the last assistant's response, ignoring any empty trailing parts
    last_response = next((part for part in reversed(response_parts) if part.strip()), '')
   
    print(f"Last response: {last_response}\n")

@router.post("/consulting")
async def get_consulting(query: Query):
  try:
    # Execute the guidance program with the provided query
    result = program(query=query.query)
    
    # Convert the result to a string
    result_str = str(result)

    # Extract the assistant's messages
    response_parts = result_str.split('\nassistant\n')

    # Get the last assistant's response, ignoring any empty trailing parts
    last_response = next((part for part in reversed(response_parts) if part.strip()), '')

    return {"response": last_response}
  except UnicodeDecodeError:
    return {"error": "Response contains non-utf-8 characters"}
  except Exception as e:
    return {"error": str(e)}

app.include_router(router)

@app.get("/")
async def root():
    return RedirectResponse(url='/docs')

# This block is executed when this script is run directly (not imported as a module)
if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8000)  # Start the Uvicorn server
Request