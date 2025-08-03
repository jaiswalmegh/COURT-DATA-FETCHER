import requests
from bs4 import BeautifulSoup

# Unified entry function (6 parameters)
def fetch_case_data(court_type, state_cd, dist_cd, case_type, case_number, year):
    """
    court_type: 'district', 'delhi_high', or 'supreme'
    state_cd, dist_cd: only required for district court
    """
    if court_type == "district":
        return scrape_district_court(state_cd, dist_cd, case_type, case_number, year)
    elif court_type == "delhi_high":
        return scrape_delhi_high_court(case_type, case_number, year)
    elif court_type == "supreme":
        return scrape_supreme_court(case_type, case_number, year)
    else:
        return {"error": "Invalid court type selected"}

# ------------------- District Court Scraper -------------------
def scrape_district_court(state_cd, dist_cd, case_type, case_number, year):
    url = "https://services.ecourts.gov.in/ecourtsweb/cases/case_no.php"
    payload = {
        'state_cd': state_cd,
        'dist_cd': dist_cd,
        'court_code': '0',
        'case_type': case_type,
        'case_no': case_number,
        'case_year': year,
        'submit': 'Submit'
    }
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        response = requests.post(url, data=payload, headers=headers, timeout=15)
        print(response.text[:1000])  # Debug: print first 1000 chars of response

        if "Invalid Case Details" in response.text or "does not exist" in response.text:
            return {"error": "No data found. Invalid case number or year."}

        soup = BeautifulSoup(response.text, 'html.parser')

        tables = soup.find_all("table")
        if not tables:
            return {
                "error": "Could not parse data. Website layout may have changed.",
                "raw_html": response.text
            }

        parties = filing_date = next_hearing_date = "Not Available"
        for table in tables:
            rows = table.find_all("tr")
            for row in rows:
                cols = [c.get_text(strip=True) for c in row.find_all("td")]
                if len(cols) == 2:
                    label, value = cols
                    if "Petitioner" in label or "Respondent" in label:
                        parties = value
                    elif "Filing" in label:
                        filing_date = value
                    elif "Next" in label:
                        next_hearing_date = value

        pdf_url = None
        for link in soup.find_all("a", href=True):
            if "judgments" in link['href'] or "orders" in link['href']:
                pdf_url = "https://services.ecourts.gov.in" + link['href']
                break

        return {
            "parties": parties,
            "filing_date": filing_date,
            "next_hearing_date": next_hearing_date,
            "pdf_url": pdf_url or "No recent order found",
            "raw_html": response.text
        }

    except Exception as e:
        return {"error": f"Error fetching case details: {str(e)}"}

# ------------------- Delhi High Court Scraper -------------------
def scrape_delhi_high_court(case_type, case_number, year):
    url = "https://delhihighcourt.nic.in/dhc_case_status_list_new.asp"
    headers = {'User-Agent': 'Mozilla/5.0'}

    payload = {
        'case_type': case_type,
        'case_no': case_number,
        'case_year': year,
        'submit': 'Submit'
    }

    try:
        response = requests.post(url, data=payload, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')

        case_table = soup.find("table", {"id": "ctl00_ContentPlaceHolder1_gvCaseStatus"})
        if not case_table:
            return {
                "error": "Could not parse data. Layout may have changed.",
                "raw_html": response.text
            }

        rows = case_table.find_all("tr")
        if len(rows) < 2:
            return {"error": "No case details available.", "raw_html": response.text}

        cols = rows[1].find_all("td")
        parties = cols[3].text.strip() if len(cols) > 3 else "Not Available"
        filing_date = cols[4].text.strip() if len(cols) > 4 else "Not Available"
        next_hearing_date = cols[5].text.strip() if len(cols) > 5 else "Not Available"

        pdf_url = None
        link_tag = rows[1].find("a", href=True)
        if link_tag:
            pdf_url = "https://delhihighcourt.nic.in/" + link_tag['href']

        return {
            "parties": parties,
            "filing_date": filing_date,
            "next_hearing_date": next_hearing_date,
            "pdf_url": pdf_url or "No recent order found",
            "raw_html": response.text
        }

    except Exception as e:
        return {"error": f"Error fetching from Delhi High Court: {str(e)}"}

# ------------------- Supreme Court Scraper -------------------
def scrape_supreme_court(case_type, case_number, year):
    url = "https://main.sci.gov.in/php/case_status/case_status_process.php"
    headers = {'User-Agent': 'Mozilla/5.0'}

    payload = {
        'd_no': case_number,
        'd_yr': year,
        'd_type': case_type,
        'Submit': 'Submit'
    }

    try:
        response = requests.post(url, data=payload, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')

        petitioner_label = soup.find("td", string="Petitioner")
        if not petitioner_label:
            return {
                "error": "Could not parse data. Layout may have changed.",
                "raw_html": response.text
            }

        parties = petitioner_label.find_next("td").text.strip()
        filing_date_label = soup.find("td", string="Filing Date")
        filing_date = filing_date_label.find_next("td").text.strip() if filing_date_label else "Not Available"

        next_hearing = soup.find("td", string="Next Date of Hearing")
        next_hearing_date = next_hearing.find_next("td").text.strip() if next_hearing else "Not Available"

        pdf_link = soup.find("a", href=True, string="View")
        pdf_url = "https://main.sci.gov.in" + pdf_link['href'] if pdf_link else "No recent order found"

        return {
            "parties": parties,
            "filing_date": filing_date,
            "next_hearing_date": next_hearing_date,
            "pdf_url": pdf_url,
            "raw_html": response.text
        }

    except Exception as e:
        return {"error": f"Error fetching from Supreme Court: {str(e)}"}
