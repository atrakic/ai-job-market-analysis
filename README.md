# AI Job Market Analysis

## Overview
This project analyzes trends in the AI job market:
- Salary distribution
- Top-paying roles
- Market insights

## Inspiration
Inspired by a Kaggle notebook:
https://www.kaggle.com/code/sohaibdevv/ai-job-market-analysis

## Setup

```bash
git clone https://github.com/atrakic/ai-job-market-analysis.git
cd ai-job-market-analysis
uv sync
```

# AI Job Market Analysis

```
uv sync                    # install deps
uv run ai-job all           # full pipeline
uv run streamlit run app.py # dashboard
uv run uvicorn api:app --reload # API
```
