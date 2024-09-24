import requests
from pexelsapi import pexels
# from pexelsapi.pexels import Pexels
#
# PEXELS_API_KEY = 'rb5fFxb4Z2G7UFvDTGnvczFW9EY0CfdRJRM7bx1dICfARYSF8cj3Etza'
#
# pexel = Pexels(PEXELS_API_KEY)
# search_photos = pexel.search_photos(query='ocean', page=1, per_page=15)
# print(search_photos)

# PEXELS_API_KEY = 'rb5fFxb4Z2G7UFvDTGnvczFW9EY0CfdRJRM7bx1dICfARYSF8cj3Etza'
#
# url = "https://api.pexels.com/v1/search?query=website&per_page=1"
# headers = {
#     "Authorization": f"API_KEY {PEXELS_API_KEY}",
# }
#
# response = requests.get(url, headers=headers)
#
# # Print status code and response content
# print(f"Status Code: {response.status_code}")
# print(f"Response Text: {response}")  # To check raw response content
#
# # # Check if the response is successful (status code 200)
# # if response.status_code == 200:
# #     try:
# #         print(response.json())  # Try parsing JSON if the response is OK
# #     except ValueError:
# #         print("Error: Response is not in JSON format")
# # else:
# #     print("Error: Failed to fetch data from Pexels API")
import requests
from django.shortcuts import render
from openai import OpenAI
import requests
from django.conf import settings
from django.templatetags.static import static
import json

from myapp.views import client

response_data = None
get_code = f"""a: none
a = input
input= (Enter your the range)
for i in a:
print(i)
i+1"""

messages = [
        {"role": "system", "content":
            "You are an AI Assistant that analyzes code, identifies errors, explains the issues, and provides "
            "corrected code."
            "You should output structured data in JSON format with the following keys: "
            "'explanation' - a detailed explanation of the errors found in the code, "
            "'corrected_code' - the code with the issues fixed, "
            "'code_structure' - HTML structure for displaying the code in a styled black box, with syntax "
            "highlighting and a copy button."
         },
        {"role": "user", "content": f"this is my code: {get_code}"},
    ]

response = client.chat.completions.create(
model="gpt-4-1106-preview",
messages=messages,
temperature=0,
        )
response_message = response.choices[0].message.content.strip()
response_data = json.loads(response_message)  # Parse the JSON response

print(response_message)

