# AI-Enabled Bot with APIs and Telegram, [SLIDES](https://go.epfl.ch/telegram-apis)

This tutorial has been given at multiple LauzHack events:
- [Mini-hackathon](https://lu.ma/lauzhack-apis-2023) (Nov 11, 2023).
- [Mini-hackathon](https://lu.ma/lauzhack-llms-apis) (Apr 19-20, 2024), projects that used it can be found [here](https://lauzhack-llms-genai-2024.devpost.com/submissions/search?utf8=%E2%9C%93&prize_filter%5Bprizes%5D%5B%5D=76173).
- [Mini-hackathon](https://lu.ma/6k75ky9t) (May 16-17, 2025), six of [the projects](https://lauzhack-llms-multimodal-2025.devpost.com/project-gallery) used it.

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

## [Old instructions] EPFL IC Cluster (RunAI)

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
