from gtts import gTTS
from pydub import AudioSegment
import os

# Step 1: Load input text from file
with open("sample.txt", "r", encoding="utf-8") as file:
    text = file.read().strip()

# Step 2: Convert text to speech and save as MP3
tts = gTTS(text)
tts.save("original.mp3")
print("✅ Original speech saved as original.mp3")

# Step 3: Load MP3 audio into AudioSegment
sound = AudioSegment.from_file("original.mp3", format="mp3")

# Export original as WAV too (for consistency)
sound.export("original.wav", format="wav")
print("✅ Original speech also saved as original.wav")


# === EFFECT FUNCTIONS === #

def pitch_shift(sound, semitones=4):
    """Shifts pitch up or down by semitones."""
    new_sample_rate = int(sound.frame_rate * (2.0 ** (semitones / 12.0)))
    shifted = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
    return shifted.set_frame_rate(sound.frame_rate)

def echo(sound, delay=250, repeat=2):
    """Applies echo by overlaying delayed and softened copies of the original sound."""
    combined = sound
    for i in range(1, repeat + 1):
        # Create silence for delay
        silence = AudioSegment.silent(duration=i * delay)
        # Reduce volume of echo
        softer = sound - (10 * i)
        # Append silence before the softened sound
        echoed = silence + softer
        # Overlay on top of the original
        combined = combined.overlay(echoed)
    return combined


def speed_change(sound, speed=1.5):
    """Changes speed of audio (1.0 = normal, >1.0 = faster)."""
    new_frame_rate = int(sound.frame_rate * speed)
    faster = sound._spawn(sound.raw_data, overrides={'frame_rate': new_frame_rate})
    return faster.set_frame_rate(sound.frame_rate)

def apply_effect(effect_choice, sound):
    if effect_choice == "1":
        return pitch_shift(sound, semitones=4)
    elif effect_choice == "2":
        return echo(sound, delay=250, repeat=3)
    elif effect_choice == "3":
        return speed_change(sound, speed=1.5)
    else:
        print("❌ Invalid choice. No effect applied.")
        return sound

# === USER CHOICE === #
print("\n🎛 Choose an audio effect to apply:")
print("1: Pitch Shift (+4 semitones)")
print("2: Echo Effect")
print("3: Speed Up (1.5x)")
effect_choice = input("Enter your choice (1/2/3): ").strip()

# === APPLY CHOSEN EFFECT === #
modified = apply_effect(effect_choice, sound)
modified.export("modified.wav", format="wav")
print("✅ Modified audio saved as modified.wav")
