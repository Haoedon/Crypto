alphabet = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

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
        self.state = [1] * length

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

# Вставьте ваш начальный ключ (19 бит)
initial_key = [1,0,1,1,0,1,0,1,1,0,0,1,1,0,1,0,1,1,0]

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

# Вставьте зашифрованные биты (строка из 0 и 1)
cipher_bits_str = "..."  # Например: "101010001110..."
cipher_bits = [int(b) for b in cipher_bits_str]

# Генерируем ключевой поток
keystream = [a5_1_step() for _ in range(len(cipher_bits))]

# Расшифровка
plain_bits = [c ^ k for c, k in zip(cipher_bits, keystream)]
plain_text = bits_to_text(plain_bits)

print("Расшифрованный текст:", plain_text)