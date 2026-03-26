import os
import streamlit as st
from ai_job_market_analysis.data_loader import load_data
from ai_job_market_analysis.preprocessing import clean_data
from ai_job_market_analysis.utils import find_csv, get_config, csv_exists
from ai_job_market_analysis.data_download import download_dataset

st.title("AI Job Market Dashboard")


@st.cache_data
def get_data():
    path = find_csv()
    df = load_data(path)
    return clean_data(df)


if not csv_exists():
    st.warning(
        "No dataset found in `data/raw/`. Provide your Kaggle credentials to download it."
    )

    with st.expander("Kaggle API credentials", expanded=True):
        kaggle_username = st.text_input(
            "Kaggle username", value=os.environ.get("KAGGLE_USERNAME", "")
        )
        kaggle_key = st.text_input(
            "Kaggle API key", type="password", value=os.environ.get("KAGGLE_KEY", "")
        )

        if st.button("Download dataset"):
            if not kaggle_username or not kaggle_key:
                st.error("Both username and API key are required.")
            else:
                os.environ["KAGGLE_USERNAME"] = kaggle_username
                os.environ["KAGGLE_KEY"] = kaggle_key
                config = get_config()
                with st.spinner("Downloading dataset from Kaggle…"):
                    try:
                        download_dataset(config["dataset"])
                        st.success("Dataset downloaded. Reload the page to continue.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Download failed: {e}")
    st.stop()

df = get_data()
st.write("### Preview")
st.dataframe(df.head())

if "job_title" in df.columns:
    st.write("### Top Jobs")
    st.bar_chart(df["job_title"].value_counts().head(10))

if "salary" in df.columns:
    st.write("### Salary Distribution")
    st.line_chart(df["salary"])
