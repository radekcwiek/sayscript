import tempfile
from pathlib import Path

from faster_whisper import WhisperModel
from scipy.io.wavfile import write


class SpeechTranscriber:
    def __init__(
        self,
        model_size: str = "medium",
        sample_rate: int = 16000,
        device: str = "cpu",
        compute_type: str = "int8",
        beam_size: int = 10,
    ):
        self.model_size = model_size
        self.sample_rate = sample_rate
        self.device = device
        self.compute_type = compute_type
        self.beam_size = beam_size
        self.model = None

    def load_model(self) -> None:
        if self.model is None:
            self.model = WhisperModel(
                self.model_size,
                device=self.device,
                compute_type=self.compute_type,
            )

    def transcribe_audio(self, audio_data) -> str:
        if audio_data is None:
            return ""

        self.load_model()

        with tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False,
        ) as temp_file:
            temp_path = Path(temp_file.name)

        try:
            write(temp_path, self.sample_rate, audio_data)

            segments, info = self.model.transcribe(
                str(temp_path),
                language="de",
                beam_size=self.beam_size,
                initial_prompt=(
                    "Dies ist ein deutscher diktierter Text für eine Textverarbeitung. "
                    "Achte auf korrekte deutsche Rechtschreibung, Umlaute und sinnvolle Wörter."
                ),
            )

            full_text = ""

            for segment in segments:
                full_text += segment.text

            return full_text.strip()

        finally:
            try:
                temp_path.unlink(missing_ok=True)
            except OSError:
                pass
