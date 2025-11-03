from typing import List, Optional

def calculate_average_length(names_list: List[str]) -> float:
    """
    Вычисляет среднее арифметическое длин имен
    :type names_list: List[str]
    :rtype: float
    """
    if not names_list:
        return 0

    total_length = sum(len(name) for name in names_list)

    return total_length / len(names_list)

def find_name_closest_to_average(names_list: List[str], average_length: float) -> Optional[str]:
    """
    Находит имя из списка, длина которого ближе всего к средней
    Если несколько имён имеют одинаковую минимальную разницу, возвращается первое найденное
    :type names_list: List[str]
    :type average_length: float
    :rtype: str or None
    """
    if not names_list:
        return None

    closest_name = names_list[0]
    min_diff = abs(len(names_list[0]) - average_length)

    for name in names_list[1:]:
        current_diff = abs(len(name) - average_length)

        if current_diff < min_diff:
            min_diff = current_diff
            closest_name = name

    return closest_name
