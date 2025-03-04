from flask import Flask, request, render_template
from database import fetch_data

app = Flask(__name__)


def get_data_for_date(date):
    """Fetch OHLC & Bollinger Bands for a specific date."""
    ohlc = fetch_data("SELECT * FROM data WHERE DATE(datetime) = %s", (date,))
    indicators = fetch_data(
        "SELECT * FROM indicators WHERE DATE(datetime) = %s", (date,)
    )
    return ohlc, indicators


@app.route("/", methods=["GET", "POST"])
def index():
    data, indicators = None, None
    if request.method == "POST":
        date = request.form["date"]
        data, indicators = get_data_for_date(date)
    return render_template("index.html", data=data, indicators=indicators)


if __name__ == "__main__":
    app.run(debug=True)
