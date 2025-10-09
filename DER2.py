alphabet = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

def bits_to_text(bits):
    chars = []
    for i in range(0, len(bits), 5):
        idx = int("".join(str(b) for b in bits[i:i+5]), 2)
        chars.append(alphabet[idx])
    return "".join(chars)

class LFSR:
    def __init__(self, length, taps, initial_state=None):
        self.length = length
        self.taps = taps
        if initial_state is not None:
            if len(initial_state) != length:
                raise ValueError("Длина начального ключа не совпадает с длиной регистра")
            self.state = initial_state.copy()
        else:
            self.state = [1] * length

    def get_output(self):
        return self.state[-1]

    def clock(self):
        feedback = 0
        for t in self.taps:
            feedback ^= self.state[self.length - t]
        self.state = [feedback] + self.state[:-1]

# Ваш начальный ключ для R2 (22 бита)
initial_key_R2 = [1,0,1,1,0,1,0,1,1,0,0,1,1,0,1,0,1,1,0,1,0,1]  # пример

# Зашифрованные биты (строка из 0 и 1, замените на свои)
cipher_bits_str = "101010001110..."  # вставьте свою строку
cipher_bits = [int(b) for b in cipher_bits_str]

def decrypt_r2(cipher_bits, initial_key):
    reg = LFSR(22, [22, 21], initial_key)
    keystream = []
    for _ in range(len(cipher_bits)):
        keystream.append(reg.get_output())
        reg.clock()
    plain_bits = [c ^ k for c, k in zip(cipher_bits, keystream)]
    return bits_to_text(plain_bits)

# Расшифровка
decrypted_text = decrypt_r2(cipher_bits, initial_key_R2)
print("Расшифрованный текст:", decrypted_text)