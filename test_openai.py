"""

Make sure to use latest version of openai python package
```
pip install openai --upgrade
```

"""

from openai import OpenAI
from keys import OPENAI_KEY

client = OpenAI(
    api_key=OPENAI_KEY,
    # LauzHack
    organization="org-bcv27ooZj8JyXgpgj5sed8rH",
)

# -- chat
response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  # giving history of chat
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Who won the world series in 2020?"},
    {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
    {"role": "user", "content": "Where was it played?"}
  ]
)

# extract text
print(response.choices[0].message.content)

# # -- image
# response = client.images.generate(
#   model="dall-e-3",
#   prompt="a white siamese cat",
#   size="1024x1024",
#   quality="standard",
#   n=1,
# )
# image_url = response.data[0].url
# print(image_url)
