from convert_audio_to_text import Converter


class Manager:
    def __init__(self):
        self.audio_file_path = 'C:/podcasts/download (1).wav'
        self.model_name = 'distil-large-v3'
        self.device = 'cpu'
        self.computer_type = 'int8'
        self.language = 'en'

    def convert(self):
        converter = Converter(audio_file_path=self.audio_file_path, model_name=self.model_name, device=self.device, computer_type=self.computer_type, language=self.language)
        text = converter.transcribe()
        print(text)

if __name__ == '__main__':
    m = Manager()
    m.convert()