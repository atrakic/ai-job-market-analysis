import logging
from contextlib import asynccontextmanager
from functools import lru_cache

import pandas as pd
from fastapi import FastAPI, HTTPException, Query

from ai_job_market_analysis.analysis import analyze_salary, detect_columns
from ai_job_market_analysis.data_download import download_dataset
from ai_job_market_analysis.data_loader import load_data
from ai_job_market_analysis.preprocessing import clean_data
from ai_job_market_analysis.utils import csv_exists, get_config
from ai_job_market_analysis.utils import find_csv

logger = logging.getLogger("uvicorn.error")


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not csv_exists():
        config = get_config()
        logger.info("Dataset not found — downloading '%s'…", config["dataset"])
        try:
            download_dataset(config["dataset"])
            logger.info("Dataset downloaded successfully.")
        except Exception as exc:
            logger.warning("Auto-download failed: %s. Set KAGGLE_USERNAME and KAGGLE_KEY env vars.", exc)
    yield


app = FastAPI(
    title="AI Job Market API",
    description="REST API for the AI job market dataset",
    version="1.0.0",
    lifespan=lifespan,
)


@lru_cache(maxsize=1)
def _load_df() -> pd.DataFrame:
    path = find_csv()
    df = load_data(path)
    return clean_data(df)


def get_df() -> pd.DataFrame:
    try:
        return _load_df()
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=503,
            detail="Dataset unavailable. Set KAGGLE_USERNAME and KAGGLE_KEY and restart.",
        ) from e


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------

@app.get("/health", tags=["meta"])
def health():
    """Service liveness check."""
    return {"status": "ok"}


@app.get("/info", tags=["meta"])
def info():
    """Dataset shape and column names."""
    df = get_df()
    return {"rows": len(df), "columns": list(df.columns)}


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

@app.get("/preview", tags=["data"])
def preview(limit: int = Query(default=10, ge=1, le=500)):
    """Return the first *limit* rows of the cleaned dataset."""
    df = get_df()
    return df.head(limit).to_dict(orient="records")


@app.get("/columns", tags=["data"])
def columns():
    """List all available column names."""
    df = get_df()
    return {"columns": list(df.columns)}


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------

@app.get("/salary/by-job", tags=["analysis"])
def salary_by_job(limit: int = Query(default=20, ge=1, le=200)):
    """Average salary ranked by job title (descending)."""
    df = get_df()
    try:
        result = analyze_salary(df).head(limit)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
    return result.reset_index().rename(
        columns={result.index.name: "job_title", result.name: "avg_salary"}
    ).to_dict(orient="records")


@app.get("/jobs/top", tags=["analysis"])
def top_jobs(limit: int = Query(default=10, ge=1, le=100)):
    """Most frequent job titles in the dataset."""
    df = get_df()
    try:
        job_col, _ = detect_columns(df)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
    counts = df[job_col].value_counts().head(limit)
    return [{"job_title": k, "count": int(v)} for k, v in counts.items()]


@app.get("/salary/distribution", tags=["analysis"])
def salary_distribution():
    """Basic salary statistics (min, max, mean, median)."""
    df = get_df()
    try:
        _, salary_col = detect_columns(df)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
    s = df[salary_col]
    return {
        "min": float(s.min()),
        "max": float(s.max()),
        "mean": float(s.mean()),
        "median": float(s.median()),
    }

