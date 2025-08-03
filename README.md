A Python Flask-based web app that lets users fetch and view live case details from Indian court portals (District Courts, Delhi High Court, and Supreme Court) in a clean and user-friendly dashboard.

📌 Project Overview
This project enables users to search for Indian court cases by Case Type, Case Number, and Filing Year, and displays:

Parties involved

Filing date & next hearing date

Links to the latest orders/judgments (PDF)

Raw case data (for transparency/debugging)

🏆 Built as part of a learning project to practice Flask, Web Scraping, and Database Integration.

✨ Key Features
Multi-court support:

District Courts (via eCourts portal)

Delhi High Court

Supreme Court of India

Dynamic Form: Dropdowns and auto-hiding of fields depending on the selected court type.

Live Data Fetching: Uses requests and BeautifulSoup to scrape real-time case details.

Error Handling: User-friendly messages when invalid case numbers are entered or if the site is unavailable.

Database Logging: All user queries and raw responses are stored in SQLite for record-keeping.

📂 Project Structure

court-data-fetcher/
├── app.py                     # Flask app entry point
├── court_scraper.py           # Web scraping logic for all courts
├── database.py                # SQLite database initialization and query logging
├── queries.db                 # SQLite database file (auto-created)
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
├── LICENSE                    # License file (MIT)
│
├── templates/                 # Jinja2 HTML templates
│   ├── index.html             # Main search form UI
│   └── result.html            # Case details dashboard
│
├── static/                    # Static assets (CSS, JS, images)
│   ├── css/
│   │   └── styles.css         # Optional custom CSS
│   └── screenshots/           # Screenshots for README
│       ├── home_page.png
│       ├── case_result.png
│       └── error.png
│
└── logs/                      # Optional: store debug logs or raw HTML responses
    └── debug.log


🛠️ Tech Stack
Backend: Python, Flask

Frontend: HTML5, CSS3 (Jinja templates)

Database: SQLite (with sqlite3)

Web Scraping: Requests + BeautifulSoup

🚀 How It Works
User Input: Enter case details using the form.

Scraping Engine:

Sends HTTP requests to court websites.

Parses HTML with BeautifulSoup.

Extracts structured details (parties, dates, PDFs).

Results Dashboard: Displays parsed data and provides direct PDF download links.

Database Logging: Logs each query with a timestamp and raw HTML for auditing.

⚡ Challenges & Learnings
Handling dynamic website layouts across multiple court portals.

Implementing flexible HTML parsers that adapt to different table formats.

Gracefully dealing with CAPTCHA restrictions and session-based requests.

Building a full-stack app without prior experience in HTML or Flask.

📥 Installation
# Clone repository
git clone https://github.com/your-username/court-data-fetcher.git

cd court-data-fetcher

# Create virtual environment and install dependencies
pip install -r requirements.txt

# Run the app
python app.py
Then open your browser at http://127.0.0.1:5000/.

📚 Future Improvements
Add more High Courts & state-specific eCourts portals.

Better CAPTCHA handling using automated token/session management.

Deploy online with Heroku or PythonAnywhere.

💡 Why This Project is Special
Built from scratch by a first-year student with no prior web development experience.

Demonstrates end-to-end full-stack development: backend, frontend, database, and web scraping.

Shows ability to work with real-world government data sources and adapt to changing layouts.

👨‍💻 Author
Megh Jaiswal

📜 License
This project is licensed under the MIT License – you are free to use, modify, and distribute it with attribution.

