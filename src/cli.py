"""
Interfaz de línea de comandos.
Punto de entrada principal del programa.
"""

import sys
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

from src.services.parser import parse_yaml_file, ParserError
from src.services.generator import generate_sql, export_sql_file, GeneratorError
from config.settings import AppConfig

console = Console()


@click.group()
@click.version_option(version="0.1.0", prog_name="python-db-generator")
def cli() -> None:
    """python-db-generator — Genera bases de datos PostgreSQL desde YAML."""
    pass


@cli.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option(
    "--output",
    "-o",
    default=None,
    help="Carpeta de salida para el archivo .sql (por defecto: output/)",
)
@click.option(
    "--preview",
    "-p",
    is_flag=True,
    default=False,
    help="Muestra el SQL generado en consola sin guardar.",
)
def generate(input_file: str, output: str | None, preview: bool) -> None:
    """
    Genera SQL desde un archivo YAML de definición.

    INPUT_FILE: Ruta al archivo .yaml con la definición del schema.

    Ejemplos:

        python main.py generate schema.yaml

        python main.py generate schema.yaml --preview

        python main.py generate schema.yaml --output mi_carpeta/
    """
    console.print(Panel("[bold cyan]python-db-generator[/bold cyan]", expand=False))

    # Parsear el YAML
    console.print(f"\n[yellow]→[/yellow] Leyendo [bold]{input_file}[/bold]...")

    try:
        schema = parse_yaml_file(input_file)
    except ParserError as e:
        console.print(f"[red]✗ Error:[/red] {e}")
        sys.exit(1)

    console.print(f"[green]✓[/green] Schema [bold]{schema.name}[/bold] cargado.")
    console.print(f"  Tablas encontradas: {', '.join(schema.table_names())}")

    # Generar SQL
    console.print("\n[yellow]→[/yellow] Generando SQL...")

    try:
        sql = generate_sql(schema)
    except GeneratorError as e:
        console.print(f"[red]✗ Error generando SQL:[/red] {e}")
        sys.exit(1)

    console.print("[green]✓[/green] SQL generado correctamente.")

    # Mostrar preview
    if preview:
        console.print("\n[bold]Preview del SQL:[/bold]")
        syntax = Syntax(sql, "sql", theme="monokai", line_numbers=True)
        console.print(syntax)

    # Exportar archivo
    if not preview:
        output_dir = output or AppConfig.OUTPUT_DIR

        try:
            file_path = export_sql_file(schema, output_dir)
        except Exception as e:
            console.print(f"[red]✗ Error exportando archivo:[/red] {e}")
            sys.exit(1)

        console.print(f"\n[green]✓[/green] Archivo guardado en: [bold]{file_path}[/bold]")

    console.print("\n[bold green]¡Listo![/bold green]\n")


@cli.command()
def version() -> None:
    """Muestra la versión del programa."""
    console.print("python-db-generator v0.1.0")
