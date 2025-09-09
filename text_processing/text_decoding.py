import base64

class TextDecoding:

    @staticmethod
    def decode_base64(encoded_string):
        encoded_bytes = encoded_string.encode('ascii')
        decoded_string = base64.b64decode(encoded_bytes).decode('utf-8')
        return decoded_string
