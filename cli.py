from ai_job_market_analysis.data_loader import load_data
from ai_job_market_analysis.preprocessing import clean_data
from ai_job_market_analysis.analysis import analyze_salary
from ai_job_market_analysis.visualization import plot_top_jobs


def main():
    df = load_data("data/raw/jobs.csv")
    df = clean_data(df)

    salary_data = analyze_salary(df)
    plot_top_jobs(salary_data)


if __name__ == "__main__":
    main()
