from fastapi import FastAPI
from ai_job_market_analysis.data_loader import load_data
from ai_job_market_analysis.preprocessing import clean_data
from ai_job_market_analysis.utils import find_csv

app = FastAPI(title="AI Job Market API")

@app.get("/preview")
def preview():
    path = find_csv()
    df = load_data(path)
    df = clean_data(df)
    return df.head(10).to_dict(orient="records")
