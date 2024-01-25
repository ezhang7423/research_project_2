import dataclasses
from dataclasses import dataclass

import typer
from rich import print
from typer_config.decorators import dump_json_config, use_json_config

from research_project import setup_experiment

setup_experiment()
from eztils import datestr
from eztils.typer import dataclass_option

from research_project import LOG_DIR, version

app = typer.Typer(
    name="research_project",
    help="project_tag",
    add_completion=False,
)


@dataclass
class Config:
    block_size: int = 1024
    recent_context: int = 20
    add_prompt: int = True
    n_layer: int = 3
    n_head: int = 1
    n_embd: int = 64
    dropout: float = 0.0
    bias: bool = True  # True: bias in Linears and LayerNorms, like GPT-2. False: a bit better and faster
    wandb_project: str = "project"
    wandb_profile_name: str = "ezipe"
    name: str = f"experiment_{datestr()}"


@app.command(name="")
@use_json_config()
@dump_json_config(str(LOG_DIR / "config.json"))
def main(
    conf: dataclass_option(Config) = "{}",  # type: ignore,
    wandb: bool = False,
) -> None:
    """Print a greeting with a giving name."""
    conf: Config = conf  # for type hinting

    print(f"[bold green]Welcome to research_project v{version}[/]")
    print(f"config {type(conf)}: {conf}")
    if wandb:
        import wandb as wb

        wb.init(
            project=conf.wandb_project,
            entity=conf.wandb_profile_name,
            name=conf.name,
            config=dataclasses.asdict(conf),
        )


app()
