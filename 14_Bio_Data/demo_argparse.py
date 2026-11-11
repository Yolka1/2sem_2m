import argparse
from pathlib import Path

from sequence_reader import FastaReader, FastqReader
from sam_reader import SamReader
from vcf_reader import VcfReader

# ---------- ВЫБОР ФАЙЛА ----------

def choose_file(extension):
    """Выводит список файлов нужного формата."""

    files = sorted(
        file for file in Path(".").iterdir()
        if file.is_file() and file.suffix.lower() == extension
    )

    if not files:
        print(f"\nФайлы формата {extension} не найдены.")
        return None

    print(f"\nДоступные файлы {extension}:")

    for number, file in enumerate(files, start=1):
        print(f"{number}. {file.name}")

    while True:
        try:
            choice = int(input("Введите номер файла: "))

            if 1 <= choice <= len(files):
                return str(files[choice - 1])

            print("Такого номера нет. Попробуйте ещё раз.")

        except ValueError:
            print("Введите целое число.")

# ---------- FASTA ----------

def analyze_fasta():
    filename = choose_file(".fasta")

    if filename is None:
        return

    reader = FastaReader(filename)

    print("\n" + "=" * 40)
    print(f"Результаты анализа: {filename}")
    print("=" * 40)

    print("Количество последовательностей:",
          reader.get_sequences_count())

    print("Средняя длина последовательности:",
          reader.get_average_length())

# ---------- FASTQ ----------

def analyze_fastq():
    filename = choose_file(".fastq")

    if filename is None:
        return

    reader = FastqReader(filename)

    print("\n" + "=" * 40)
    print(f"Результаты анализа: {filename}")
    print("=" * 40)

    print("Количество последовательностей:",
          reader.get_sequences_count())

    print("Средняя длина последовательности:",
          reader.get_average_length())

    print("\nПостроение графика качества...")
    reader.plot_quality()

# ---------- SAM ----------

def analyze_sam():
    filename = choose_file(".sam")

    if filename is None:
        return

    reader = SamReader(filename)

    print("\n" + "=" * 40)
    print(f"Результаты анализа: {filename}")
    print("=" * 40)

    print("\nМета-строки:")
    for line in reader.get_meta_lines():
        print(line)

    print("\nPG ID:", " ".join(reader.get_group_ids("PG")))
    print("RG ID:", " ".join(reader.get_group_ids("RG")))
    print("SQ ID:", " ".join(reader.get_group_ids("SQ")))

    print("\nКоличество выравниваний:",
          reader.count_records())

    print("\nСтатистика по хромосомам:")
    print(reader.chromosome_stats().to_string(index=False))

# ---------- VCF ----------

def analyze_vcf():
    filename = choose_file(".vcf")

    if filename is None:
        return

    reader = VcfReader(filename)

    print("\n" + "=" * 40)
    print(f"Результаты анализа: {filename}")
    print("=" * 40)

    print("\nМета-строки:")
    for line in reader.get_meta_lines():
        print(line)

    print("\nINFO ID:", " ".join(reader.get_group_ids("INFO")))
    print("FORMAT ID:", " ".join(reader.get_group_ids("FORMAT")))
    print("FILTER ID:", " ".join(reader.get_group_ids("FILTER")))
    print("contig ID:", " ".join(reader.get_group_ids("contig")))

    print("\nКоличество вариантов:",
          reader.count_variants())

    print("\nСтатистика по регионам:")
    print(reader.region_count_stats().to_string(index=False))

# ---------- ГЛАВНОЕ МЕНЮ ----------

def main():
    parser = argparse.ArgumentParser(
        description="Программа для анализа биологических файлов."
    )

    formats = parser.add_subparsers(
        dest="format",
        help="Выберите формат файла"
    )

    formats.add_parser("fasta", help="Анализ FASTA-файлов")
    formats.add_parser("fastq", help="Анализ FASTQ-файлов")
    formats.add_parser("sam", help="Анализ SAM-файлов")
    formats.add_parser("vcf", help="Анализ VCF-файлов")

    args = parser.parse_args()

    commands = {
        "fasta": analyze_fasta,
        "fastq": analyze_fastq,
        "sam": analyze_sam,
        "vcf": analyze_vcf
    }

    if args.format is None:
        print("=" * 40)
        print("АНАЛИЗ БИОЛОГИЧЕСКИХ ФАЙЛОВ")
        print("=" * 40)

        print("Выберите формат файла:")
        print("1. FASTA")
        print("2. FASTQ")
        print("3. SAM")
        print("4. VCF")

        while True:
            try:
                choice = int(input("Ваш выбор: "))

                if 1 <= choice <= 4:
                    break

                print("Выберите число от 1 до 4.")

            except ValueError:
                print("Введите целое число.")

        selected_format = ["fasta", "fastq", "sam", "vcf"][choice - 1]
        commands[selected_format]()

    else:
        commands[args.format]()

if __name__ == "__main__":
    main()