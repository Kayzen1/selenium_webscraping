# 🎉 Doctor Reviews Scraper

This project is a web scraper built using Python and Selenium to extract detailed doctor reviews and ratings from a medical website for further research purpose. The scraper collects data such as doctor names, specialties, ratings, and user comments, and saves the results into a CSV file.

---

## 📍 Features
- **Dynamic Web Scraping**: Extracts multiple pages of data using Selenium.
- **Multithreading**: Accelerates scraping by processing multiple pages concurrently with `ThreadPoolExecutor`.
- **Comprehensive Data**: Collects doctor details, reviews, tags, and ratings.
- **Custom Handling**: Handles ads, cookies, and dynamically loaded content.

---

## 🔌 Installation

### Prerequisites
1. Install Python (3.7 or higher).
2. Install Google Chrome and download the appropriate version of [ChromeDriver](https://chromedriver.chromium.org/downloads).
3. Install required Python libraries:
   ```bash
   pip install selenium tqdm

---

## 📄 File Structure
```
project/
├──
├── chromedriver  # ChromeDriver executable
├── scraper.py    # Main Python script
├── doctor.csv    # Output CSV file
```

---

## Usage

### 1. Set Up ChromeDriver  
Update the `PATH` in the `get_driver()` function with the location of your ChromeDriver:
```python
PATH = "/path/to/your/chromedriver"
```

### 2. Run the Script
Execute the script in the terminal:
```bash
python scraper.py
```

### 3. Output
The extracted data will be saved in doctor.csv with the following columns:

- d_name: Doctor's name
- d_speciality: Doctor's specialty
- total_score: Overall rating score
- total_survey_count: Total number of surveys
- five_star, four_star, three_star, two_star, one_star: Number and percentage for each rating category
- positive_tags, negative_tags: Lists of positive and negative tags
- comment_text: User comments

---

## Code Structure

### Functions
- iselement(browser, cssselector)
Checks if an element exists on the webpage.

- get_driver()
Sets up and returns a Selenium WebDriver instance.

- get_doc_linklist(url)
Scrapes doctor profile links from multiple pages.

- get_doctor_details(link)
Extracts detailed information from each doctor's profile page.

### Multithreading
Uses ThreadPoolExecutor to scrape multiple doctor profiles simultaneously:

```python
with ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(get_doctor_details, link_list)
```

---

## Handling Common Issues
### 1. Ad Popups
Automatically closes popups that obstruct scraping.
### 2. Cookies
Handles cookie popups that block interaction.
### 3. Pagination
Navigates through multiple pages until the specified limit (99 pages).

---

## Output
Here is the link to the [output](doctor.csv)
