# SPDX-License-Identifier: Apache-2.0

"""
Microphone recording helper for SayScript.

AudioRecorder captures microphone input through sounddevice and returns the
recorded samples as a NumPy array. It does not perform transcription itself.
Transcription is handled separately by the speech transcriber/worker modules.
"""

import numpy as np
import sounddevice as sd

from app.logging_setup import get_logger


class AudioRecorder:
    """
    Record mono microphone audio into memory.

    The recorder uses an InputStream callback. Each callback receives a small
    audio block, copies it, and appends it to ``self.frames``. When recording
    stops, all frames are concatenated into one NumPy array.
    """

    def __init__(self, sample_rate: int = 16000):
        self.sample_rate = sample_rate
        self.stream = None
        self.frames = []
        self.logger = get_logger()

    def start(self) -> None:
        """
        Start recording from the default input device.

        Existing frames are cleared before a new recording starts.
        """
        self.frames = []

        def callback(indata, frames, time, status):
            """
            Store one audio block from sounddevice.

            The callback arguments are defined by sounddevice. ``frames`` and
            ``time`` are not needed here, but they must remain part of the
            callback signature.
            """
            if status:
                self.logger.warning("Audio input status: %s", status)

            self.frames.append(indata.copy())

        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            dtype="int16",
            callback=callback,
        )
        self.stream.start()

        self.logger.info("Audio recording started")

    def stop(self):
        """
        Stop recording and return the recorded audio samples.

        Returns None if recording was not active or if no audio frames were
        captured.
        """
        if self.stream is None:
            return None

        self.stream.stop()
        self.stream.close()
        self.stream = None

        if not self.frames:
            self.logger.warning("Audio recording stopped without captured frames")
            return None

        audio = np.concatenate(self.frames, axis=0)

        self.logger.info("Audio recording stopped: %s samples", len(audio))

        return audio
