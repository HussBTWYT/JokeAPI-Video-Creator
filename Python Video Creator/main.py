import os
import random
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, concatenate_audioclips, AudioFileClip
import requests
import json
import re
import pyttsx3

# API connection for jokes part
jokes = {}

for i in range(3):
    url = "https://hussbtwjokesapi.pythonanywhere.com/api/randomjoke"
    params = "joke"

    response = requests.get(url, params)

    data = json.loads(response.text)

    result = data["joke"]

    jokes[i + 1] = result

def save_audio(text, filename):
    engine = pyttsx3.init()
    engine.save_to_file(text, filename)
    engine.runAndWait()

def save_jokes_to_txt(jokes, output_path):
    with open(os.path.join(output_path, "jokes.txt"), "w") as file:
        for joke_number, joke_text in jokes.items():
            file.write(f"Joke {int(joke_number)}: {joke_text}\n")

def create_video(output_path, background_path, text_durations):
    try:
        # Load the background video
        background_clip = VideoFileClip(background_path)

        # Get the duration of the background video
        background_duration = background_clip.duration

        # Get a random start time within the video duration for a 30-second subclip
        start_time = random.uniform(0, background_duration - 30)

        # Extract a 30-second subclip of the background video
        background_subclip = background_clip.subclip(start_time, start_time + 30)

        # Mute the audio of the background subclip
        background_subclip = background_subclip.set_audio(None)

        # List to store TextClips
        text_clips = []

        # List to store AudioClips
        audio_clips = []

        # A variable to keep track of the current time in the video
        current_time = 0

        # A constant to define the initial delay between each line of the joke
        initial_delay = 0.25

        # Define the gap duration between lines
        line_gap = 2.00

        # Loop through each text duration tuple
        for text, _, duration in text_durations:
            # Split the text by punctuation marks followed by a space
            lines = re.split(r"[.?!]\s", text)

            # Create a text clip with the joke number and the start time
            joke_number = f"Joke {int(current_time // 5) + 1}:"
            joke_number_audio_file = f"joke_number_{int(current_time // 5) + 1}.wav"
            save_audio(joke_number, joke_number_audio_file)
            joke_number_audio_clip = AudioFileClip(joke_number_audio_file).set_start(current_time + initial_delay)

            # Append the joke number audio clip to the list
            audio_clips.append(joke_number_audio_clip)

            # Loop through each line and its duration
            for line in lines:
                # Create a text clip with the line and a smaller fontsize
                txt_clip = TextClip(line, fontsize=20, color='white')

                # Calculate the delay dynamically based on the duration of the previous audio clip and the gap
                delay = max(initial_delay, joke_number_audio_clip.duration * 0.1) + line_gap

                # Set the position to center, start time, and duration
                txt_clip = txt_clip.set_pos('center').set_start(current_time + delay).set_duration(duration)

                # Append the text clip to the list
                text_clips.append(txt_clip)

                # Save line audio to file
                line_audio_file = f"line_{int(current_time + delay)}.wav"
                save_audio(line, line_audio_file)

                # Load line audio clip
                line_audio_clip = AudioFileClip(line_audio_file).set_start(current_time + delay)

                # Append the line audio clip to the list
                audio_clips.append(line_audio_clip)

                # Update the current time by adding the duration of the line audio clip
                current_time += line_audio_clip.duration

            # Add a gap before the next joke
            current_time += line_gap

        # Reset current_time to 0 for the next joke
        current_time = 0

        # Overlay the text clips on the background subclip
        final_clip = CompositeVideoClip([background_subclip] + text_clips)

        # Concatenate the audio clips
        final_audio = concatenate_audioclips(audio_clips)

        # Set the audio of the final clip to the concatenated audio
        final_clip = final_clip.set_audio(final_audio)

        # Write the result to a file
        output_file_name = "output_video.mp4"
        output_file_path = os.path.join(output_path, output_file_name)
        i = 1
        while os.path.exists(output_file_path):
            output_file_name = f"output_video{i}.mp4"
            output_file_path = os.path.join(output_path, output_file_name)
            i += 1
        final_clip.write_videofile(output_file_path, codec="libx264", audio_codec="aac", fps=60)

        print(f"Video successfully created at {output_file_path}")

        # Save jokes to a text file
        save_jokes_to_txt(jokes, output_path)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Clean up audio files
        for file in os.listdir():
            if file.endswith(".wav"):
                os.remove(file)

if __name__ == "__main__":
    # Define a list of text, start time, and duration tuples
    text_durations = [(f"{jokes[1]}", 0, 5), (f"{jokes[2]}", 5, 8), (f"{jokes[3]}", 13, 6)]

    # Set the paths for the background video and output directory
    background_video_path = r"your/path/to/minecraft_background.mp4"
    output_video_directory = r"your/path/to/Outputted Videos"

    # Create the video with the specified parameters
    create_video(output_video_directory, background_video_path, text_durations)

