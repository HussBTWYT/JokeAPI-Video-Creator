[![Python]](https://www.python.org/)

# Package Installation

- Install Python requirements `pip install -r requirements.txt`

# To see examples of this system

If you would like to see some examples [*again please note that these are in beta and have a* **variety of problems** *so please submit a pull request to contribute to this project to fix errors*] go to the repository, and go inside > Example Videos > *variety of example videos*

**May I repeat, please submit a pull request to contribute to this project to fix errors as there are a variety of them, which I could not fix by myself.**

# Functionality of the Video Creator

The video creator uses my API [JokeAPI](github.com/HussBTW/YT/JokeAPI) to create something that resembles a TikTok video, given 3 jokes in the video.

**NOTE: THERE IS SITLL A HUGE VARIETY OF PROBLEMS WITH THIS, AS IN A HIGH BETA VERSION.**

# How To Use

Firstly, clone the repository by the following command: 

```bash
git clone https://github.com/HussBTWYT/JokeAPI-Video-Creator
```

Secondly, Install the Python requirements using `pip install -r requirements.txt`

Then, open command prompt and write the following command:

```bash
python main.py
```

Then, check the directory of **"Outputted Videos"** and you should see your video.

*Note that outputted videos file's name go in order, e.g. output_video.mp4, then output_video1.mp4, then output_video2.mp4 (if output_video.mp4 already exists, this order occurs)*

# API Usage 

## Before I continue, this is only for the actual API, and does not resemble the Video-Creator code.

This is an API hosted on [Flask](https://flask.palletsprojects.com/en/1.1.x/) app that serves a JSON response according to the [randomly generated] joke.

Note that there are multiple use cases of programming languages that can be used here, and is up to you however PYTHON WILL BE THE MAIN, that is why there is a requirements.txt for python only.

To use this API, run the following example script using the requests libary and json libary:

```python
import requests, json

url = "https://hussbtwjokesapi.pythonanywhere.com/api/randomjoke"
params = "joke"

response = requests.get(url, params)

data = json.loads(response.text)

print(data["joke"])
```
