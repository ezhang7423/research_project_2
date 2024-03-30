"""project_tag"""

""" 
Other global variables
"""
from typing import Optional

import dataclasses
import os
from argparse import Namespace
from dataclasses import dataclass, make_dataclass
from importlib import metadata as importlib_metadata
from pathlib import Path

from dotenv import load_dotenv
from eztils import abspath, datestr, setup_path
from eztils.argparser import HfArgumentParser, update_dataclass_defaults
from rich import print

load_dotenv()


def get_version() -> str:
    try:
        return importlib_metadata.version("research_project")
    except importlib_metadata.PackageNotFoundError:  # pragma: no cover
        return "unknown"


version: str = get_version()
__version__ = version

REPO_DIR = setup_path(Path(abspath()) / "..")
DATA_ROOT = setup_path(os.getenv("DATA_ROOT") or REPO_DIR)
RUN_DIR = LOG_DIR = Path()


def setup_experiment():
    """
    Sets up the experiment by creating a run directory and a log directory, and creating a symlink from the repo directory to the run directory.
    """
    print("Setting up experiment...")
    global RUN_DIR
    global LOG_DIR

    # create run dir
    RUN_DIR = setup_path(DATA_ROOT / "runs")
    LOG_DIR = setup_path(RUN_DIR / datestr())

    print(f"LOG DIR: {LOG_DIR}")

    # symlink repo dir / runs to run_dir
    if not (REPO_DIR / "runs").exists() and (REPO_DIR / "runs") != RUN_DIR:
        print(f'Creating symlink from {REPO_DIR / "runs"} to {RUN_DIR}')
        (REPO_DIR / "runs").symlink_to(RUN_DIR)

    os.chdir(LOG_DIR)

    """SETUP CONFIG"""
    parser = HfArgumentParser(Config)
    parser.add_argument("-c", "--config", type=str)

    conf: Config
    extras: Namespace
    conf, extras = parser.parse_args_into_dataclasses()

    if extras.config is not None:  # parse config file
        (original_conf,) = parser.parse_json_file(extras.config)
        # reinit the parser so that the command line args overwrite the file-specified args
        parser = HfArgumentParser(update_dataclass_defaults(Config, original_conf))
        parser.add_argument("-c", "--config", type=str)
        conf, extras = parser.parse_args_into_dataclasses()

    parser.to_json([conf], LOG_DIR / "config.json")
    return conf


@dataclass
class Config:
    block_size: int = 1024
    recent_context: int = 20
    add_prompt: int = True
    n_layer: int = 3
    n_head: int = 1
    n_embd: int = 64
    dropout: float = 0.0
    bias: bool = (
        True  # True: bias in Linears and LayerNorms, like GPT-2. False: a bit better and faster
    )
    seed: int = 42
    wandb: bool = False


def main():
    conf = setup_experiment()

    print(f"[bold green]Welcome to research_project v{version}[/]")
    print(conf)

    # from eztils.torch import seed_everything # install torch first to uncomment this line (by getting `poetry add eztils[torch]`` as a dependency)
    # seed_everything(conf.seed)
    if conf.wandb:
        import wandb as wb

        wb.init(
            project=conf.wandb_project,
            entity=conf.wandb_profile_name,
            name=conf.name,
            config=dataclasses.asdict(conf),
        )


if __name__ == "__main__":
    main()
