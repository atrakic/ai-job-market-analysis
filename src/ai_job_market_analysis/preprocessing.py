def analyze_salary(df):
    return df.groupby("job_title")["salary"].mean().sort_values(ascending=False)


def clean_data(df):
    df = df.dropna()
    # add more cleaning steps
    return df
