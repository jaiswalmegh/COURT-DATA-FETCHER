from flask import Flask, render_template, request
from court_scraper import fetch_case_data

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None

    if request.method == 'POST':
        try:
            court_type = request.form.get('court_type')
            case_type = request.form.get('case_type')
            case_number = request.form.get('case_number')
            year = request.form.get('year')

            # Only capture state and district for district court
            state = request.form.get('state') if court_type == "district" else None
            district = request.form.get('district') if court_type == "district" else None

            # Call the unified fetch_case_data function
            result = fetch_case_data(
                court_type,
                state,
                district,
                case_type,
                case_number,
                year
            )

            # Handle error in the result dictionary
            if result is None or "error" in result:
                error = result.get("error", "No data found or invalid input.")
                result = None

        except Exception as e:
            error = f"Error: {str(e)}"

    return render_template('index.html', result=result, error=error)


if __name__ == '__main__':
    app.run(debug=True)
