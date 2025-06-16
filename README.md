# Python Job Scraper 🚀

A simple yet powerful Python script to scrape job listings from [python.org/jobs](https://www.python.org/jobs/) based on location and posting date.

---

## 🌐 Overview

This tool helps you:

* Search for Python jobs by location.
* Filter jobs by how recently they were posted (today, this week, or this month).
* Automatically navigate through multiple pages of listings.

---

## 📚 Features

* Scrapes job title, company, location, job type, posting date, and application link.
* Supports filtering by:

  * Location (case-insensitive)
  * Date posted (last 1 day, 7 days, or 30 days)
* Auto-pagination: Scrapes jobs across all pages.

---

## 📦 Requirements

Make sure you have the following Python packages installed:

```bash
pip install requests beautifulsoup4
```

---

## 💡 How It Works

1. User is prompted for:

   * Desired job location
   * Time range to filter by (1 = day, 2 = week, 3 = month)
2. The script fetches job listings from python.org.
3. Matches jobs are printed with details.
4. Script continues scraping until there are no more pages.

---

## 📝 Example Output

```bash
Enter location you want to work in: Remote
Enter posted within:
1 = Day
2 = Week
3 = Month
Choice: 2

Details for job 1 on page 1:
Job Info
Title         : Senior Back-End Python Engineer
Company name  : Active Prime
Locations     : Remote, Remote, Remote
Date posted   : 12 June 2025
Apply link    : https://www.python.org/jobs/7913/
----------------------------------------
```

---

## 🎓 Educational Value

This project is great for learning:

* Web scraping with `BeautifulSoup`
* Pagination handling
* Date/time comparison
* Modular Python scripting

---

## 🚫 Disclaimer

This scraper is designed for educational and personal use only. Be respectful to `python.org`'s terms of service.

---

## 🚀 Future Improvements

* Export results to CSV/JSON
* Add keyword search
* Use command-line arguments (via `argparse`)
* Add GUI with `Tkinter` or `Streamlit`

---

## 🌟 Author

Made with ❤️ by Shivam, a Data Engineering student passionate about Python and automation.

---

## ✅ License

MIT License. Free to use and modify.
