alphabet = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

def text_to_bits(text):
    bits = []
    for char in text:
        idx = alphabet.find(char)
        if idx == -1:
            raise ValueError(f"Символ {char} не найден в алфавите")
        bits.extend([int(x) for x in f"{idx:05b}"])
    return bits

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

# Укажите свой начальный ключ для второго регистра (22 бита):
initial_key_R2 = [1,0,1,1,0,1,0,1,1,0,0,1,1,0,1,0,1,1,0,1,0,1]  # Пример
R2 = LFSR(22, [22, 21], initial_key_R2)

# Функция генерации ключевого потока только с использованием второго регистра
def r2_stream_step():
    out = R2.get_output()
    R2.clock()
    return out

# Пример шифрования текста только вторым регистром
text = "ОДИНДУРАКМОЖЕТБОЛЬШЕСПРАШИВАТЬЗПТЧЕМДЕСЯТЬУМНЫХОТВЕТИТЬТЧК"
bits = text_to_bits(text)
keystream = [r2_stream_step() for _ in range(len(bits))]
cipher_bits = [b ^ k for b, k in zip(bits, keystream)]

print("Вид скремблера: R2 (X22 + X21 + 1)")
print("Начальный ключ:", "".join(str(b) for b in initial_key_R2))
print("Зашифрованные биты:", "".join(str(b) for b in cipher_bits))