import guidance
import re
guidance.llm = guidance.llms.OpenAI("gpt-4")
role_simulator = guidance('''
{{#system~}}
You are an impartial and knowlegable judge.
{{~/system}}

{{#user~}}
You will answer the user as {{role}} in the following conversation. At every step, I will provide you with the user input, as well as a comment reminding you of your instructions. Never talk about the fact that you are an AI, even if the user asks you. Always answer as {{role}}.
{{#if first_question}}You can also start the conversation.{{/if}}
{{~/user}}
                                           
{{~! The assistant either starts the conversation or not, depending on if this is the first or second agent }}
{{#assistant~}}
Ok, I will follow these instructions.
{{#if first_question}}Let me start the conversation now:
{{role}}: {{first_question}}{{/if}}
{{~/assistant}}

{{~! Then the conversation unrolls }}
{{~#geneach 'conversation' stop=False}}
{{#user~}}
User: {{set 'this.input' (await 'input')}}
Comment: Remember, answer as a {{role}}. Start your utterance with {{role}}:
{{~/user}}

{{#assistant~}}
{{gen 'this.response' temperature=0 max_tokens=300}}
{{~/assistant}}
{{~/geneach}}''')

litigator = role_simulator(role='Personal Injury Lawyer', await_missing=True)
defense = role_simulator(role='Defense Lawyer', await_missing=True)

first_question = '''What do you think is the best way to stop inflation?'''
litigator = litigator(input=first_question, first_question=None)
defense = defense(input=defense["conversation"][-2]["response"].strip('Personal Injury Lawyer: '), first_question=first_question)
for i in range(2):
    litigator = litigator(input=defense["conversation"][-2]["response"].replace('Defense Lawyer: ', ''))
    defense = defense(input=litigator["conversation"][-2]["response"].replace('Personal Injury Lawyer: ', ''))
print('Defense Lawyer: ' + first_question)
for x in defense['conversation'][:-1]:
    print('Personal Injury Lawyer:', x['input'])
    print()
    print(x['response'])