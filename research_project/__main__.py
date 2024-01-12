from dataclasses import dataclass

import typer
from rich import print
from typer_config.decorators import dump_json_config, use_json_config

from research_project import setup_experiment

setup_experiment()
from eztils.typer import dataclass_option

from research_project import LOG_DIR, version

app = typer.Typer(
    name="research_project",
    help="project_tag",
    add_completion=False,
)


@dataclass
class ExampleConfig:
    block_size: int = 1024
    recent_context: int = 20
    add_prompt: int = True
    n_layer: int = 3
    n_head: int = 1
    n_embd: int = 64
    dropout: float = 0.0
    bias: bool = True  # True: bias in Linears and LayerNorms, like GPT-2. False: a bit better and faster


@app.command(name="")
@use_json_config()
@dump_json_config(str(LOG_DIR / "config.json"))
def main(
    example_config: dataclass_option(ExampleConfig) = "{}",  # type: ignore
) -> None:
    """Print a greeting with a giving name."""

    print(f"[bold green]Welcome to research_project v{version}[/]")
    print(f"example_config {type(example_config)}: {example_config}")


app()
