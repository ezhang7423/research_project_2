"""project_tag"""

""" 
Other global variables
"""
import os
import sys
from importlib import metadata as importlib_metadata
from pathlib import Path

from dotenv import load_dotenv
from eztils import abspath, datestr, setup_path
from rich import print

load_dotenv()


def get_version() -> str:
    try:
        return importlib_metadata.version(__name__)
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
