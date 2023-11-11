"""

Make sure to use latest version of openai python package
```
pip install openai --upgrade
```

"""

from openai import OpenAI
from keys import OPENAI_KEY

client = OpenAI(
    api_key=OPENAI_KEY
)

response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Who won the world series in 2020?"},
    {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
    {"role": "user", "content": "Where was it played?"}
  ]
)

print(response)
