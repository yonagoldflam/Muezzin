from faster_whisper import WhisperModel

class Converter:
    def __init__(self,audio_file_path ,model_name, device, computer_type, language):
        self.AUDIO_FILE = audio_file_path
        self.MODEL_NAME = model_name
        self.DEVICE = device
        self.COMPUTER_TYPE = computer_type
        self.LANGUAGE = language

        self.whisper_model = WhisperModel("distil-large-v3", device="cpu", compute_type="int8")

    def transcribe(self, beam_size : int=5):
        segments, info = self.whisper_model.transcribe(self.AUDIO_FILE, language=self.LANGUAGE, beam_size=beam_size, vad_filter=True)
        text = {}
        for segment in segments:
            time = f"[{segment.start:.2f}] -> [{segment.end:.2f}]"
            text[time] = segment.text
        return text

