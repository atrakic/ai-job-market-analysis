def detect_columns(df):
    columns = [c.lower() for c in df.columns]

    salary_col = None
    job_col = None

    for col in df.columns:
        c = col.lower()

        if any(k in c for k in ["salary", "pay", "income"]):
            salary_col = col

        if any(k in c for k in ["job", "title", "role", "position"]):
            job_col = col

    if not salary_col or not job_col:
        raise ValueError(
            f"Could not detect required columns.\nColumns found: {df.columns}"
        )

    return job_col, salary_col


def analyze_salary(df):
    job_col, salary_col = detect_columns(df)

    return df.groupby(job_col)[salary_col].mean().sort_values(ascending=False)
