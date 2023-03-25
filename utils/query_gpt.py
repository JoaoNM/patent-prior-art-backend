import OPENAI_KEY
import openai

API_KEY = OPENAI_KEY.OPENAI_API_KEY

openai.api_key = API_KEY
openai.organization = "org-hzFOUxcvM8LcAPohvF4WAIYY"

def query_gpt(text):
    chat = [
        {"role": "user", "content": text},
    ]

    request_body = {
        "model": "gpt-3.5-turbo",
        "messages": chat,
    }

    print("making request to GPT-3...")

    response = openai.ChatCompletion.create(**request_body)

    return response.choices[0].message.content

# Below is sample code to play around for fun. If you want to chat w GPT-3, uncomment the code below and run this file.

# user_query = ""

# chat = [
#     {"role": "user", "content": "Hello! What's the weather like in Johor Bahru? I'm planning a trip there."},
# ]

# while (user_query != "exit"):   

#     if (user_query == "show chat"):
#         print(chat)
#         user_query = input("User: ")
#         continue

#     sample_request = {
#         "model": "gpt-3.5-turbo",
#         "messages": chat,
#     }

#     response = openai.ChatCompletion.create(**sample_request)

#     print(response.choices[0].message)

#     user_query = input("User: ")

#     chat.append(response.choices[0].message)
#     chat.append({"role": "user", "content": user_query})

# print("Thanks for chatting!")