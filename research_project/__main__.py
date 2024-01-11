# type: ignore[attr-defined]
from typing import Optional

from enum import Enum
from random import choice

import typer
from rich.console import Console
from typer_config.decorators import dump_json_config, use_json_config

from research_project import setup_experiment

setup_experiment()
from research_project import LOG_DIR, version



app = typer.Typer(
    name="research_project",
    help="project_tag",
    add_completion=False,
)
console = Console()


def version_callback(print_version: bool) -> None:
    """Print the version of the package."""
    if print_version:
        console.print(f"[yellow]research_project[/] version: [bold blue]{version}[/]")
        raise typer.Exit()


@app.command(name="")
@use_json_config()
@dump_json_config(str(LOG_DIR / "config.json"))
def main(
    # add my custom option 
) -> None:
    """Print a greeting with a giving name."""

    console.print(f"[bold green]Welcome to your new project[/]")


app()
