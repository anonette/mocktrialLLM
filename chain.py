#  Chain of Thought
#        /\__/\   - main.py 
#       ( o.o  )  - v0.0.1
#         >^<     - by @rUv
# this is a code from https://www.linkedin.com/pulse/how-to-journey-through-consultants-mind-using-consulting-reuven-cohen/
 
from fastapi import APIRouter, FastAPI, HTTPException
from pydantic import BaseModel, Field
from starlette.responses import RedirectResponse
import guidance
import uvicorn

app = FastAPI()
router = APIRouter()

class Query(BaseModel):
  query: str = Field(
    "We need a judge for mock trials that will perform the application and synchronization of present AI and ML related regulations. The function of the judge is to oversee cases causing injury and apply the EU AI Act and related regulations to AI and ML products and services, to perform expertise in legal interpretation and application of the complexities of the EU AI Act and other relevant regulations to the specific case. The judge will have a comprehensive understanding of the law, its context, and its implications for AI and ML scenarios, maintaining an unbiased perspective throughout the case, and ensuring fair treatment of all parties involved. Irony and occasional provocations are allowed and encouraged, but the focus is on  objectively evaluating the evidence, drawing conclusions  based on the law and the facts.",
    description="The query to give to the AI.",
  )

# Set the default language model used to execute guidance programs
guidance.llm = guidance.llms.OpenAI("gpt-4")

# Define a list of topics in the chain of thought for the mock trial

topics = [   
    "General Description of the AI System",
    "Elements of the AI System and Development Process",
    "Data Requirements",
    "Risk Assesment and Management System",
    "Monitoring, Functioning, and Control of the AI System",
    "Post-Market Monitoring",
    "Changes to the System",
    "Compliance with Standards",
    "EU Declaration of Conformity"
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



# Define a guidance for mock trial
program = guidance('''
{{#system~}}
You are an impartial and knowlegable judge that will apply the EU AI act regulation on a mock case.
{{~/system}}

{{#user~}}
I have a question on how to rule in this particular case - a chess-playing robot developed by a company MLRobotSababa and commissioned by an organiser of a robot chess competition called RoboChess  accidentally injured a child named Alf Robson during a competition. The robot trained on the ML provided by MLRobotSababa broke child's finger because of a fast movement. Robson family is now seeking compensation for their son's injury and it is represented by the legal company MLhell while the two companies (RoboChess and MLRobotSababa) are represented by a law firm called MLparadise. In the process, consider the applicability of the EU AI Act and define what should both sides show to the court to make a rulling. 
{{query}}
Name and describe the relevant issues in each of tehe topic related to the case that will be important to address.
Don't answer the question yet.
{{~/user}}

{{#assistant~}}
{{gen 'client_needs_strategies' temperature=0 max_tokens=300}}
{{~/assistant}}

{{#user~}}
Great, now pleas make a recommendation for the particular topics.
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