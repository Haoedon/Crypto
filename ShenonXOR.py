def lfsr(seed, taps, length):
    state = seed.copy()
    result = []
    for step in range(length):
        output_bit = state[-1]
        result.append(output_bit)
        feedback = 0
        for t in taps:
            feedback ^= state[t]
        state = [feedback] + state[:-1]
    return result

def text_to_bits(text):
    return [int(bit) for char in text.encode('utf-8') for bit in format(char, '08b')]

def bits_to_text(bits):
    chars = []
    for b in range(0, len(bits), 8):
        byte = bits[b:b+8]
        if len(byte) < 8:
            break
        chars.append(chr(int(''.join(map(str, byte)), 2)))
    return ''.join(chars)

# Параметры регистров (пример)
taps1 = [0, 3]
seed1 = [1, 0, 0, 1]
taps2 = [2, 4]
seed2 = [1, 0, 1, 0, 1]

# Текст для шифрования
plaintext = "Пример текста"

# Переводим текст в биты
plain_bits = text_to_bits(plaintext)
length = len(plain_bits)

# Генерируем псевдослучайную последовательность
lfsr1 = lfsr(seed1, taps1, length)
lfsr2 = lfsr(seed2, taps2, length)
scrambler = [a ^ b for a, b in zip(lfsr1, lfsr2)]

# Шифруем
cipher_bits = [b ^ k for b, k in zip(plain_bits, scrambler)]

# Выводим результат
print('Зашифрованные биты:', cipher_bits)
print('Зашифрованный текст:', bits_to_text(cipher_bits))