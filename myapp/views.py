from django.shortcuts import render
from openai import OpenAI
import requests
from django.conf import settings
from django.templatetags.static import static
from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse, redirect, reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from .models import UserEmails

# Initialize the OpenAI client with your API key
client = OpenAI(api_key='sk-proj-5MIiz__RGOGkY1MI7hv1qQRBciZHcqBcxpKtZoNHojhP0_xE5oTRV4ju6wSBozhbNNyfQMZE3ST3BlbkFJ'
                        '-wpZP0x7ZWCTxwGZTqzRaqtoM0_6HPSuRi1kOi6l9UHsNKQTlzbMqEpqUmrHjCV-fpjz5KRmYA')


def home(request):
    return render(request, 'main.html')


def country_check(request):
    response_message = None  # Initialize the response_message variable
    if request.method == 'POST':
        user_input = request.POST.get('country_name')
        messages = [
            {"role": "system",
             "content": "You are an adventure guide who creates personalized adventure maps based on user input. When "
                        "a user provides a location or interest, you should generate a custom adventure map that "
                        "includes suggested activities, landmarks, and unique experiences related to that input. The "
                        "response should be detailed and engaging, offering recommendations and interesting facts "
                        "about the location or interest. Make sure the suggestions are relevant to the user’s input. "
                        "the output should not be more then 500 words."
                        "and enhance their exploration experience."
                        "finally, make sure that your output be in the html div so that"
                        "all the headings, bullets points etc should be shown correctly."},

            {"role": "user",
             "content": f"Create a personalized adventure map for '{user_input}'. Include recommended activities, "
                        f"landmarks, and unique experiences related to this location or interest. Provide engaging "
                        f"and relevant information that will help the user explore and enjoy the area or theme they "
                        f"are interested in."},
        ]

        try:
            # Using the Chat Completions API
            response = client.chat.completions.create(
                model="gpt-4-1106-preview",  # model
                messages=messages,
                temperature=0
            )
            # Extracting the response message
            response_message = response.choices[0].message.content.strip()
        except Exception as e:
            response_message = f"An error occurred: {str(e)}"

    return render(request, 'index.html', {'response_message': response_message})


# def gift_suggest(request):
#     response_message = None  # Initialize the response_message variable
#     if request.method == 'POST':
#         # Collecting form data
#         gender = request.POST.get('gender')
#         age = request.POST.get('age')
#         relationship = request.POST.get('relationship')
#         price = request.POST.get('price')
#         gift_type = request.POST.get('gift_type')
#         occasion = request.POST.get('occasion')
#         interests = request.POST.get('interests')
#
#         # Get the full static URL for the image
#         image_url = request.build_absolute_uri(static('pic.png'))
#
#         # Preparing the prompt for ChatGPT
#         messages = [
#             {"role": "system",
#              "content": f"You are an AI assistant that provides personalized gift suggestions based on user input. Use "
#                         "the input provided to generate a list of thoughtful and creative gift ideas that match the "
#                         "recipient's profile. Be sure to include a variety of options that cater to different tastes "
#                         "and preferences. Include detailed descriptions, why the gift would be a good choice, and "
#                         "make sure your response is formatted in HTML with proper headings, lists, and details."
#                         "and it should be enclosed in a Bootstrap card. for example if you give"
#                         "suggestion of 3 products so each product should be in the form of card"
#                         "and that card should have title and all the stuff that usually"
#                         "we use in the cards. and in each row there would be 3 cards. your output should"
#                         "be between 3 to 6 cards. and only give a div as a output"
#                         f"which have the card and then headings and all the stuff. for the image section"
#                         f"you can use this image for now each in card. this is the link of the "
#                         f"image: {image_url}. you can use the same link that I provide you in all cards"
#                         f"image width and height should be 150px"},
#             {"role": "user",
#              "content": f"I need a gift suggestion for a {gender}, aged {age}, who is my {relationship}. "
#                         f"The budget is {price}, and I'm looking for something related to {gift_type}. "
#                         f"It's for a {occasion}, and they are interested in {interests}. Please suggest some unique gift ideas."},
#         ]
#
#         try:
#             # Using the Chat Completions API
#             response = client.chat.completions.create(
#                 model="gpt-4-1106-preview",  # model
#                 messages=messages,
#                 temperature=0
#             )
#             # Extracting the response message
#             response_message = response.choices[0].message.content.strip()
#         except Exception as e:
#             response_message = f"An error occurred: {str(e)}"
#
#     return render(request, 'gift.html', {'response_message': response_message})

