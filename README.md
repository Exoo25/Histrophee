# 📜 HisTrophee

### Historical events, dates, discoveries, and timelines — all in one desktop app.

HisTrophee is a **PyQt5 desktop application for exploring history** through year-based searches, category filtering, Gregorian/Hijri dates, Wikipedia search, "On This Day" discoveries, statistics, timeline filtering, and CSV export.

Built for people who want to quickly explore **what happened, when it happened, and what else was happening around it.**

---

## 🧭 Navigation

<details>
<summary><b>Jump to a section</b></summary>

* [✨ Features](#-features)
* [🔎 Search](#-search)
* [🌙 Themes](#-themes)
* [🎞️ Timeline](#️-timeline)
* [📅 On This Day](#-on-this-day)
* [📊 Statistics](#-statistics)
* [🌐 Wikipedia Integration](#-wikipedia-integration)
* [🌙 Gregorian & Hijri Calendars](#-gregorian--hijri-calendars)
* [📤 CSV Export](#-csv-export)
* [📖 Event Details](#-event-details)
* [📸 Screenshots](#-screenshots)
* [⚙️ Tech Stack](#️-tech-stack)
* [🚀 Installation](#-installation)

  * [Windows EXE](#windows-exe)
  * [Run From Source](#run-from-source)
  * [Build Your Own EXE](#build-your-own-exe)
* [🔑 API Keys](#-api-keys)
* [🐛 Troubleshooting](#-troubleshooting)
* [🤝 Contributing](#-contributing)
* [📜 License](#-license)

</details>

---

# ✨ Features

## 🔎 Search

Search historical events by year using the **API Ninjas Historical Events API**.

You can combine your search with:

* 📅 Year
* 🌙 Calendar system
* 🏷️ Category
* 🔍 Keyword

For example:

```text
Year: 1947
Calendar: Gregorian
Category: Politics
Search: Pakistan
```

The search results are displayed in a sortable table.

---

## 🏷️ Automatic Categories

HisTrophee automatically analyzes event descriptions and attempts to classify them.

Supported categories include:

| Category       | Examples                                       |
| -------------- | ---------------------------------------------- |
| ⚔️ War         | Battles, invasions, armies, rebellions         |
| 🏛️ Politics   | Governments, elections, treaties, independence |
| 🔬 Science     | Discoveries, experiments, research             |
| 🧭 Exploration | Voyages, expeditions, exploration              |
| ☪️ Religion    | Religious events, prophets, mosques, churches  |
| 💻 Technology  | Computers, inventions, software, machines      |
| 🌋 Disaster    | Earthquakes, floods, tsunamis, eruptions       |
| 🎨 Culture     | Film, music, literature, art                   |
| 📦 Other       | Events that don't match another category       |

The categorization system is lightweight and keyword-based, so it doesn't require a database or machine-learning model.

---

# 🌙 Themes

HisTrophee includes a built-in light/dark theme toggle.

### ☀️ Light Mode

Clean and bright for everyday browsing.

### 🌙 Dark Mode

A darker interface for nighttime research sessions.

No restart is required when switching themes.

---

# 🎞️ Timeline

HisTrophee includes an optional **timeline filter**.

Enable the timeline and use the slider to progressively filter events throughout the year.

For example:

```text
January ──────────────── December
  ▲
  │
  └── Events up to the selected day
```

The timeline can be disabled whenever you want to return to the full-year results.

---

# 📅 On This Day

Don't want to search for a specific year?

Use:

**📅 On This Day**

HisTrophee retrieves historical information for today's date through the Wikimedia On This Day feed.

It can display:

* 📜 Historical events
* 🎂 Births
* 🕊️ Deaths
* 🔗 Related Wikipedia sources

This makes the app useful even when you're just looking for something interesting that happened **on today's date**.

---

# 📊 Statistics

Turn your search results into visual data.

The statistics window currently provides:

### Events by Category

Shows how many results belong to each historical category.

### Events by Month

Shows the distribution of events across the twelve months.

### Total Events

The statistics window also displays the total number of events being analyzed.

> Statistics require **Matplotlib**.

---

# 🌐 Wikipedia Integration

HisTrophee isn't limited to the historical events API.

When you search for a keyword, the application can also search **Wikipedia** for related articles.

Wikipedia results can appear when:

* You perform a keyword search.
* No historical events are found.
* Your filters produce no matching events.

Each Wikipedia result can be opened in a dedicated article dialog.

You can then open the complete article in your browser.

---

# 🌙 Gregorian & Hijri Calendars

HisTrophee supports both:

### 📅 Gregorian

Search using a Gregorian year such as:

```text
1947
```

### 🌙 Hijri

Search using a Hijri year such as:

```text
1366
```

The application converts Hijri year ranges to Gregorian dates and retrieves the corresponding historical events.

Individual events can also display their Hijri date alongside the Gregorian date.

Hijri/Gregorian conversion is handled through the **Aladhan API**.

---

# 📤 CSV Export

Found something useful?

Export the currently visible results using:

**📤 Export CSV**

The exported file contains:

```text
Date
Hijri Date
Event / Article
Category
Description
```

The file is saved using UTF-8 encoding and can be opened in applications such as:

* Microsoft Excel
* LibreOffice Calc
* Google Sheets
* Python
* Other CSV-compatible tools

---

# 📖 Event Details

Double-click an event to open its detailed view.

The details dialog provides:

* 📅 Gregorian date
* 🌙 Hijri date
* 🏷️ Category
* 📚 Source
* 📜 Event description
* 🌐 Source link when available

Wikipedia results have their own dedicated article dialog.

---

# 📸 Screenshots

> Replace these placeholders with your actual screenshots.

## 🏠 Main Interface

![HisTrophee Main Interface](screenshots/main.png)

## 🔎 Historical Search

![Historical Search](screenshots/search.png)

## 📊 Statistics

![Statistics](screenshots/statistics.png)

## 📅 On This Day

![On This Day](screenshots/on-this-day.png)

## 🌙 Dark Mode

![Dark Mode](screenshots/dark-mode.png)

## 🎞️ Timeline

![Timeline](screenshots/timeline.png)

---

# ⚙️ Tech Stack

HisTrophee is built primarily with Python.

| Technology    | Purpose                        |
| ------------- | ------------------------------ |
| 🐍 Python     | Core application               |
| 🖥️ PyQt5     | Desktop GUI                    |
| 🌐 Requests   | API communication              |
| 📊 Matplotlib | Statistics and charts          |
| 📄 CSV        | Result exporting               |
| 📚 API Ninjas | Historical events              |
| 🌐 Wikimedia  | On This Day + Wikipedia search |
| 🌙 Aladhan    | Hijri/Gregorian conversion     |

The application uses `QThread` to perform network operations without freezing the main interface.

---

# 🚀 Installation

There are two main ways to use HisTrophee.

## Windows EXE

If you only want to use the application, download the latest Windows executable from the project's **Releases** page.

### 1. Download

Download:

```text
HisTrophee.exe
```

### 2. Run

Double-click the executable.

Python does **not** need to be installed separately when using the packaged executable.

### 3. API Key

You will still need to configure your API key if the distributed build requires one.

See [API Keys](#-api-keys).

---

## Run From Source

### Requirements

You need:

* Python 3.10+
* An API Ninjas API key
* Internet connection

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/HisTrophee.git
cd HisTrophee
```

Install the dependencies:

```bash
pip install PyQt5 requests matplotlib
```

Then run:

```bash
python main.py
```

---

## Build Your Own EXE

HisTrophee can be packaged into a Windows executable using **PyInstaller**.

Install PyInstaller:

```bash
pip install pyinstaller
```

Then build:

```bash
pyinstaller --onefile --windowed main.py
```

The executable will be created inside:

```text
dist/
```

So you'll find:

```text
dist/main.exe
```

You can rename it to:

```text
HisTrophee.exe
```

### Recommended Build

For a cleaner release:

```bash
pyinstaller --onefile --windowed --name HisTrophee main.py
```

This produces:

```text
dist/
└── HisTrophee.exe
```

---

# 🔑 API Keys

HisTrophee uses the following external services:

### API Ninjas

Used for historical event retrieval.

You need an API Ninjas API key for the historical events search.

The application sends it through the request header:

```python
"X-Api-Key": API_KEY
```

### Aladhan

Used for:

* Hijri → Gregorian conversion
* Gregorian → Hijri conversion

No Aladhan API key is required by the current implementation.

### Wikimedia

Used for:

* Wikipedia search
* On This Day

No Wikimedia API key is required by the current implementation.

---

## ⚠️ Security Note

**Do not commit your real API key to a public GitHub repository.**

For development, keep your API key outside the repository or load it through an environment variable.

For example:

```python
import os

API_KEY = os.getenv("API_NINJAS_API_KEY")
```

Then configure the environment variable before running the application.

---

# 🐛 Troubleshooting

## ❌ "Invalid API Key"

Check that your API Ninjas key is correct and active.

---

## ❌ "Rate Limited"

API Ninjas may have rejected the request because the API rate limit was reached.

Wait before trying again.

---

## ❌ No Results

Try:

* Removing the category filter.
* Removing the keyword.
* Searching another year.
* Checking your internet connection.
* Using the Wikipedia fallback search.

---

## ❌ Statistics Don't Appear

Make sure Matplotlib is installed:

```bash
pip install matplotlib
```

---

## ❌ Connection Error

HisTrophee relies on online APIs.

Make sure your computer has an active internet connection and that the relevant services are reachable.

---

# 🧠 How It Works

The general search pipeline looks like this:

```text
                 ┌──────────────┐
                 │    User      │
                 │ enters query │
                 └──────┬───────┘
                        │
                        ▼
                ┌───────────────┐
                │    HisTrophee │
                │    PyQt5 GUI  │
                └───────┬───────┘
                        │
                        ▼
                ┌───────────────┐
                │   API Worker  │
                │   QThread     │
                └───────┬───────┘
                        │
              ┌─────────┼─────────┐
              ▼         ▼         ▼
        API Ninjas   Aladhan   Wikimedia
              │         │         │
              └─────────┼─────────┘
                        ▼
                ┌───────────────┐
                │ Process &     │
                │ categorize    │
                │ results       │
                └───────┬───────┘
                        │
                        ▼
                ┌───────────────┐
                │ Results Table │
                └───────┬───────┘
                        │
             ┌──────────┼──────────┐
             ▼          ▼          ▼
          Details   Statistics   CSV
```

Network requests are handled in a worker thread so the main PyQt5 interface can remain responsive while searches are running.

---

# 📁 Project Structure

A simple project layout can look like:

```text
HisTrophee/
│
├── main.py
├── README.md
├── requirements.txt
├── LICENSE
│
├── screenshots/
│   ├── main.png
│   ├── search.png
│   ├── statistics.png
│   ├── on-this-day.png
│   ├── timeline.png
│   └── dark-mode.png
│
└── dist/
    └── HisTrophee.exe
```

---

# 📦 Requirements

A `requirements.txt` file can contain:

```text
PyQt5
requests
matplotlib
```

Install everything with:

```bash
pip install -r requirements.txt
```

---

# 🔐 Privacy

HisTrophee does not require a personal account or local database.

However, searches and conversions may send information such as:

* Requested year
* Search terms
* API requests

to the external services used by the application.

Review the respective service policies before distributing the application commercially.

---

# 🤝 Contributing

Contributions are welcome!

If you find a bug or have an idea:

1. Open an issue.
2. Explain the problem or feature.
3. Include reproduction steps when reporting bugs.
4. Submit a pull request if you want to implement the change.

Please keep contributions focused and maintainable.

---

# 🗺️ Roadmap

Potential future improvements include:

* [ ] More advanced historical filtering
* [ ] Better event categorization
* [ ] More calendar systems
* [ ] Improved timeline visualization
* [ ] Historical maps
* [ ] More statistical visualizations
* [ ] Better source information
* [ ] Search history
* [ ] Additional export formats
* [ ] Improved API error handling

---

# 📜 License

This project is licensed under the **MIT License**.

See [`LICENSE`](LICENSE) for the full license text.

---

# ⭐ Support the Project

If you find HisTrophee useful:

⭐ Star the repository
🐛 Report bugs
💡 Suggest features
🔀 Contribute improvements

Every bit of support helps the project grow.

---

<div align="center">

### 📜 HisTrophee

**Explore the past. Discover the story.**

Made with 🐍 Python + 🖥️ PyQt5

</div>
