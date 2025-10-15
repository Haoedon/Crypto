alphabet = "яабвгдежзийклмнопрстуфхцчшщъыьэю"[:32]  # 32 символа

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

def lfsr(seed, taps, length):
    state = seed.copy()
    result = []
    for _ in range(length):
        output_bit = state[-1]
        result.append(output_bit)
        feedback = 0
        for t in taps:
            feedback ^= state[t]
        state = [feedback] + state[:-1]
    return result

# Параметры двух регистров и их многочленов (обратной связи)
taps1 = [0, 2]  # например, x^5 + x^3 + 1
seed1 = [1, 0, 1, 0, 1]  # 5 бит
taps2 = [1, 4]  # например, x^5 + x^2 + 1
seed2 = [0, 1, 1, 0, 1]  # 5 бит

plaintext = "одиндуракможетбольшеспрашиватьзптчемдесятьумныхответитьтчк"  # пример текста
plain_bits = text_to_bits(plaintext)
length = len(plain_bits)

# Генерируем два потока
lfsr1 = lfsr(seed1, taps1, length)
lfsr2 = lfsr(seed2, taps2, length)
# Итоговый поток — XOR двух регистров
keystream = [a ^ b for a, b in zip(lfsr1, lfsr2)]

# Шифруем
cipher_bits = [b ^ k for b, k in zip(plain_bits, keystream)]
print("Зашифрованные биты:", cipher_bits)
print("Зашифрованный текст:", bits_to_text(cipher_bits))

# Для расшифровки:
lfsr1_dec = lfsr(seed1, taps1, length)
lfsr2_dec = lfsr(seed2, taps2, length)
keystream_dec = [a ^ b for a, b in zip(lfsr1_dec, lfsr2_dec)]
plain_bits_dec = [c ^ k for c, k in zip(cipher_bits, keystream_dec)]
print("Расшифрованный текст:", bits_to_text(plain_bits_dec))