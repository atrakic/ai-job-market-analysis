# AI Job Market Analysis

## Overview

This project analyzes trends in the AI job market using a Kaggle dataset:

- Salary distribution across roles
- Top-paying and most frequent job titles
- Interactive Streamlit dashboard
- REST API for programmatic access

## Inspiration

Inspired by [this Kaggle notebook](https://www.kaggle.com/code/sohaibdevv/ai-job-market-analysis).

## Setup

```bash
git clone https://github.com/atrakic/ai-job-market-analysis.git
cd ai-job-market-analysis
uv sync
```

Set your Kaggle credentials (required to download the dataset):

```bash
export KAGGLE_USERNAME=<your-username>
export KAGGLE_KEY=<your-api-key>
```

Alternatively, enter them in the Streamlit dashboard when prompted.

## Usage

```bash
uv run ai-job all                       # full pipeline (download → clean → analyze → plot)
uv run streamlit run app.py             # interactive dashboard
uv run uvicorn api:app --reload         # REST API (http://localhost:8000)
```

## API Routes

Interactive docs are available at `http://localhost:8000/docs` once the server is running.

### Meta

| Method | Route     | Description                    |
| ------ | --------- | ------------------------------ |
| GET    | `/health` | Liveness check                 |
| GET    | `/info`   | Dataset shape and column names |

### Data

| Method | Route               | Description                   |
| ------ | ------------------- | ----------------------------- |
| GET    | `/columns`          | List all column names         |
| GET    | `/preview?limit=10` | Return first N rows (max 500) |

### Analysis

| Method | Route                     | Description                                     |
| ------ | ------------------------- | ----------------------------------------------- |
| GET    | `/salary/by-job?limit=20` | Average salary ranked by job title (descending) |
| GET    | `/salary/distribution`    | Min, max, mean, and median salary               |
| GET    | `/jobs/top?limit=10`      | Most frequent job titles                        |

## Project Structure

```
app.py              # Streamlit dashboard
api.py              # FastAPI REST API
src/
  ai_job_market_analysis/
    analysis.py     # salary analysis logic
    cli.py          # CLI entrypoint (uv run ai-job)
    data_download.py# Kaggle dataset downloader
    data_loader.py  # CSV loader
    preprocessing.py# data cleaning
    utils.py        # shared helpers
    visualization.py# matplotlib/seaborn plots
data/raw/           # downloaded CSV files (git-ignored)
outputs/            # generated figures and reports
notebooks/          # exploratory Jupyter notebooks
```
