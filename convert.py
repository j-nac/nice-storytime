import os
import sys

import soundfile as sf
from kokoro import KPipeline


def text_to_speech(input_file):
    # Check if file exists
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    # Initialize the pipeline (lang_code 'a' = American English)
    # It will automatically attempt to use the GPU if CUDA is available
    pipeline = KPipeline(lang_code="a")

    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Generate audio.
    # generator yields (graphemes, phonemes, audio_tensor)
    generator = pipeline(content, voice="bm_daniel", speed=1.0)

    all_audio = []
    for i, (gs, ps, audio) in enumerate(generator):
        all_audio.append(audio)

    # Combine and save
    import numpy as np

    final_audio = np.concatenate(all_audio)
    output_name = os.path.splitext(input_file)[0] + ".wav"

    sf.write(output_name, final_audio, 24000)
    print(f"Success! Saved to {output_name}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python convert.py <your_file.txt>")
    else:
        text_to_speech(sys.argv[1])
