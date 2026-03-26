import typer

from ai_job_market_analysis.analysis import analyze_salary
from ai_job_market_analysis.data_download import download_dataset
from ai_job_market_analysis.data_loader import load_data
from ai_job_market_analysis.preprocessing import clean_data
from ai_job_market_analysis.utils import find_csv, get_config
from ai_job_market_analysis.visualization import plot_top_jobs

app = typer.Typer(help="AI Job Market Analysis CLI")


@app.command()
def download():
    """Download the dataset from Kaggle."""
    config = get_config()
    download_dataset(config["dataset"])


@app.command()
def analyze():
    """Load, clean, analyze, and plot the dataset."""
    path = find_csv()
    df = load_data(path)
    df = clean_data(df)
    result = analyze_salary(df)
    plot_top_jobs(result)
    print("Analysis complete.")


@app.command()
def all():
    """Fully automatic pipeline: download → analyze."""
    download()
    analyze()
    print("Full pipeline completed successfully.")
