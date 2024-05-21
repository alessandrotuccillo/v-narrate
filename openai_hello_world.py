from openai import OpenAI
import os

# Create client
client = OpenAI(
    # Load your API key from the environment variable
    api_key = os.environ.get("OPENAI_API_KEY"),
)

'''
# Set up the prompt for the GPT model
prompt = "In order to give GPT-4 an image as input, is it sufficient to upload the images on a Google Drive and then give the respective link as URL to gpt?"

# Call the OpenAI API to generate a response
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{'role': 'user', "content": prompt}]
)

# Print the generated greeting
print(response.choices[0].message.content)
'''

text = "How do I cook an egg in the provided scene?"

# Call the API with prompt specified by text
response = client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": text},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://i.ibb.co/WPJScDn/IMG-5375.png"
                    },
                },
            ],
        }
    ],
    max_tokens=300
)

print(response.choices[0].message.content)

with open("C:\\Users\\aless\\OneDrive\\Desktop\\Data performance\\8 - water bottle, flower, fire estinguisher, lemon, plate, glass, coffee machine, energy drink.txt", 'a') as f:
    f.write('PROMPT:' + text + '\n' + response.choices[0].message.content + '\n' + '\n')