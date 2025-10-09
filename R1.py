# Алфавит: только буквы русского алфавита (без пробела, точки, запятой)
alphabet = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

def text_to_bits(text):
    bits = []
    for char in text:
        idx = alphabet.find(char)
        if idx == -1:
            raise ValueError(f"Символ {char} не найден в алфавите")
        bits.extend([int(x) for x in f"{idx:05b}"])  # 5 бит на символ
    return bits

def bits_to_text(bits):
    chars = []
    for i in range(0, len(bits), 5):
        idx = int("".join(str(b) for b in bits[i:i+5]), 2)
        chars.append(alphabet[idx])
    return "".join(chars)

class LFSR:
    def __init__(self, length, taps, sync_bit):
        self.length = length
        self.taps = taps
        self.sync_bit = sync_bit
        self.state = [1] * length  # Можно заменить на произвольное начальное состояние

    def get_sync(self):
        return self.state[self.length - self.sync_bit]

    def get_output(self):
        return self.state[-1]

    def clock(self):
        feedback = 0
        for t in self.taps:
            feedback ^= self.state[self.length - t]
        self.state = [feedback] + self.state[:-1]

def majority(x, y, z):
    return (x & y) | (x & z) | (y & z)

# Пример начального ключа для R1 (19 бит)
initial_key = [1,0,1,1,0,1,0,1,1,0,0,1,1,0,1,0,1,1,0]  # Можно задать свой

# Инициализация регистров
R1 = LFSR(19, [19, 18, 17, 14], 8)
R1.state = initial_key.copy()
R2 = LFSR(22, [22, 21], 10)
R3 = LFSR(23, [23, 22, 21, 8], 10)

def a5_1_step():
    x, y, z = R1.get_sync(), R2.get_sync(), R3.get_sync()
    f = majority(x, y, z)
    if x == f:
        R1.clock()
    if y == f:
        R2.clock()
    if z == f:
        R3.clock()
    return R1.get_output() ^ R2.get_output() ^ R3.get_output()

# Текст для шифрования
text = "ОДИНДУРАКМОЖЕТБОЛЬШЕСПРАШИВАТЬЗПТЧЕМДЕСЯТЬУМНЫХОТВЕТИТЬТЧК"
bits = text_to_bits(text)
keystream = [a5_1_step() for _ in range(len(bits))]
cipher_bits = [b ^ k for b, k in zip(bits, keystream)]

print("Вид скремблера: РСЛОС (R1)")
print("Начальный ключ:", "".join(str(b) for b in initial_key))
print("Зашифрованные биты:", "".join(str(b) for b in cipher_bits))