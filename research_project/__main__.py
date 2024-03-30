import dataclasses

import typer
from rich import print
from typer_config.decorators import dump_json_config, use_json_config

from research_project import Config, setup_experiment

setup_experiment()
# from eztils.torch import seed_everything # install torch first to uncomment this line (by getting `poetry add eztils[torch]`` as a dependency)
from eztils.typer import dataclass_option

from research_project import LOG_DIR, version

app = typer.Typer(
    name="research_project",
    help="project_tag",
    add_completion=False,
)


@app.command(name="")
@use_json_config()
@dump_json_config(str(LOG_DIR / "config.json"))
def main(
    conf: dataclass_option(Config) = "{}",  # type: ignore,
    wandb: bool = False,
) -> None:
    """Print a greeting with a giving name."""
    conf: Config = conf  # for type hinting
    # seed_everything(conf.seed)

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
