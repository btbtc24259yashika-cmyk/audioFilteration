from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import numpy as np
import soundfile as sf
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter
import time

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# ------------------------
# Simple DSP noise filter
# ------------------------

def bandpass_filter(data, sr, low=300, high=3400):

    nyq = 0.5 * sr
    low = low / nyq
    high = high / nyq

    b, a = butter(4, [low, high], btype='band')
    return lfilter(b, a, data)


def rms(x):
    return np.sqrt(np.mean(x**2))


def snr(clean, noise):
    return 20 * np.log10(rms(clean) / (rms(noise) + 1e-6))


# ------------------------
# Routes
# ------------------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/test")
def test():
    return jsonify({"status": "ok"})


@app.route("/process", methods=["POST"])
def process_audio():

    try:

        file = request.files["audio"]

        ts = int(time.time())

        input_path = os.path.join(UPLOAD_FOLDER, f"in_{ts}.webm")
        wav_path = os.path.join(UPLOAD_FOLDER, f"in_{ts}.wav")

        file.save(input_path)

        # convert using ffmpeg
        os.system(f'ffmpeg -y -i "{input_path}" "{wav_path}"')

        audio, sr = sf.read(wav_path)

        if len(audio.shape) > 1:
            audio = audio[:, 0]

        cleaned = bandpass_filter(audio, sr)

        noise = audio - cleaned

        orig_rms = float(rms(audio))
        clean_rms = float(rms(cleaned))
        noise_rms = float(rms(noise))
        snr_val = float(snr(cleaned, noise))

        out_audio = os.path.join(OUTPUT_FOLDER, f"cleaned_{ts}.wav")
        out_graph = os.path.join(OUTPUT_FOLDER, f"graph_{ts}.png")

        sf.write(out_audio, cleaned, sr)

        # graph
        plt.figure(figsize=(8,3))
        plt.plot(audio, alpha=0.5)
        plt.plot(cleaned, alpha=0.7)
        plt.savefig(out_graph)
        plt.close()

        return jsonify({

            "success": True,
            "audio": f"/outputs/cleaned_{ts}.wav",
            "graph": f"/outputs/graph_{ts}.png",
            "snr": round(snr_val,2),

            "original_rms": round(orig_rms,4),
            "cleaned_rms": round(clean_rms,4),
            "noise_rms": round(noise_rms,4),
            "sample_rate": sr

        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@app.route("/outputs/<path:filename>")
def outputs(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)