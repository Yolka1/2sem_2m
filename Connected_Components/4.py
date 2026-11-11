import argparse

def main():
    parser = argparse.ArgumentParser(
        description='Подсчёт количества связных компонент неориентированного графа.'
    )

    parser.add_argument('input_file', help='Путь к входному файлу')
    parser.add_argument('-o', '--output', help='Путь к выходному файлу')

    args = parser.parse_args()

    try:
        # Считываем входные данные
        with open(args.input_file, 'r', encoding='utf-8') as file:
            data = list(map(int, file.read().split()))

        # Проверяем количество исходных данных
        if len(data) < 2:
            raise ValueError('Файл должен содержать количество вершин и рёбер.')

        n = data[0]
        m = data[1]

        if n < 1 or m < 0:
            raise ValueError('Количество вершин должно быть положительным, а рёбер — неотрицательным.')

        if len(data) != 2 + 2 * m:
            raise ValueError('Количество рёбер не соответствует входным данным.')

        # Создаём список смежности
        graph = [[] for _ in range(n + 1)]

        k = 2
        for i in range(m):
            a = data[k]
            b = data[k + 1]

            if not (1 <= a <= n and 1 <= b <= n):
                raise ValueError('Номер вершины выходит за допустимые пределы.')

            graph[a].append(b)
            graph[b].append(a)

            k += 2

        # Создаём список посещённых вершин
        visited = [False] * (n + 1)
        count = 0

        # Ищем связные компоненты с помощью DFS
        for v in range(1, n + 1):
            if not visited[v]:
                count += 1
                stack = [v]
                visited[v] = True

                while stack:
                    current = stack.pop()

                    for neighbor in graph[current]:
                        if not visited[neighbor]:
                            visited[neighbor] = True
                            stack.append(neighbor)

        # Выводим результат
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as file:
                file.write(str(count) + '\n')
            print('Результат сохранён в файл:', args.output)
        else:
            print(count)

    except ValueError as error:
        parser.error(str(error))

    except OSError:
        parser.error('Не удалось прочитать или записать файл. Проверьте путь и права доступа.')

if __name__ == '__main__':
    main()