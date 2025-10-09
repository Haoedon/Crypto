def lfsr(seed, taps, length):
    """Генерация последовательности РСЛОС"""
    state = seed.copy()
    result = []
    seen_states = {}
    for step in range(length):
        output_bit = state[-1]
        print(f"Шаг {step+1}: состояние = {state}, выходной бит = {output_bit}")
        result.append(output_bit)
        state_tuple = tuple(state)
        if state_tuple in seen_states:
            print(f"Зацикливание на шаге {step+1}: состояние {state}")
            break
        seen_states[state_tuple] = step+1
        # XOR по индексам обратной связи
        feedback = 0
        for t in taps:
            feedback ^= state[t]
        # Сдвиг регистра
        state = [feedback] + state[:-1]
    return result

# Функция для поиска правильного начального состояния
def find_max_period_seed(taps, reg_len, max_period):
    from itertools import product
    for seed in product([0, 1], repeat=reg_len):
        if all(bit == 0 for bit in seed):
            continue  # пропустить нулевое состояние
        state = list(seed)
        seen_states = {}
        for step in range(max_period + 1):
            state_tuple = tuple(state)
            if state_tuple in seen_states:
                break
            seen_states[state_tuple] = step+1
            feedback = 0
            for t in taps:
                feedback ^= state[t]
            state = [feedback] + state[:-1]
        # Если цикл начинается на шаге max_period+1, это правильное состояние
        if len(seen_states) == max_period:
            return list(seed)
    return None
# Многочлен x^5 + x^3 + x^2 + x + 1: обратная связь с битами 4, 2, 1, 0 (индексация с 0)
taps = [0, 1, 2, 4]  # x^5 (бит 4), x^3 (бит 2), x^2 (бит 1), x (бит 0)
reg_len = 5
max_period = 31  # максимальный период для 5 бит
seed = find_max_period_seed(taps, reg_len, max_period)
if seed:
    print(f"Подобрано начальное состояние: {seed}")
    sequence = lfsr(seed, taps, max_period)
    print("РСЛОС последовательность:", sequence)
else:
    print("Не удалось подобрать начальное состояние с максимальным периодом.")