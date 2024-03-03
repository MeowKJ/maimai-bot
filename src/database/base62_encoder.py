# base62_encoder.py - Base62 encoder and decoder
import string


class Base62Encoder:
    ALPHABET = string.digits + string.ascii_letters
    BASE = 62

    @staticmethod
    def encode(number):
        if isinstance(number, str):
            # 尝试将字符串转换为整数
            try:
                number = int(number)
            except ValueError as exc:
                raise ValueError("Base62 encoding expects a numeric input.") from exc

        if number == 0:
            return Base62Encoder.ALPHABET[0]
        result = ""
        while number:
            number, rem = divmod(number, Base62Encoder.BASE)
            result = Base62Encoder.ALPHABET[rem] + result
        return result

    @staticmethod
    def decode(encoded_str):
        number = 0
        for char in encoded_str:
            number = number * Base62Encoder.BASE + Base62Encoder.ALPHABET.index(char)
        return number
