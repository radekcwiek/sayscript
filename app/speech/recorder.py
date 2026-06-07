import sounddevice as sd
import numpy as np


class AudioRecorder:
    def __init__(self, sample_rate: int = 16000):
        self.sample_rate = sample_rate
        self.recording = None
        self.stream = None
        self.frames = []

    def start(self) -> None:
        self.frames = []

        def callback(indata, frames, time, status):
            if status:
                print(f"Audio status: {status}")

            self.frames.append(indata.copy())

        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            dtype="int16",
            callback=callback,
        )
        self.stream.start()

    def stop(self):
        if self.stream is None:
            return None

        self.stream.stop()
        self.stream.close()
        self.stream = None

        if not self.frames:
            return None

        return np.concatenate(self.frames, axis=0)
