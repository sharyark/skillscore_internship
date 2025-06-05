import os
import pretty_midi
import pandas as pd

MIDI_FOLDER = "MIDI_FOLDER"  # Replace with your MIDI files directory
OUTPUT_CSV  = "features.csv"

# Create an empty list to collect feature dictionaries
all_features = []

# Iterate over each .mid file in midi_data/
for filename in os.listdir(MIDI_FOLDER):
    if not filename.lower().endswith((".mid", ".midi")):
        continue
    filepath = os.path.join(MIDI_FOLDER, filename)
    
    # Load MIDI file using pretty_midi
    try:
        midi_data = pretty_midi.PrettyMIDI(filepath)
    except Exception as e:
        print(f"⚠️ Could not parse {filename}: {e}")
        continue

    # Iterate over each instrument track (e.g., piano, strings)
    for instrument in midi_data.instruments:
        # Skip drum tracks if desired: if instrument.is_drum: continue
        for note in instrument.notes:
            feature = {
                "midi_file": filename,
                "instrument": instrument.program,      # MIDI program number
                "note_pitch": note.pitch,             # 0–127
                "start_time": note.start,             # in seconds
                "end_time": note.end,                 # in seconds
                "duration": note.end - note.start,     # in seconds
                "velocity": note.velocity             # 0–127
            }
            all_features.append(feature)

# Convert to DataFrame and save as CSV
df = pd.DataFrame(all_features)
df.to_csv(OUTPUT_CSV, index=False)
print(f"✅ Extracted features saved to {OUTPUT_CSV}")
