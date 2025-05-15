"""
pip install together

Overview of models (chat, image, audio):
https://docs.together.ai/docs/serverless-models

Example usage:
https://github.com/togethercomputer/together-cookbook

"""


from together import Together
from keys import TOGETHER_AI

# auth defaults to os.environ.get("TOGETHER_API_KEY")
client = Together(
    api_key=TOGETHER_AI,
)

### TEXT
response = client.chat.completions.create(
    # model="Qwen/Qwen3-235B-A22B-fp8-tput",
    model="meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
    # messages=[{"role": "user", "content": "What are some fun things to do in New York?"}]
    # giving history of chat
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
        {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        {"role": "user", "content": "Where was it played?"}
    ]
)
print(response.choices[0].message.content)

### IMAGE
response = client.images.generate(
    prompt="Cats eating popcorn while programming",
    model="black-forest-labs/FLUX.1-dev",
    steps=10,
    n=4
)
print("\nimage url : ", response.data[0].url)

### AUDIO generation
# -- available voices: https://docs.together.ai/docs/text-to-speech#voices-available
speech_file_path = "speech.wav"
response = client.audio.speech.create(
    model="cartesia/sonic",
    input="Today is a wonderful day to build something people love!",
    voice="1920's radioman",
    )
response.stream_to_file(speech_file_path)
print("\naudio file saved to", speech_file_path)