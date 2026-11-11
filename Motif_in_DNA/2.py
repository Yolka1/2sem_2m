import click

@click.command()
@click.argument('input_file', type=click.Path(exists=True, dir_okay=False))
@click.option('-o', '--output', type=click.Path(), default=None,
              help='Путь к выходному файлу')

def main(input_file, output):
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            lines = [line.strip() for line in file if line.strip()]

        # Проверяем количество последовательностей
        if len(lines) != 2:
            raise click.ClickException(
                'В файле должны находиться две последовательности ДНК.'
            )

        s = lines[0].upper()
        t = lines[1].upper()

        # Проверяем корректность последовательностей
        if any(c not in 'ATGC' for c in s + t):
            raise click.ClickException(
                'Последовательности могут содержать только A, T, G, C.'
            )

        # Ищем все вхождения мотива
        result = []

        for i in range(len(s) - len(t) + 1):
            if s[i:i + len(t)] == t:
                result.append(str(i + 1))

        answer = ' '.join(result)

        # Выводим результат в файл или терминал
        if output:
            with open(output, 'w', encoding='utf-8') as file:
                file.write(answer + '\n')
            click.echo('Результат сохранён в файл: ' + output)
        else:
            click.echo(answer)

    except OSError:
        raise click.ClickException(
            'Не удалось прочитать или записать файл. Проверьте путь и права доступа.'
        )

if __name__ == '__main__':
    main()