PEXELS_API_KEY = 'rb5fFxb4Z2G7UFvDTGnvczFW9EY0CfdRJRM7bx1dICfARYSF8cj3Etza'


# Function to get images from Pexels
def fetch_pexels_image(query):
    url = f"https://api.pexels.com/v1/search?query={query}&per_page=1"
    headers = {
        "Authorization": PEXELS_API_KEY,
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data["photos"]:
            return data["photos"][0]["src"]["medium"]
    return static('pic.png')  # Fallback image


# AI Gift Suggestion View


def gift_suggest(request):
    response_message = None  # Initialize the response_message variable
    if request.method == 'POST':
        # Collecting form data
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        relationship = request.POST.get('relationship')
        price = request.POST.get('price')
        gift_type = request.POST.get('gift_type')
        occasion = request.POST.get('occasion')
        interests = request.POST.get('interests')

        # Get the full static URL for the image
        image_url = request.build_absolute_uri(static('pic.png'))

        # Preparing the prompt for ChatGPT
        messages = [
            {"role": "system",
             "content": f"You are an AI assistant that provides personalized gift suggestions based on user input. Use "
                        "the input provided to generate a list of thoughtful and creative gift ideas that match the "
                        "recipient's profile. Be sure to include a variety of options that cater to different tastes "
                        "and preferences. Include detailed descriptions, why the gift would be a good choice, and "
                        "make sure your response is formatted in HTML with proper headings, lists, and details."
                        "and it should be enclosed in a Bootstrap card. for example if you give"
                        "suggestion of 3 products so each product should be in the form of card"
                        "and that card should have title and all the stuff that usually"
                        "we use in the cards. and in each row there would be 3 cards. your output should"
                        "be between 3 to 6 cards. and only give a div as a output"
                        f"which have the card and then headings and all the stuff. for the image section"
                        f"you can use this image for now each in card. this is the link of the "
                        f"image: {image_url}. you can use the same link that I provide you in all cards but "
                        f"make sure that the size of each image should be 180 * 180 px. make sure to"
                        f"avoid any kinda "
                        f"html words before the divs. and the image should be"
                        f"on the top center of the card"},
            {"role": "user",
             "content": f"I need a gift suggestion for a {gender}, aged {age}, who is my {relationship}. "
                        f"The budget is {price}, and I'm looking for something related to {gift_type}. "
                        f"It's for a {occasion}, and they are interested in {interests}. Please suggest some unique gift ideas."},
        ]

        try:
            # Using the Chat Completions API
            response = client.chat.completions.create(
                model="gpt-4-1106-preview",  # model
                messages=messages,
                temperature=0
            )
            # Extracting the response message
            response_message = response.choices[0].message.content.strip()
        except Exception as e:
            response_message = f"An error occurred: {str(e)}"

    return render(request, 'gift.html', {'response_message': response_message})


def aliveordead(request):
    response_message = None
    if request.method == 'POST':
        name = request.POST.get('name')

        messages = [
            {"role": "system",
             "content": "You are an Ai Assitant. the users will give you a name"
                        "of a calaberity and you are supposed to tell them if"
                        "that celabrity is alive or dead. i know that"
                        "you have limited access but you can just reply"
                        "from whatver the knowledge you have. "
                        "there is one more thing that you must follow. in case the celabrity"
                        "is alive, you should give the DOB of the celabrity."
                        "and in case he is not alive, you can give his"
                        "date of death. "
                        "let say if someone ask: Elon Musk"
                        "you can reply that: Elon Musk is alive, and his Date of birth is "
                        "June 28, 1971."
                        "and in the same way provide the death details."
             },
            {"role": "user", "content": f"{name}, Please let me know this celabrity is alive or dead."
                                        f"if she is alived, tell me his DOB and if he is not alived, give "
                                        f"is date of death"}
        ]
        try:
            response = client.chat.completions.create(
                model="gpt-4-1106-preview",  # model
                messages=messages,
                temperature=0
            )
            response_message = response.choices[0].message.content.strip()

        except Exception as e:
            response_message = f"An error is coming: {str(e)}"

    return render(request, 'alive.html', {'message': response_message})


import json


def fixcode(request):
    response_message = None
    if request.method == 'POST':
        get_code = request.POST.get('get_code')

        messages = [
            {
                "role": "user",
                "content": (
                    "You are an AI Coding Assistant who finds and removes the errors/bugs in the code and provides "
                    "the correct code and explains what the errors were. "
                    "You will be provided with code to analyze and check for errors. "
                    "If any errors are found, first explain the errors and why they occurred. "
                    "Provide the output in Json format with the following keys: "
                    "1. 'explanation': Explains what the error was and why it occurred. This should be in a"
                    " <div> inlcudeing all the"
                    "required html tags like <h>, <ul>, <pre> ete."
                    "2. 'corrected_code': The corrected code inside a <div> inlcudeing all the"
                    "required html tags like <h>, <ul>, <pre> ete."
                    "here is the example output that you are suppose to give"
                    "Example: { 'explanation: <div>\n <h2>Explanation </h2> <br> .............</div>', 'corrected_code': <div>\n <h2>Corrected Code:</h2>\n <pre>\na .....</div>' "
                    "No Extra things please. just to the point json data"
                )
            },
            {
                "role": "user",
                "content": f"Here is my code: {get_code}. also i saw in your last response"
                           f"that you added some extra thing like this: ```json in the start"
                           f"of your answer and also write this ``` at the end of the code"
                           f"so dont do that. i faced many issue while converting this json"
                           f"into the python dictionary. please give the structured output"
                           f"so that i can easily convert it inot python dictionary. also i"
                           f"can see that your last response dont have the corrected code"
                           f"so make sure you are also proving the correct code in the output"
            }
        ]

        try:
            response = client.chat.completions.create(
                model="gpt-4-1106-preview",  # model
                messages=messages,
                temperature=0
            )
            response_message = response.choices[0].message.content.strip()
            try:
                response_message = json.loads(response.choices[0].message.content.strip())
            except json.JSONDecodeError:
                response_message = {"explanation": response.choices[0].message.content.strip(), "corrected_code": ""}
        except Exception as e:
            response_message = f"An error occurred: {str(e)}"

    return render(request, 'code.html', {'message': response_message})


def get_email(request):
     get__email = request.POST.get('get_email')
     em = EmailMessage('A New Entry from Ai Website', f'A New User Signup for the system. here is the email of the '
                                                         f'user: {get__email}', 'atifayub788@gmail.com',
                                                       ['atifayub788@gmail.com',])
     em.send()

     #second email to the subscriber
     em1 = EmailMessage('Thanks for Subscribing Xtreeme Tech', f'Hello, We apperciate your intrest in subscribing our Newsletter. Dont Worry '
                                                               f'we will only send you the emails from which you will be benifited. '
                                                         f'You used this email to subscribe: {get__email}', 'atifayub788@gmail.com',
                                                       [get__email])
     em1.send()
     obj = UserEmails(email=get__email)
     obj.save()
     return redirect(reverse('home'))



