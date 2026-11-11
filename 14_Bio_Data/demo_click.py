import click
from pathlib import Path

from sequence_reader import FastaReader, FastqReader
from sam_reader import SamReader
from vcf_reader import VcfReader

# ---------- ВЫБОР ФАЙЛА ----------

def choose_file(extension):
    """Выводит список файлов нужного формата и предлагает выбрать один."""

    files = sorted(
        file for file in Path(".").iterdir()
        if file.is_file() and file.suffix.lower() == extension
    )

    if not files:
        click.echo(f"Файлы формата {extension} не найдены.")
        return None

    click.echo(f"\nДоступные файлы {extension}:")

    for number, file in enumerate(files, start=1):
        click.echo(f"{number}. {file.name}")

    choice = click.prompt(
        "Введите номер файла",
        type=click.IntRange(1, len(files))
    )

    return str(files[choice - 1])

# ---------- ОСНОВНАЯ ПРОГРАММА ----------

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """Программа для анализа биологических файлов."""

    if ctx.invoked_subcommand is None:
        click.echo("=" * 40)
        click.echo("АНАЛИЗ БИОЛОГИЧЕСКИХ ФАЙЛОВ")
        click.echo("=" * 40)
        click.echo("Выберите формат файла:")
        click.echo("1. FASTA")
        click.echo("2. FASTQ")
        click.echo("3. SAM")
        click.echo("4. VCF")

        choice = click.prompt(
            "Ваш выбор",
            type=click.IntRange(1, 4)
        )

        commands = {
            1: "fasta",
            2: "fastq",
            3: "sam",
            4: "vcf"
        }

        ctx.invoke(cli.commands[commands[choice]])

# ---------- FASTA ----------

@cli.command()
def fasta():
    """Анализ FASTA-файла."""

    filename = choose_file(".fasta")
    if filename is None:
        return

    reader = FastaReader(filename)

    click.echo("\n" + "=" * 40)
    click.echo(f"Результаты анализа: {filename}")
    click.echo("=" * 40)

    click.echo(
        f"Количество последовательностей: "
        f"{reader.get_sequences_count()}"
    )
    click.echo(
        f"Средняя длина последовательности: "
        f"{reader.get_average_length()}"
    )

# ---------- FASTQ ----------

@cli.command()
def fastq():
    """Анализ FASTQ-файла."""

    filename = choose_file(".fastq")
    if filename is None:
        return

    reader = FastqReader(filename)

    click.echo("\n" + "=" * 40)
    click.echo(f"Результаты анализа: {filename}")
    click.echo("=" * 40)

    click.echo(
        f"Количество последовательностей: "
        f"{reader.get_sequences_count()}"
    )
    click.echo(
        f"Средняя длина последовательности: "
        f"{reader.get_average_length()}"
    )

    click.echo("\nПостроение графика качества...")
    reader.plot_quality()

# ---------- SAM ----------

@cli.command()
def sam():
    """Анализ SAM-файла."""

    filename = choose_file(".sam")
    if filename is None:
        return

    reader = SamReader(filename)

    click.echo("\n" + "=" * 40)
    click.echo(f"Результаты анализа: {filename}")
    click.echo("=" * 40)

    click.echo("\nМета-строки:")
    for line in reader.get_meta_lines():
        click.echo(line)

    click.echo("\nPG ID: " + " ".join(reader.get_group_ids("PG")))
    click.echo("RG ID: " + " ".join(reader.get_group_ids("RG")))
    click.echo("SQ ID: " + " ".join(reader.get_group_ids("SQ")))

    click.echo(
        f"\nКоличество выравниваний: {reader.count_records()}"
    )

    click.echo("\nСтатистика по хромосомам:")
    click.echo(reader.chromosome_stats().to_string(index=False))

# ---------- VCF ----------

@cli.command()
def vcf():
    """Анализ VCF-файла."""

    filename = choose_file(".vcf")
    if filename is None:
        return

    reader = VcfReader(filename)

    click.echo("\n" + "=" * 40)
    click.echo(f"Результаты анализа: {filename}")
    click.echo("=" * 40)

    click.echo("\nМета-строки:")
    for line in reader.get_meta_lines():
        click.echo(line)

    click.echo("\nINFO ID: " + " ".join(reader.get_group_ids("INFO")))
    click.echo("FORMAT ID: " + " ".join(reader.get_group_ids("FORMAT")))
    click.echo("FILTER ID: " + " ".join(reader.get_group_ids("FILTER")))
    click.echo("contig ID: " + " ".join(reader.get_group_ids("contig")))

    click.echo(
        f"\nКоличество вариантов: {reader.count_variants()}"
    )

    click.echo("\nСтатистика по регионам:")
    click.echo(reader.region_count_stats().to_string(index=False))

if __name__ == "__main__":
    cli()