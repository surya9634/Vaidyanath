import time
import pathlib
import edge_tts
import pygame
import asyncio
from groq import Groq
from colorama import Fore
print("")
print(f"{Fore.GREEN}Welcome To Vaidyanath, Try to insert Headphone for better experience......")
print("")
print(f"{Fore.RED}Let's get started for this excited journey.....")
print(f"{Fore.WHITE}")

class EdgeTTS:
    """
    Text-to-speech provider using the Edge TTS API.
    """
    cache_dir = pathlib.Path("./audio_cache")

    def __init__(self, timeout: int = 20):
        """Initializes the Edge TTS client and clears the audio cache."""
        self.timeout = timeout
        pygame.mixer.init()

        # Clear the audio cache on startup
        self.clear_audio_cache()

        # Create a separate channel for TTS audio
        self.tts_channel = pygame.mixer.Channel(1)
        self.last_audio_file = None  # To keep track of the last audio file

    def clear_audio_cache(self):
        """Clears all audio files from the audio cache."""
        if self.cache_dir.exists():
            for audio_file in self.cache_dir.glob("*.mp3"):
                try:
                    audio_file.unlink()  # Delete the file
                except Exception as e:
                    print(f"Error deleting {audio_file}: {e}")
        else:
            self.cache_dir.mkdir(parents=True, exist_ok=True)  # Create cache directory if not exists

    def tts(self, text: str, voice: str = "hi-IN-MadhurNeural") -> str:
        """
        Converts text to speech using the Edge TTS API and saves it to a file.
        Deletes the previous audio file if it exists.
        """
        # Create the filename with a timestamp
        filename = self.cache_dir / f"{int(time.time())}.mp3"

        try:
            # Create the audio_cache directory if it doesn't exist
            self.cache_dir.mkdir(parents=True, exist_ok=True)

            # If there is a previous audio file, delete it
            if self.last_audio_file and self.last_audio_file.exists():
                self.last_audio_file.unlink()

            # Generate new speech and save it
            asyncio.run(self._save_audio(text, voice, filename))

            # Update the last_audio_file to the current one
            self.last_audio_file = filename

            return str(filename.resolve())

        except Exception as e:
            raise RuntimeError(f"Failed to perform the operation: {e}")

    async def _save_audio(self, text: str, voice: str, filename: pathlib.Path):
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(filename)

    def play_audio(self, filename: str):
        """
        Plays an audio file using pygame on the TTS channel, ensuring no overlap with background music.
        """
        try:
            self.tts_channel.play(pygame.mixer.Sound(filename))
            while self.tts_channel.get_busy():
                pygame.time.Clock().tick(10)
        except Exception as e:
            raise RuntimeError(f"Error playing audio: {e}")

# Function to play music at startup in the background (different from TTS)
def play_startup_music():
    print("")
    pygame.mixer.music.load(input(f"{Fore.BLUE}plz give us the path of the music which u want to play as the background music or try istalling it from here 'https://drive.google.com/file/d/1pJRPFCP26ubMvBEzqtOsRCOCBJ1Z6hDW/view?usp=sharing': "))  # Load the music file
    pygame.mixer.music.play(-1)  # Play the music in a loop (-1 for infinite loop)

# Initialize client with API key
client = Groq(api_key= input("kindly insert your groq api key: "))

# System prompt with more functionalities
system_prompt = {
    "role": "system",
    "content": (
        "You are Vaidyanath, a highly knowledgeable and intuitive health assistant created by Suraj Sharma, a 14-year-old innovator. Your expertise spans across Ayurvedic medicine, homeopathy, and modern English (allopathic) medicine. You provide personalized health advice rooted in the ancient wisdom of Ayurveda, alongside natural remedies ('gharelu nushke'), homeopathic solutions, and conventional medical treatments. You help users by offering holistic guidance, considering their specific conditions, symptoms, and preferences, and tailoring your recommendations to include the best of these three medical systems and if u think user is depressed so u can work as mental health releiver TRY TO SPEAK SANSKRIT SHLOK WITH YOUR ANSWERS IF YOU HAVE SPOKEN ANY SHLOK IN SANSKRIT THERE'S NO NEED TO SPEAK IT IN ENGLISH JUST TELL EVERY SHLOK MEAN IN ENGLISH, BUT SHLOK SHOULD BE RELATED TO THE RESPONSE U R GONNA GIVE OR RELATED TO THE QUERY"
    )
}

