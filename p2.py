import requests
import matplotlib.pyplot as plt

API_URL = "https://api.example.com/students/scores"  

SAMPLE = [
    {"name": "Asha", "score": 82}, 
    {"name": "Rahul", "score": 74},
    {"name": "Priya", "score": 91}, 
    {"name": "Sam", "score": 65},
    {"name": "Meera", "score": 88},
]


def fetch_scores():
    try:
        r = requests.get(API_URL, timeout=10)
        r.raise_for_status()
        return r.json()
    except (requests.RequestException, ValueError):
        print("API unavailable, using sample data.")
        return SAMPLE


def main():
    data = fetch_scores()
    names = [d["name"] for d in data]
    scores = [d["score"] for d in data]
    avg = sum(scores) / len(scores)
    print(f"Average score: {avg:.2f}")

    plt.figure(figsize=(8, 5))
    plt.bar(names, scores, color="steelblue")
    plt.axhline(avg, color="red", linestyle="--", label=f"Average = {avg:.1f}")
    plt.xlabel("Student")
    plt.ylabel("Test score")
    plt.title("Student Test Scores")
    plt.legend()
    plt.tight_layout()
    plt.savefig("scores_chart.png")
    # plt.show()  # Commented out for headless execution


if __name__ == "__main__":
    main()