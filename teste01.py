# 🎵 Detector de acordes em tempo real com interface gráfica
# -------------------------------------------------------
# Instale:
# pip install librosa numpy sounddevice

import tkinter as tk
import numpy as np
import librosa
import sounddevice as sd
import threading

SR = 22050
DURATION = 3  # segundos por análise

NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F',
         'F#', 'G', 'G#', 'A', 'A#', 'B']

# Templates simples de acordes maiores e menores
CHORD_TEMPLATES = {}

for i, note in enumerate(NOTES):
    major = np.zeros(12)
    minor = np.zeros(12)

    major[i] = 1
    major[(i + 4) % 12] = 1
    major[(i + 7) % 12] = 1

    minor[i] = 1
    minor[(i + 3) % 12] = 1
    minor[(i + 7) % 12] = 1

    CHORD_TEMPLATES[note + ""] = major
    CHORD_TEMPLATES[note + "m"] = minor


def record_audio():
    audio = sd.rec(int(DURATION * SR), samplerate=SR, channels=1)
    sd.wait()
    return audio.flatten()


def detect_chord(y):
    chroma = librosa.feature.chroma_stft(y=y, sr=SR)
    chroma_mean = np.mean(chroma, axis=1)

    norm = np.linalg.norm(chroma_mean)
    if norm == 0:
        return "Silêncio"

    chroma_mean = chroma_mean / norm

    best_match = None
    max_score = -np.inf

    for chord, template in CHORD_TEMPLATES.items():
        score = np.dot(chroma_mean, template)
        if score > max_score:
            max_score = score
            best_match = chord

    return best_match


def infer_key(chords):
    # regra simples baseada em frequência
    counts = {}
    for c in chords:
        root = c.replace("m", "")
        counts[root] = counts.get(root, 0) + 1

    key = max(counts, key=counts.get)
    return key + " Maior"


def harmonic_field(key):
    note = key.split()[0]
    idx = NOTES.index(note)
    intervals = [0, 2, 4, 5, 7, 9, 11]
    degrees = ['I', 'ii', 'iii', 'IV', 'V', 'vi', 'vii°']

    result = []
    for i, interval in enumerate(intervals):
        n = NOTES[(idx + interval) % 12]
        result.append(f"{n} ({degrees[i]})")

    return result


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Detector Harmônico")
        self.chords = []

        self.label = tk.Label(
            root, text="Clique em iniciar", font=("Arial", 16))
        self.label.pack(pady=20)

        self.btn = tk.Button(root, text="Iniciar", command=self.start)
        self.btn.pack(pady=10)

        self.result = tk.Label(root, text="", font=("Arial", 12))
        self.result.pack(pady=20)

    def start(self):
        threading.Thread(target=self.process).start()

    def process(self):
        self.chords = []
        for i in range(4):
            self.label.config(text=f"Gravando acorde {i+1}...")
            audio = record_audio()
            chord = detect_chord(audio)
            self.chords.append(chord)
            self.label.config(text=f"Detectado: {chord}")
            self.root.update()

        key = infer_key(self.chords)
        field = harmonic_field(key)

        result_text = f"Acordes: {self.chords}\n\nTom: {key}\n\nCampo harmônico:\n"
        result_text += "\n".join(field)

        self.result.config(text=result_text)
        self.label.config(text="Finalizado")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
