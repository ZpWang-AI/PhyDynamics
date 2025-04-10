from utils_zp import *
from openai import OpenAI
# Set OpenAI's API key and API base to use vLLM's API server.


openai_api_key = "EMPTY"
openai_api_base = "http://localhost:8001/v1"

client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)


def llm_api(queries:Union[str, List[str]], messages=None):
    def inner(messages_):
        chat_response = client.chat.completions.create(
            model="Qwen/Qwen2.5-7B-Instruct",
            messages=messages_,
            # temperature=0.7,
            temperature=0,
            top_p=0.8,
            max_tokens=512,
            extra_body={
                "repetition_penalty": 1.05,
            },
        )
        ret = chat_response.choices[0].message.content
        # print('>', ret)
        return ret

    if isinstance(queries, str):
        if messages is None:
            messages = [
                {"role": "system", "content": "You are Qwen, created by Alibaba Cloud. You are a helpful assistant."},
                {"role": "user", "content": queries},
            ]
            return inner(messages)
    else:
        messages = [
            {"role": "system", "content": "You are Qwen, created by Alibaba Cloud. You are a helpful assistant."},
                # {"role": "user", "content": "Tell me something about large language models."},
        ]
        for query in queries:
            messages.append({'role': 'user', 'content': query})
            messages.append({'role': 'assistant', 'content': inner(messages)})
        return messages[-1]['content']


PROMPT1 = """
## Task
I will give you a sentence. 
If the sentence solely involves humans, their clothing, or the camera they are facing, output "Yes". 
If the sentence includes mentions of other living or non-living things (such as pets, cars, water, or food), output "No". 
Here are two examples.

## Examples
### Input 1
A man is laughing.
### Expected output 1
Yes
### Input 2
A woman driving a car in a blue skirt is talking to her friends.
### Expected output 2
No

## Actual task
### Input
{caption}
### Output  
    """.strip()

PROMPT2 = """
## Task
I will give you a sentence. 
If the sentence mentions an action or movement by humans, output "Yes". 
If the sentence solely refers to humans without mentioning any actions or movements, output "No". 
Here are two examples.

## Examples
### Input 1
A group of people are talking about something.
### Expected output 1
Yes
### Input 2
A group of people in white coats standing next to each other.
### Expected output 2
No

## Actual task
### Input
{caption}
### Output  
    """.strip()

PROMPT3 = """
## Task
I will give you a sentence. 
If the sentence solely states that a human or a group of humans is talking, without mentioning any other actions or movements, output "Yes". 
If the sentence includes any other actions or movements (such as playing sports, making music, working, cooking, etc.), output "No". 
Here are two examples.

## Examples
### Input 1
A man in a blue shirt is talking to the camera.
### Expected output 1
Yes
### Input 2
A person is mixing something in a bowl.
### Expected output 2
No

## Actual task
### Input
{caption}
### Output  
    """.strip()




if __name__ == '__main__':
    # A man in a blue shirt talking to the camera.
    target_caption = '''
There are two soccer players, one in a black and red jersey and the other in a blue and white jersey, playing against each other on a field with a crowd of people watching.
'''.strip()

    print(llm_api(PROMPT1.format(caption=target_caption)))
    print(llm_api(PROMPT2.format(caption=target_caption)))
    print(llm_api(PROMPT3.format(caption=target_caption)))
