# Telegram bots and APIs, [SLIDES](https://go.epfl.ch/telegram-apis)

First used at a [mini-hackathon](https://lu.ma/lauzhack-apis-2023) (Nov 11, 2023).

Slides and recordings can be found here: https://go.epfl.ch/telegram-apis

## Installation

```bash
# 1) create and activate virtual environment
# -- EITHER with conda
conda create -n apis_env python=3.11
conda activate apis_env
# -- OR with venv
python3.11 -m venv apis_env
source apis_env/bin/activate

# 2) install dependencies
(apis_env) pip install -r requirements.txt
```

## Usage 

1. Follow along the slides on making a Telegram bot and APIs: [link](https://docs.google.com/presentation/d/1IedczIb_IedU-NWEnH4qHZCaX985zEsptzePF3b_vHA/edit?usp=sharing).
2. Dive deeper with a specific bot - [PaperBoat](https://github.com/lucafusarbassini/paperboat) - to learn about about OpenAI, LangChain, and scrapping: [link](https://docs.google.com/presentation/d/1Otleuoi5-TfD3YCz1cS0k9MF-Tp7_E0Z/edit?usp=drive_link&ouid=115816041756434628590&rtpof=true&sd=true).

## On IC Cluster (RunAI)

From root of [this repo](https://github.com/epfml/getting-started-lauzhack/?tab=readme-ov-file#4-use-this-repo-to-start-a-llm-training-run-with-your-fork-of-the-llm-baselines-code), create a pod:
```bash
python csub.py -n sandbox
# runai list   # to check the status

# when it is running, connect to pod to be insite a Terminal!
runai exec sandbox -it -- zsh

# clone repo inside home folder
cd /mloscratch/<your_username>
git clone https://github.com/<your username>/apis-telegram.git
cd apis-telegram

# install dependencies
pip install -r requirements.txt
```

Connecting with VScode: https://github.com/epfml/getting-started-lauzhack/?tab=readme-ov-file#using-vscode

Launching bot!
```bash
python3 telegram_gpt.py
```
