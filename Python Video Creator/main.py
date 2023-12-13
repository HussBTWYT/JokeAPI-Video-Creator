import os
import random
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, concatenate_audioclips, AudioFileClip
import requests
import json
import pyttsx3

# API connection for jokes part
jokes = {}

# Get three jokes from the API
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

def create_video_smooth_subtitles(output_path, background_path, text_durations):
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

        # List to store AudioClips for smooth subtitles
        smooth_audio_clips = []

        # A variable to keep track of the current time in the video
        current_time = 0

        # A constant to define the initial delay between each line of the joke
        initial_delay = 0.80

        # Define the gap duration between lines
        line_gap = 0.5

        # Loop through each text duration tuple
        for text, start_time, duration in text_durations:
            # Save part audio to file
            part_audio_file = f"part_{int(start_time)}.wav"
            save_audio(text, part_audio_file)

            # Load part audio clip
            part_audio_clip = AudioFileClip(part_audio_file)

            # Update the last element of the tuple to the adjusted duration
            adjusted_duration = part_audio_clip.duration - 0.75
            text_durations[text_durations.index((text, start_time, duration))] = (text, start_time, adjusted_duration)

            # Append the part audio clip to the list
            smooth_audio_clips.append(part_audio_clip)

            # Create a TextClip for each joke
            txt_clip_part = TextClip(text, fontsize=20, color='white')

            # Calculate the delay dynamically based on the duration of the previous audio clip and the gap
            delay = current_time + initial_delay

            # Adjust the delay by subtracting 1.75 for synchronization
            adjusted_delay = delay - 1.75

            # Set the position to center, start time, and duration
            txt_clip_part = txt_clip_part.set_pos('center').set_start(adjusted_delay).set_duration(adjusted_duration)

            # Append the text clip to the list
            text_clips.append(txt_clip_part)

            # Update the current time by adding the duration of the part audio clip and the gap
            current_time += adjusted_duration + line_gap


        # Concatenate the audio clips for smooth subtitles
        smooth_final_audio = concatenate_audioclips(smooth_audio_clips)

        # Overlay the text clips on the background subclip
        final_clip = CompositeVideoClip([background_subclip] + text_clips)

        # Set the audio of the final clip to the concatenated audio for smooth subtitles
        final_clip = final_clip.set_audio(smooth_final_audio)

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
            if file.startswith("part_") and file.endswith(".wav"):
                os.remove(file)

if __name__ == "__main__":
    # Use the three jokes for text durations
    text_durations = [
        (f"{jokes[1]}", 0, 7),
        (f"{jokes[2]}", 4, 5),
        (f"{jokes[3]}", 8, 6)
    ]

    # Set the paths for the background video and output directory
    background_video_path = r"your\path\to\minecraft_background.mp4"
    output_video_directory = r"your\path\to\Outputted Videos"

    # Create the video with smooth subtitles
    create_video_smooth_subtitles(output_video_directory, background_video_path, text_durations)
