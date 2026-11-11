import argparse

def main():
    parser = argparse.ArgumentParser(
        description='Трансляция последовательности РНК в белковую последовательность.'
    )

    parser.add_argument('input_file', help='Путь к входному файлу')
    parser.add_argument('-o', '--output', help='Путь к выходному файлу')

    args = parser.parse_args()

    try:
        # Считываем последовательность РНК
        with open(args.input_file, 'r', encoding='utf-8') as file:
            rna = file.readline().strip().upper()

        # Проверяем входные данные
        if not rna:
            raise ValueError('Входной файл не содержит последовательность РНК.')

        if any(c not in 'AUGC' for c in rna):
            raise ValueError('Последовательность может содержать только A, U, G, C.')

        if len(rna) % 3 != 0:
            raise ValueError('Длина последовательности должна быть кратна трём.')

        # Таблица генетического кода
        codons = {
            'UUU': 'F', 'UUC': 'F', 'UUA': 'L', 'UUG': 'L',
            'UCU': 'S', 'UCC': 'S', 'UCA': 'S', 'UCG': 'S',
            'UAU': 'Y', 'UAC': 'Y', 'UAA': 'STOP', 'UAG': 'STOP',
            'UGU': 'C', 'UGC': 'C', 'UGA': 'STOP', 'UGG': 'W',

            'CUU': 'L', 'CUC': 'L', 'CUA': 'L', 'CUG': 'L',
            'CCU': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
            'CAU': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q',
            'CGU': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R',

            'AUU': 'I', 'AUC': 'I', 'AUA': 'I', 'AUG': 'M',
            'ACU': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',
            'AAU': 'N', 'AAC': 'N', 'AAA': 'K', 'AAG': 'K',
            'AGU': 'S', 'AGC': 'S', 'AGA': 'R', 'AGG': 'R',

            'GUU': 'V', 'GUC': 'V', 'GUA': 'V', 'GUG': 'V',
            'GCU': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',
            'GAU': 'D', 'GAC': 'D', 'GAA': 'E', 'GAG': 'E',
            'GGU': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G'
        }

        # Переводим последовательность РНК в белок
        protein = ''

        for i in range(0, len(rna), 3):
            codon = rna[i:i + 3]

            if codons[codon] == 'STOP':
                break

            protein += codons[codon]

        # Выводим результат
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as file:
                file.write(protein + '\n')
            print('Результат сохранён в файл:', args.output)
        else:
            print(protein)

    except ValueError as error:
        parser.error(str(error))

    except OSError:
        parser.error(
            'Не удалось прочитать или записать файл. Проверьте путь и права доступа.'
        )

if __name__ == '__main__':
    main()