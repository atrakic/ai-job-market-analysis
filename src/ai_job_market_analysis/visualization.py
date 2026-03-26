import matplotlib.pyplot as plt
import os


def plot_top_jobs(data):
    os.makedirs("outputs/figures", exist_ok=True)

    plt.figure(figsize=(10, 5))
    data.head(10).plot(kind="bar")
    plt.title("Top Paying AI Jobs")
    plt.tight_layout()

    plt.savefig("outputs/figures/top_jobs.png")
    plt.close()