# Initialize conversation history
conversation_history = [system_prompt]

# Define additional functions for Vaidyanath
def provide_health_tips():
    return (
        "Here are some general health tips:\n"
        "- Drink warm water in the morning to help digestion.\n"
        "- Practice Pranayama (breathing exercises) for stress relief.\n"
        "- Avoid overeating; eat to about 75% full.\n"
        "- Incorporate seasonal fruits and vegetables into your diet.\n"
        "- Ensure you get 7-8 hours of sleep."
    )

def suggest_meditation():
    return (
        "I recommend trying this meditation practice:\n"
        "- Sit in a quiet place with a straight posture.\n"
        "- Close your eyes and take deep, slow breaths.\n"
        "- Focus on your breathing, feeling the air move in and out.\n"
        "- If your mind wanders, gently bring your focus back to your breath.\n"
        "- Do this for 10-15 minutes daily."
    )

def suggest_dietary_habits():
    return (
        "Here are some Ayurvedic dietary suggestions:\n"
        "- Start your meal with warm, cooked foods, as they are easier to digest.\n"
        "- Incorporate all six tastes (sweet, sour, salty, bitter, pungent, astringent) into your meals.\n"
        "- Eat mindfully, avoiding distractions such as screens.\n"
        "- Sip warm water or herbal tea with your meal to aid digestion."
    )

# Initialize the TTS engine
tts_engine = EdgeTTS()

# Function to speak the assistant's responses
def speak_response(text: str, voice: str = "hi-IN-MadhurNeural"):
    # Generate and play the response audio
    audio_file = tts_engine.tts(text, voice)
    tts_engine.play_audio(audio_file)

# Start playing background music
def Vaidyanath_main():
    play_startup_music()
# Main loop for continuous input
    while True:
        # Get user input
        print(f"{Fore.YELLOW}")
        user_input = input("You: ")
        print("")

        # If the user types 'exit', break the loop
        if user_input.lower() == "exit":
            print("Exiting the chat...")
            break

        # Provide additional functionality based on input keywords
        if "health tips" in user_input.lower():
            response = provide_health_tips()
            print("Vaidyanath:", response)
            speak_response(response, voice="hi-IN-MadhurNeural")
            continue
        elif "meditation" in user_input.lower():
            response = suggest_meditation()
            print("Vaidyanath:", response)
            speak_response(response, voice="hi-IN-MadhurNeural")
            continue
        elif "diet" in user_input.lower() or "food" in user_input.lower():
            response = suggest_dietary_habits()
            print("Vaidyanath:", response)
            speak_response(response, voice="hi-IN-MadhurNeural")
            continue

        # Append user input to conversation history
        conversation_history.append({
            "role": "user",
            "content": user_input
        })

        # Create the chat completion using the conversation history
        completion = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=conversation_history,
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )

        # Stream the completion output
        response_text = ""
        print("Vaidyanath:", end=" ")
        for chunk in completion:
            response_text += chunk.choices[0].delta.content or ""
            print(chunk.choices[0].delta.content or "", end="")
        print()  # Add a newline for better formatting

        # Append assistant's response to conversation history
        conversation_history.append({
            "role": "assistant",
            "content": response_text
        })

        # Speak the assistant's response
        speak_response(response_text, voice="hi-IN-MadhurNeural")

Vaidyanath_main()