import logging
import os
from datetime import datetime
import time
import yaml
import pandas as pd
from typing import Any, Optional
from path_analysis.path_analysis import path_length
import typer

app = typer.Typer()


def read_yaml(yaml_file: str) -> dict[str, Any]:
    """
    Reading yaml file and saving the data to dictionary

    Args:
        yaml_file (str): yaml file path

    Returns:
        yaml_dic (dict): contains all the yaml file data
    """

    # load yaml config data
    with open(yaml_file, "r") as stream:
        try:
            yaml_dic = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            logging.error(exc)
    return yaml_dic


@app.command()
def main(
    config: str = typer.Option(..., "--config", help="YAML configuration file path"),
    run_dir: Optional[str] = typer.Option(
        None, "--run-dir", help="Directory to store the run outputs"
    ),
):
    """
    Runs Path Length analysis with given configuration.

    Args:
        config (str): Path to the YAML configuration file.
        run_dir (str, optional): Directory to store run outputs. Defaults to the current directory.
    """
    # logs format
    now_str = datetime.utcnow().strftime("length_run_%Y_%m_%d_%H_%M_%S")

    # checking config file existence
    if not os.path.exists(config):
        logging.error(f"The configuration file {config} doesn't exist, please check")
        raise typer.Exit(code=1)

    if run_dir in ["pwd", "", None]:
        run_dir = os.path.join(os.path.abspath(os.getcwd()), now_str)
    else:
        run_dir = os.path.abspath(run_dir)

    # checking run_dir existence & creation
    if not os.path.isdir(run_dir):
        os.makedirs(run_dir, exist_ok=True)
    else:
        os.makedirs(run_dir, exist_ok=True)

    # logs setup
    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[
            logging.FileHandler(os.path.join(run_dir, f"{now_str}.log")),
            logging.StreamHandler(),
        ],
        format="%(asctime)s | %(levelname)-7s | %(message)s",
        datefmt="%d-%b-%Y %H:%M:%S",
    )

    # set pandas options
    pd.set_option("display.max_rows", None)

    # reading config file
    config_data = read_yaml(config)

    # Calling the main function
    time_start = time.time()
    path_length_df = path_length(**config_data)
    exc_time = time.time() - time_start

    # Save clean report with desired lengths
    path_length_df.to_csv(os.path.join(run_dir, "final_report_length.csv"), index=False)
    logging.info(f"path_length_report: \n {path_length_df}")

    # Reporting execution time
    logging.info(f"Path length execution time: {exc_time} sec")


if __name__ == "__main__":
    app()
