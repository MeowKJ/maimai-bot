import string


class Base62Encoder:
    ALPHABET = string.digits + string.ascii_letters
    BASE = 62

    @staticmethod
    def encode_number(n):
        if isinstance(n, str):
            # 尝试将字符串转换为整数
            n = int(n)
        if n == 0:
            return Base62Encoder.ALPHABET[0]
        result = ""
        while n:
            n, rem = divmod(n, Base62Encoder.BASE)
            result = Base62Encoder.ALPHABET[rem] + result
        return result

    @staticmethod
    def encode_string(s):
        encoded_str = ""
        for char in s:
            encoded_str += Base62Encoder.encode_number(ord(char))
        return encoded_str

    @staticmethod
    def decode(encoded_str):
        number = 0
        for char in encoded_str:
            number = number * Base62Encoder.BASE + Base62Encoder.ALPHABET.index(char)
        return number
