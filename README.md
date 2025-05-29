# 📊 Yahoo Breaking News Crawler
This project is a Scrapy-based web crawler that fetches the latest breaking news from Yahoo Taiwan News using their internal API. It extracts structured data including the news title, author, publish time, and URL.

<br>

## 📌 Features
- Fetches Yahoo Taiwan breaking news via internal API
- Retrieves 50 articles per request and paginates automatically (up to 500 by default)
- Extracted fields:
  - title :   news headline
  - author :  news provider
  - time :    publish time
  - link :    full article URL

<br>

## 🛠️ Tech Stack
| Tool / Library         | Purpose                                       |
| ---------------------- | --------------------------------------------- |
| **Python 3.x**         | Core programming language                     |
| **Scrapy**             | Web crawling framework                        |
| **JSON**               | Data format for output/export                 |
| **Yahoo Internal API** | Source of breaking news data                  |
| **datetime module**    | Parsing and formatting timestamps             |
| **urllib.parse**       | Encoding request parameters (e.g., `quote()`) |
| **User-Agent headers** | Mimics browser behavior for access            |

<br>

## 📁 Project Structure
```md
/yahoo_news_spider/
├── yahoo_news_spider/            # Main App Package
│   ├── __init__.py
│   ├── items.py                  # Defines the output fields
│   ├── middlewares.py
│   ├── pipelines.py              # Process items (Ex. export csv file)
│   ├── settings.py               # Scrapy settings
│   └── spiders/
│       └── yahoo_break_news.py   # Main spider script
├── output/
│   └── yahoo_breaking_news_(starttime)_(endtime).csv
├── log.txt                       # Record Process
├── scrapy.cfg                    # Scrapy configuration file for managing the project and spider entry points 
├── test.py                       # A test script to manually run and inspect the spider or logic
└── README.md                     # Project documentation and usage guide

```
<br>

## ⚠️ Notes

- This spider relies on Yahoo Taiwan’s internal API. If the API structure or parameters change in the future, code updates may be necessary.
- Please follow Yahoo's robots.txt and terms of service when using this crawler.
<br>

## 📬 Contact
Feel free to reach out via the contact form on the site or connect with me on [My Email](mimilee2733@gmail.com).
