import typer
import yaml

from ai_job_market_analysis.data_download import download_dataset
from ai_job_market_analysis.data_loader import load_data
from ai_job_market_analysis.preprocessing import clean_data
from ai_job_market_analysis.analysis import analyze_salary
from ai_job_market_analysis.visualization import plot_top_jobs
from ai_job_market_analysis.utils import find_csv

app = typer.Typer()


def get_config():
    with open("config.yaml") as f:
        return yaml.safe_load(f)


@app.command()
def all():
    """Fully automatic pipeline"""
    config = get_config()

    # 1. download
    download_dataset(config["dataset"])

    # 2. find dataset automatically
    path = find_csv()

    # 3. load + process
    df = load_data(path)
    df = clean_data(df)

    # 4. analyze
    result = analyze_salary(df)

    # 5. visualize
    plot_top_jobs(result)

    print("Full pipeline completed successfully.")
