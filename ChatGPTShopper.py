import os
import json
from typing import List
from pydantic import BaseModel
from openai import OpenAI

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
TEST_CHATGPT_RESPONSE = json.dumps({"orders": [{"ProductName": "Bananas", "Quantity": 6, "Weight": 120},
                                    {"ProductName": "Apples", "Quantity": 4, "Weight": 180},
                                    {"ProductName": "Oranges", "Quantity": 3, "Weight": 200},
                                    {"ProductName": "Lettuce", "Quantity": 1, "Weight": 500},
                                    {"ProductName": "Tomatoes", "Quantity": 4, "Weight": 150},
                                    {"ProductName": "Onions (1 kg bag)", "Quantity": 1, "Weight": 1000},
                                    {"ProductName": "Garlic bulbs", "Quantity": 2, "Weight": 60},
                                    {"ProductName": "Carrots (1 kg bag)", "Quantity": 1, "Weight": 1000},
                                    {"ProductName": "Bell peppers", "Quantity": 2, "Weight": 180},
                                    {"ProductName": "Broccoli head", "Quantity": 1, "Weight": 300},
                                    {"ProductName": "Spinach bag", "Quantity": 1, "Weight": 300},
                                    {"ProductName": "Avocados", "Quantity": 2, "Weight": 200},
                                    {"ProductName": "Potatoes (2 kg bag)", "Quantity": 1, "Weight": 2000},
                                    {"ProductName": "Chicken breast pack", "Quantity": 1, "Weight": 1000},
                                    {"ProductName": "Ground beef pack", "Quantity": 1, "Weight": 500},
                                    {"ProductName": "Salmon fillet pack", "Quantity": 1, "Weight": 400},
                                    {"ProductName": "Eggs (12-pack)", "Quantity": 1, "Weight": 700},
                                    {"ProductName": "Tofu block", "Quantity": 1, "Weight": 400},
                                    {"ProductName": "Canned beans (400g can)", "Quantity": 2, "Weight": 400},
                                    {"ProductName": "Canned tuna (160g can)", "Quantity": 3, "Weight": 160},
                                    {"ProductName": "Rice (1 kg bag)", "Quantity": 1, "Weight": 1000},
                                    {"ProductName": "Pasta (500g)", "Quantity": 2, "Weight": 500},
                                    {"ProductName": "Whole wheat bread loaf", "Quantity": 1, "Weight": 700},
                                    {"ProductName": "Tortillas pack", "Quantity": 1, "Weight": 400},
                                    {"ProductName": "Oats (1 kg)", "Quantity": 1, "Weight": 1000},
                                    {"ProductName": "Cereal box", "Quantity": 1, "Weight": 500},
                                    {"ProductName": "Milk (1L)", "Quantity": 2, "Weight": 1000},
                                    {"ProductName": "Greek yogurt tub", "Quantity": 1, "Weight": 500},
                                    {"ProductName": "Cheddar cheese block", "Quantity": 1, "Weight": 400},
                                    {"ProductName": "Butter", "Quantity": 1, "Weight": 250},
                                    {"ProductName": "Olive oil (1L)", "Quantity": 1, "Weight": 1000},
                                    {"ProductName": "Salt (1 kg)", "Quantity": 1, "Weight": 1000},
                                    {"ProductName": "Black pepper (50g)", "Quantity": 1, "Weight": 50},
                                    {"ProductName": "Sugar (1 kg)", "Quantity": 1, "Weight": 1000},
                                    {"ProductName": "Coffee (250g)", "Quantity": 1, "Weight": 250},
                                    {"ProductName": "Tea (box)", "Quantity": 1, "Weight": 40},
                                    {"ProductName": "Tomato sauce jar", "Quantity": 2, "Weight": 500},
                                    {"ProductName": "Peanut butter", "Quantity": 1, "Weight": 400},
                                    {"ProductName": "Honey", "Quantity": 1, "Weight": 250},
                                    {"ProductName": "Soy sauce (500ml)", "Quantity": 1, "Weight": 500},
                                    {"ProductName": "Vinegar (500ml)", "Quantity": 1, "Weight": 500},
                                    {"ProductName": "Mayonnaise", "Quantity": 1, "Weight": 400},
                                    {"ProductName": "Jam", "Quantity": 1, "Weight": 300},
                                    {"ProductName": "Frozen vegetable mix", "Quantity": 1, "Weight": 1000},
                                    {"ProductName": "Frozen berries", "Quantity": 1, "Weight": 500},
                                    {"ProductName": "Ice cream tub", "Quantity": 1, "Weight": 500},
                                    {"ProductName": "Mixed nuts", "Quantity": 1, "Weight": 200},
                                    {"ProductName": "Dark chocolate bar", "Quantity": 2, "Weight": 100},
                                    {"ProductName": "Crackers", "Quantity": 1, "Weight": 200},
                                    {"ProductName": "Orange juice (1L)", "Quantity": 1, "Weight": 1000},
                                    {"ProductName": "Sparkling water (1.5L)", "Quantity": 2, "Weight": 1500},
                                    {"ProductName": "Laundry detergent (2L)", "Quantity": 1, "Weight": 2000},
                                    {"ProductName": "Dish soap (500ml)", "Quantity": 1, "Weight": 500},
                                    {"ProductName": "All-purpose cleaner (750ml)", "Quantity": 1, "Weight": 750},
                                    {"ProductName": "Sponges (3-pack)", "Quantity": 1, "Weight": 50},
                                    {"ProductName": "Paper towels (2 rolls)", "Quantity": 1, "Weight": 500},
                                    {"ProductName": "Trash bags (30-count)", "Quantity": 1, "Weight": 400},
                                    {"ProductName": "Toilet paper (8 rolls)", "Quantity": 1, "Weight": 800},
                                    {"ProductName": "Glass cleaner (500ml)", "Quantity": 1, "Weight": 500},
                                    {"ProductName": "Disinfectant wipes (80-count)", "Quantity": 1, "Weight": 600},
                                    {"ProductName": "Hand soap (250ml)", "Quantity": 1, "Weight": 250}]},indent=2)


# Define data models
class GroceryOrder(BaseModel):
    ProductName: str
    Quantity: int
    Weight: str
    EstCost: float


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
    data = json.loads(content)

    # Validate against schema
    parsed_response = Response(**data)

    # Print validated response
    print("\nStructured Response:")
    print(parsed_response.model_dump_json(indent=2))


if __name__ == "__main__":
    # user_input = input("Enter your prompt: ")
    user_input = "30 year old, single, simple life style, 1 week, all types of groceries including cleaning products"
    ChatResponse = AskChatGPT(user_input)
    # JsonResponsePrint(TEST_CHATGPT_RESPONSE)
    JsonResponsePrint(ChatResponse)