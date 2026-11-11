import argparse

def main():
    parser = argparse.ArgumentParser(
        description='Построение консенсусной последовательности и профильной матрицы ДНК.'
    )

    parser.add_argument('input_file', help='Путь к входному FASTA-файлу')
    parser.add_argument('-o', '--output', help='Путь к выходному файлу')

    args = parser.parse_args()

    try:
        sequences = []
        current = []

        # Считываем последовательности из FASTA-файла
        with open(args.input_file, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()

                if not line:
                    continue

                if line.startswith('>'):
                    if current:
                        sequences.append(''.join(current))
                        current = []
                else:
                    current.append(line.upper())

            if current:
                sequences.append(''.join(current))

        # Проверяем входные данные
        if not sequences:
            raise ValueError('Файл не содержит последовательностей ДНК.')

        if any(not s for s in sequences):
            raise ValueError('Обнаружена пустая последовательность.')

        n = len(sequences[0])

        if any(len(s) != n for s in sequences):
            raise ValueError('Все последовательности должны иметь одинаковую длину.')

        if any(c not in 'ATGC' for s in sequences for c in s):
            raise ValueError('Последовательности могут содержать только A, T, G, C.')

        # Создаём профильную матрицу
        profile = {
            'A': [0] * n,
            'C': [0] * n,
            'G': [0] * n,
            'T': [0] * n
        }

        # Подсчитываем нуклеотиды в каждой позиции
        for s in sequences:
            for i in range(n):
                profile[s[i]][i] += 1

        # Строим консенсусную последовательность
        consensus = ''

        for i in range(n):
            maximum = max(profile[x][i] for x in profile)

            for x in profile:
                if profile[x][i] == maximum:
                    consensus += x
                    break

        # Формируем результат
        result = [consensus]

        for x in profile:
            result.append(x + ': ' + ' '.join(map(str, profile[x])))

        answer = '\n'.join(result)

        # Выводим результат в файл или терминал
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as file:
                file.write(answer + '\n')
            print('Результат сохранён в файл:', args.output)
        else:
            print(answer)

    except OSError:
        parser.error('Не удалось прочитать или записать файл. Проверьте путь и права доступа.')

    except ValueError as error:
        parser.error(str(error))

if __name__ == '__main__':
    main()