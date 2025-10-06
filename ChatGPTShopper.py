import os
import json
from typing import List
from pydantic import BaseModel
from openai import OpenAI
from tabulate import tabulate


OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
TEST_CHATGPT_RESPONSE = json.load(open("TestGroceryJson.json"))


# Define data models
class GroceryOrder(BaseModel):
    ProductName: str
    Quantity: int
    Weight: str
    EstCost: float
    FoundCost: float = 0


class Response(BaseModel):
    orders: List[GroceryOrder]


def HasAPIKey() -> bool:
    hasKey = OPENAI_API_KEY != ''
    if not hasKey:
        print('OpenAI API key is missing')
    return hasKey


def AskChatGPT(user_input: str) -> str:
    # Initialize client using API key from environment variable
    if not HasAPIKey():
        return ""
    client = OpenAI(api_key=OPENAI_API_KEY)

    # Prompt input from user
    # user_input = input("Enter your prompt: ")

    # Send request to Chat Completions API
    response = client.chat.completions.parse(
        model="gpt-5",
        messages=[
            {"role": "system", "content": "You will be simulating a person doing groceries"
                                          "Rules:"
                                          "- do not include the weight as part of the product name"
                                          "- only include the weight in the Weight field"
                                          "- Include an estimated cost for the product in the estmated cost field in Australian Dollars"
                                          "- The cost must be from Australian, Victoria supermarkets"},
            {"role": "user", "content": user_input}
        ],
        response_format=Response
    )

    # Print the response content
    # Extract and parse JSON response
    content = response.choices[0].message.content
    JsonResponsePrint(content)


def JsonResponsePrint(content):
    data = json.loads(json.dumps(content))


    try:
        # Validate against schema
        parsed_response = Response(**data)
        # Print validated response
        print("\nStructured Response:")
        # print(parsed_response.model_dump_json(indent=2))
        print(tabulate(data.get("orders", []), headers="keys", tablefmt="grid"))

    except Exception as e:
        print(e)

def CalculateCost(content) -> float:
    data = json.loads(json.dumps(content))
    # orders: list[GroceryOrder] = data.get("orders", [])
    cost: float = 0
    # print(orders)
    orders = [GroceryOrder(**o) for o in data["orders"]]

    for order in orders:
        cost += order.Quantity * order.EstCost
    return cost

if __name__ == "__main__":
    # user_input = input("Enter your prompt: ")
    user_input = "30 year old, single, simple life style, 1 week, all types of groceries including cleaning products"
    # ChatResponse = AskChatGPT(user_input)
    # JsonResponsePrint(ChatResponse)
    # JsonResponsePrint(TEST_CHATGPT_RESPONSE)
    print(f"Total cost: {CalculateCost(TEST_CHATGPT_RESPONSE)}")
