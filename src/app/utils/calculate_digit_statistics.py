from collections import Counter


def calculate_digit_statistics(
    content: bytes,
) -> dict[int, int]:
    """Подсчитать количество вхождений каждой цифры в содержимом файла."""
    digits = content.decode().strip()

    counts = Counter(digits)

    return {i: counts.get(str(i), 0) for i in range(10)}
