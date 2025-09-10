from faster_whisper import WhisperModel
from utils.logging.logger import Logger

logger = Logger().get_logger()

class Transcriber:
    def __init__(self,model_name, device, computer_type, language):
        logger.info('Converter started')
        self.MODEL_NAME = model_name
        self.DEVICE = device
        self.COMPUTER_TYPE = computer_type
        self.LANGUAGE = language

        try:
            self.whisper_model = WhisperModel(self.MODEL_NAME, device=self.DEVICE, compute_type=self.COMPUTER_TYPE)
            logger.info('connection to Whisper Model successful')
        except Exception as e:
            logger.error(f'Whisper model connection failed: {e}')

    def transcribe(self,audio_file_path, beam_size : int=5):
        try:
            segments, info = self.whisper_model.transcribe(audio_file_path, language=self.LANGUAGE, beam_size=beam_size, vad_filter=True)
            logger.info('Whisper model transcription successful')
            text = ''
            for segment in segments:
                text += segment.text
            return text
        except Exception as e:
            logger.error(f'Whisper model transcription failed: {e}')


