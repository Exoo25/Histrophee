##########################################
#             HISTROPHEE - V1            #
#               SOURCE CODE              #
##########################################

import sys
import csv
import html
import webbrowser
import requests

from datetime import date, timedelta, datetime

from PyQt5.QtCore import (
    Qt,
    QThread,
    pyqtSignal
)
from PyQt5.QtWidgets import QShortcut
from PyQt5.QtGui import QKeySequence

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QFileDialog,
    QHeaderView,
    QDialog,
    QTextEdit,
    QCheckBox,
    QSlider,
    QGroupBox,
    QSpinBox
)

try:
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
    from matplotlib.figure import Figure

    MATPLOTLIB_AVAILABLE = True

except ImportError:
    MATPLOTLIB_AVAILABLE = False

API_KEY = "aehJR+HvQkF1jXQghQaC3g==X5fqDvt3X5Uw8kQs"

API_URL = (
    "https://api.api-ninjas.com/v1/historicalevents"
)

ALADHAN_H2G_URL = (
    "https://api.aladhan.com/v1/hToG"
)

ALADHAN_G2H_URL = (
    "https://api.aladhan.com/v1/gToH"
)

WIKIPEDIA_URL = (
    "https://en.wikipedia.org/w/rest.php/v1/search/page"
)

ON_THIS_DAY_URL = (
    "https://api.wikimedia.org/feed/v1/wikipedia/en/onthisday/all"
)

def detect_category(text):

    text = text.lower()

    categories = {

        "War": [
            "war",
            "battle",
            "siege",
            "army",
            "military",
            "invasion",
            "troops",
            "soldiers",
            "revolt",
            "rebellion",
            "conflict"
        ],

        "Politics": [
            "president",
            "king",
            "queen",
            "government",
            "election",
            "treaty",
            "republic",
            "minister",
            "parliament",
            "political",
            "dynasty",
            "independence",
            "movement",
            "partition",
            "congress"
        ],

        "Science": [
            "scientist",
            "science",
            "experiment",
            "physics",
            "chemistry",
            "astronomy",
            "discovery",
            "discovered",
            "research"
        ],

        "Exploration": [
            "explorer",
            "exploration",
            "voyage",
            "expedition",
            "landing",
            "landed",
            "sailing"
        ],

        "Religion": [
            "prophet",
            "caliph",
            "pope",
            "church",
            "mosque",
            "religion",
            "religious",
            "islam",
            "muslim"
        ],

        "Disaster": [
            "earthquake",
            "flood",
            "tsunami",
            "eruption",
            "hurricane",
            "tornado",
            "disaster"
        ],

        "Technology": [
            "computer",
            "internet",
            "software",
            "technology",
            "invention",
            "telephone",
            "engine",
            "machine",
            "rocket"
        ],

        "Culture": [
            "film",
            "movie",
            "music",
            "novel",
            "artist",
            "literature",
            "festival",
            "painting",
            "album"
        ]
    }

    for category, keywords in categories.items():

        for keyword in keywords:

            if keyword in text:
                return category

    return "Other"

class DetailsDialog(QDialog):

    def __init__(
        self,
        event,
        parent=None
    ):

        super().__init__(parent)

        self.setWindowTitle(
            "Event Details"
        )

        self.resize(
            750,
            550
        )

        layout = QVBoxLayout(
            self
        )

        title = QLabel(
            event["event"]
        )

        title.setWordWrap(
            True
        )

        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            padding: 10px;
        """)

        info = QLabel(
            f"📅 Gregorian: {event.get('date', 'Unknown')}\n"
            f"🌙 Hijri: {event.get('hijri', 'Unknown')}\n"
            f"🏷 Category: {event.get('category', 'Other')}\n"
            f"📚 Source: {event.get('source', 'Unknown')}"
        )

        info.setStyleSheet(
            "font-size: 14px; padding: 8px;"
        )

        description = QTextEdit()

        description.setReadOnly(
            True
        )

        description.setPlainText(
            event.get(
                "description",
                event["event"]
            )
        )

        layout.addWidget(
            title
        )

        layout.addWidget(
            info
        )

        layout.addWidget(
            description
        )

        source_url = event.get(
            "url",
            ""
        )

        if source_url:

            open_button = QPushButton(
                "🌐 Open Source"
            )

            open_button.clicked.connect(
                lambda: webbrowser.open(source_url)
            )

            layout.addWidget(
                open_button
            )

class WikipediaDialog(QDialog):

    def __init__(
        self,
        article,
        parent=None
    ):

        super().__init__(parent)

        self.article = article

        self.setWindowTitle(
            "Wikipedia Article"
        )

        self.resize(
            800,
            600
        )

        layout = QVBoxLayout(
            self
        )

        title = QLabel(
            article["title"]
        )

        title.setWordWrap(
            True
        )

        title.setStyleSheet("""
            font-size: 25px;
            font-weight: bold;
            padding: 10px;
        """)

        description = QLabel(
            article.get(
                "description",
                "No description available."
            )
        )

        description.setWordWrap(
            True
        )

        description.setStyleSheet("""
            font-size: 15px;
            padding: 8px;
        """)

        excerpt = QTextEdit()

        excerpt.setReadOnly(
            True
        )

        excerpt.setHtml(
            article.get(
                "excerpt",
                "No excerpt available."
            )
        )

        open_button = QPushButton(
            "🌐 Open Wikipedia Article"
        )

        open_button.clicked.connect(
            self.open_article
        )

        layout.addWidget(
            title
        )

        layout.addWidget(
            description
        )

        layout.addWidget(
            excerpt
        )

        layout.addWidget(
            open_button
        )

    def open_article(self):

        url = self.article.get(
            "url",
            ""
        )

        if url:

            webbrowser.open(
                url
            )

class StatisticsDialog(QDialog):

    def __init__(
        self,
        events,
        parent=None
    ):

        super().__init__(parent)

        self.events = events

        self.setWindowTitle(
            "📊 Historical Statistics"
        )

        self.resize(
            1000,
            750
        )

        layout = QVBoxLayout(
            self
        )

        title = QLabel(
            "📊 Historical Statistics"
        )

        title.setStyleSheet("""
            font-size: 25px;
            font-weight: bold;
            padding: 10px;
        """)

        layout.addWidget(
            title
        )

        if not MATPLOTLIB_AVAILABLE:

            message = QLabel(
                "Matplotlib is not installed.\n\n"
                "Install it with:\n"
                "pip install matplotlib"
            )

            message.setStyleSheet(
                "font-size: 16px; padding: 20px;"
            )

            layout.addWidget(
                message
            )

            return

        category_counts = {}

        for event in events:

            category = event.get(
                "category",
                "Other"
            )

            category_counts[category] = (
                category_counts.get(
                    category,
                    0
                ) + 1
            )

        categories = list(
            category_counts.keys()
        )

        category_values = [
            category_counts[x]
            for x in categories
        ]

        month_counts = {
            month: 0
            for month in range(1, 13)
        }

        for event in events:

            try:

                month = int(
                    event.get(
                        "month",
                        0
                    )
                )

                if 1 <= month <= 12:

                    month_counts[month] += 1

            except:

                pass

        month_names = [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec"
        ]

        month_values = [
            month_counts[x]
            for x in range(1, 13)
        ]

        self.figure1 = Figure(
            figsize=(8, 4)
        )

        self.canvas1 = FigureCanvasQTAgg(
            self.figure1
        )

        ax1 = self.figure1.add_subplot(
            111
        )

        ax1.bar(
            categories,
            category_values
        )

        ax1.set_title(
            "Events by Category"
        )

        ax1.set_ylabel(
            "Number of Events"
        )

        ax1.tick_params(
            axis="x",
            rotation=35
        )

        self.figure1.tight_layout()

        layout.addWidget(
            self.canvas1
        )

        self.figure2 = Figure(
            figsize=(8, 4)
        )

        self.canvas2 = FigureCanvasQTAgg(
            self.figure2
        )

        ax2 = self.figure2.add_subplot(
            111
        )

        ax2.plot(
            month_names,
            month_values,
            marker="o"
        )

        ax2.set_title(
            "Events by Month"
        )

        ax2.set_ylabel(
            "Number of Events"
        )

        self.figure2.tight_layout()

        layout.addWidget(
            self.canvas2
        )

        total = QLabel(
            f"Total events analyzed: {len(events)}"
        )

        total.setStyleSheet(
            "font-size: 15px; font-weight: bold;"
        )

        layout.addWidget(
            total
        )

class APIWorker(QThread):

    events_ready = pyqtSignal(
        list
    )

    wikipedia_ready = pyqtSignal(
        list,
        str
    )

    on_this_day_ready = pyqtSignal(
        list
    )

    error = pyqtSignal(
        str,
        str
    )

    status = pyqtSignal(
        str
    )

    def __init__(
        self,
        year,
        calendar,
        category,
        search_text,
        on_this_day=False
    ):

        super().__init__()

        self.year = year

        self.calendar = calendar

        self.category = category

        self.search_text = search_text

        self.on_this_day = on_this_day

    def run(self):

        try:

            if self.on_this_day:

                self.load_on_this_day()

                return

            if self.calendar == "Hijri":

                self.status.emit(
                    "Converting Hijri year..."
                )

                date_range = (
                    self.get_hijri_year_range(
                        self.year
                    )
                )

                if date_range is None:

                    self.error.emit(
                        "Hijri Conversion Error",
                        "Could not convert this Hijri year."
                    )

                    return

                start_date, end_date = (
                    date_range
                )

                years = range(
                    start_date.year,
                    end_date.year + 1
                )


            else:

                if not (-500 <= self.year <= 2022):
                    self.error.emit(

                        "Invalid Year",

                        "Gregorian year must be between -500 and 2022."

                    )

                    return

                years = [

                    self.year

                ]

                # Python's datetime.date cannot represent BCE years.

                # Only create date objects for normal Gregorian years.

                if self.year >= 1:

                    start_date = date(

                        self.year,

                        1,

                        1

                    )

                    end_date = date(

                        self.year,

                        12,

                        31

                    )

                else:

                    start_date = None

                    end_date = None
            all_events = []

            for api_year in years:

                self.status.emit(
                    f"Fetching events for {api_year}..."
                )

                response = requests.get(
                    API_URL,
                    headers={
                        "X-Api-Key": API_KEY
                    },
                    params={
                        "year": api_year
                    },
                    timeout=15
                )

                if response.status_code == 401:

                    self.error.emit(
                        "Invalid API Key",
                        "API Ninjas rejected your API key."
                    )

                    return

                if response.status_code == 403:

                    self.error.emit(
                        "Access Denied",
                        "Your API key does not have access."
                    )

                    return

                if response.status_code == 429:

                    self.error.emit(
                        "Rate Limited",
                        "API Ninjas rate limit reached."
                    )

                    return

                response.raise_for_status()
                print("API REQUEST FINISHED", response.status_code)


                data = response.json()
                print("API DATA:", data)

                if isinstance(
                    data,
                    list
                ):

                    all_events.extend(
                        data
                    )

            events = []

            hijri_cache = {}

            for item in all_events:

                event_text = str(
                    item.get(
                        "event",
                        ""
                    )
                ).strip()

                if not event_text:

                    continue

                try:

                    event_year = int(
                        item.get(
                            "year",
                            0
                        )
                    )

                except:

                    continue

                try:

                    month = int(
                        item.get(
                            "month",
                            0
                        )
                    )

                except:

                    month = 0

                try:

                    day = int(
                        item.get(
                            "day",
                            0
                        )
                    )

                except:

                    day = 0

                if not (
                    1 <= month <= 12
                    and
                    1 <= day <= 31
                ):

                    continue

                try:

                    current_date = date(
                        event_year,
                        month,
                        day
                    )

                except:

                    continue

                if self.calendar == "Hijri":

                    if not (
                        start_date
                        <= current_date
                        <= end_date
                    ):

                        continue

                cache_key = (
                    event_year,
                    month,
                    day
                )

                if cache_key not in hijri_cache:

                    self.status.emit(
                        f"Converting {current_date.isoformat()}..."
                    )

                    hijri_cache[
                        cache_key
                    ] = self.to_hijri(
                        event_year,
                        month,
                        day
                    )

                hijri_date = hijri_cache[
                    cache_key
                ]

                category = detect_category(
                    event_text
                )

                events.append({

                    "year":
                        event_year,

                    "month":
                        month,

                    "day":
                        day,

                    "date":
                        self.format_date(
                            event_year,
                            month,
                            day
                        ),

                    "hijri":
                        hijri_date,

                    "event":
                        event_text,

                    "category":
                        category,

                    "description":
                        event_text,

                    "source":
                        "API Ninjas",

                    "url":
                        ""
                })

            unique = {}

            for event in events:

                key = (
                    event["year"],
                    event["month"],
                    event["day"],
                    event["event"].lower()
                )

                unique[key] = event

            events = list(
                unique.values()
            )

            self.events_ready.emit(
                events
            )

            query_parts = []

            if self.search_text:

                query_parts.append(
                    self.search_text
                )

            query_parts.append(
                str(self.year)
            )

            if self.category != "All":

                query_parts.append(
                    self.category
                )

            wiki_query = f"Events happened in {self.year}"

            matching_events = self.filter_events(
                events
            )

            should_search_wikipedia = (
                    bool(self.search_text)
                    or not events
            )

            if should_search_wikipedia:

                self.status.emit(
                    f"Searching Wikipedia for: {wiki_query}"
                )

                articles = (
                    self.search_wikipedia(
                        wiki_query
                    )
                )

                self.wikipedia_ready.emit(
                    articles,
                    wiki_query
                )

        except requests.exceptions.Timeout:

            self.error.emit(
                "Timeout",
                "A network request took too long."
            )

        except requests.exceptions.ConnectionError:

            self.error.emit(
                "Connection Error",
                "Could not connect to an API."
            )

        except requests.exceptions.RequestException as error:

            self.error.emit(
                "API Error",
                str(error)
            )

        except Exception as error:

            self.error.emit(
                "Unexpected Error",
                str(error)
            )

    def load_on_this_day(self):

        today = date.today()

        self.status.emit(
            f"Loading events for {today.strftime('%B %d')}..."
        )

        url = (
            f"{ON_THIS_DAY_URL}/"
            f"{today.month:02d}/"
            f"{today.day:02d}"
        )

        response = requests.get(
            url,
            timeout=15,
            headers={
                "User-Agent":
                    "HisTrophee/2.0"
            }
        )

        response.raise_for_status()
        self.status.emit(
            f"HTTP status: {response.status_code}"
        )

        data = response.json()

        self.status.emit(
            f"API returned {len(data)} results"
        )




        events = []

        for item in data.get(
            "events",
            []
        ):

            year = item.get(
                "year",
                ""
            )

            text = item.get(
                "text",
                ""
            )

            pages = item.get(
                "pages",
                []
            )

            url = ""

            if pages:

                page = pages[0]

                content_urls = page.get(
                    "content_urls",
                    {}
                )

                desktop = content_urls.get(
                    "desktop",
                    {}
                )

                url = desktop.get(
                    "page",
                    ""
                )

            events.append({

                "year":
                    year,

                "month":
                    today.month,

                "day":
                    today.day,

                "date":
                    f"{today.strftime('%B %d')} "
                    f"({year})",

                "hijri":
                    "",

                "event":
                    text,

                "category":
                    detect_category(
                        text
                    ),

                "description":
                    text,

                "source":
                    "Wikimedia On This Day",

                "url":
                    url
            })

        for item in data.get(
            "births",
            []
        ):

            year = item.get(
                "year",
                ""
            )

            text = item.get(
                "text",
                ""
            )

            pages = item.get(
                "pages",
                []
            )

            url = ""

            if pages:

                content_urls = pages[0].get(
                    "content_urls",
                    {}
                )

                desktop = content_urls.get(
                    "desktop",
                    {}
                )

                url = desktop.get(
                    "page",
                    ""
                )

            events.append({

                "year":
                    year,

                "month":
                    today.month,

                "day":
                    today.day,

                "date":
                    f"{today.strftime('%B %d')} "
                    f"({year})",

                "hijri":
                    "",

                "event":
                    "🎂 Birth: " + text,

                "category":
                    "Culture",

                "description":
                    text,

                "source":
                    "Wikimedia On This Day",

                "url":
                    url
            })

        for item in data.get(
            "deaths",
            []
        ):

            year = item.get(
                "year",
                ""
            )

            text = item.get(
                "text",
                ""
            )

            pages = item.get(
                "pages",
                []
            )

            url = ""

            if pages:

                content_urls = pages[0].get(
                    "content_urls",
                    {}
                )

                desktop = content_urls.get(
                    "desktop",
                    {}
                )

                url = desktop.get(
                    "page",
                    ""
                )

            events.append({

                "year":
                    year,

                "month":
                    today.month,

                "day":
                    today.day,

                "date":
                    f"{today.strftime('%B %d')} "
                    f"({year})",

                "hijri":
                    "",

                "event":
                    "🕊 Death: " + text,

                "category":
                    detect_category(
                        text
                    ),

                "description":
                    text,

                "source":
                    "Wikimedia On This Day",

                "url":
                    url
            })

        self.on_this_day_ready.emit(
            events
        )

    def filter_events(
        self,
        events
    ):

        search = (
            self.search_text
            .lower()
            .strip()
        )

        result = []

        for event in events:

            if (
                self.category != "All"
                and
                event["category"]
                != self.category
            ):

                continue

            if search:

                searchable = (
                    event["event"]
                    + " "
                    + event["category"]
                ).lower()

                if search not in searchable:

                    continue

            result.append(
                event
            )

        return result

    def get_hijri_year_range(
        self,
        hijri_year
    ):

        try:

            start = (
                self.hijri_to_gregorian(
                    hijri_year,
                    1,
                    1
                )
            )

            next_year = (
                self.hijri_to_gregorian(
                    hijri_year + 1,
                    1,
                    1
                )
            )

            if (
                start is None
                or
                next_year is None
            ):

                return None

            end = (
                next_year
                - timedelta(
                    days=1
                )
            )

            return (
                start,
                end
            )

        except:

            return None

    def hijri_to_gregorian(
        self,
        year,
        month,
        day
    ):

        response = requests.get(
            ALADHAN_H2G_URL,
            params={
                "date":
                    f"{day}-{month}-{year}"
            },
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        if data.get(
            "code"
        ) != 200:

            return None

        gregorian = (
            data["data"]["gregorian"]
        )

        return date(
            int(
                gregorian["year"]
            ),
            int(
                gregorian["month"]["number"]
            ),
            int(
                gregorian["day"]
            )
        )

    def to_hijri(
        self,
        year,
        month,
        day
    ):

        try:

            response = requests.get(
                ALADHAN_G2H_URL,
                params={
                    "date":
                        f"{day:02d}-"
                        f"{month:02d}-"
                        f"{year}"
                },
                timeout=15
            )

            response.raise_for_status()

            data = response.json()

            if data.get(
                "code"
            ) != 200:

                return ""

            hijri = (
                data["data"]["hijri"]
            )

            return (
                f"{hijri['day']} "
                f"{hijri['month']['en']} "
                f"{hijri['year']} AH"
            )

        except:

            return ""

    def search_wikipedia(
        self,
        query
    ):

        if not query:

            query = (
                f"{self.year} historical events"
            )

        response = requests.get(
            WIKIPEDIA_URL,
            headers={
                "User-Agent":
                    "HistoricalEventsExplorer/2.0"
            },
            params={
                "q": query,
                "limit": 12
            },
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        pages = data.get(
            "pages",
            []
        )

        articles = []

        for page in pages:

            title = page.get(
                "title",
                "Untitled"
            )

            description = page.get(
                "description",
                ""
            )

            excerpt = page.get(
                "excerpt",
                ""
            )

            excerpt = html.unescape(
                excerpt
            )

            article = {

                "title":
                    title,

                "description":
                    description,

                "excerpt":
                    excerpt,

                "url":
                    "https://en.wikipedia.org/wiki/"
                    +
                    title.replace(
                        " ",
                        "_"
                    )
            }

            articles.append(
                article
            )

        return articles

    def format_date(
        self,
        year,
        month,
        day
    ):

        months = [

            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December"
        ]

        return (
            f"{months[month - 1]} "
            f"{day}, "
            f"{year}"
        )

class HistoricalEventsApp(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "Historical Events Explorer"
        )

        self.resize(
            1350,
            800
        )

        self.events = []

        self.wikipedia_articles = []

        self.on_this_day_events = []

        self.worker = None

        self.dark_mode = False

        self.timeline_enabled = False

        self.timeline_day = 365

        self.build_ui()

        self.apply_theme()

    def build_ui(self):

        main = QVBoxLayout(
            self
        )

        title_row = QHBoxLayout()

        title = QLabel(
            "📜 HisTrophee"
        )

        title.setStyleSheet("""
            font-size: 30px;
            font-weight: bold;
            padding: 12px;
        """)

        title_row.addWidget(
            title
        )

        title_row.addStretch()

        self.theme_button = QPushButton(
            "🌙 Dark"
        )

        self.theme_button.clicked.connect(
            self.toggle_theme
        )

        title_row.addWidget(
            self.theme_button
        )

        main.addLayout(
            title_row
        )

        controls = QHBoxLayout()

        controls.addWidget(
            QLabel("Year:")
        )

        self.year_input = QLineEdit()
        def surprise_me():
            import random
            a = random.randint(1,2022)
            self.year_input.setText(str(a))

        self.random_button = QPushButton("🎲 Random Year")
        self.random_button.clicked.connect(surprise_me)
        controls.addWidget(self.random_button)

        shortcut = QShortcut(QKeySequence("Ctrl+R"), self)
        shortcut.activated.connect(surprise_me)
        self.year_input.setPlaceholderText(
            "Example: 1947"
        )

        self.year_input.setFixedWidth(
            130
        )

        controls.addWidget(
            self.year_input
        )

        controls.addWidget(
            QLabel("Calendar:")
        )

        self.calendar_box = QComboBox()

        self.calendar_box.addItems([
            "Gregorian",
            "Hijri"
        ])

        controls.addWidget(
            self.calendar_box
        )

        controls.addWidget(
            QLabel("Category:")
        )

        self.category_box = QComboBox()

        self.category_box.addItems([

            "All",
            "War",
            "Politics",
            "Science",
            "Exploration",
            "Religion",
            "Technology",
            "Disaster",
            "Culture",
            "Other"
        ])

        controls.addWidget(
            self.category_box
        )

        self.search_input = QLineEdit()

        self.search_input.setPlaceholderText(
            "Search events or Wikipedia..."
        )

        controls.addWidget(
            self.search_input
        )

        self.search_button = QPushButton(
            "🔎 Search"
        )

        self.search_button.clicked.connect(
            self.load_events
        )

        controls.addWidget(
            self.search_button
        )

        self.today_button = QPushButton(
            "📅 On This Day"
        )

        self.today_button.setToolTip(
            "Show historical events, births and deaths for today's date."
        )

        self.today_button.clicked.connect(
            self.load_on_this_day
        )

        controls.addWidget(
            self.today_button
        )

        self.stats_button = QPushButton(
            "📊 Statistics"
        )

        self.stats_button.clicked.connect(
            self.show_statistics
        )

        controls.addWidget(
            self.stats_button
        )

        main.addLayout(
            controls
        )

        timeline_group = QGroupBox(
            "🎞️ Timeline"
        )

        timeline_layout = QVBoxLayout(
            timeline_group
        )

        timeline_top = QHBoxLayout()

        self.timeline_check = QCheckBox(
            "Enable timeline filter"
        )

        self.timeline_check.toggled.connect(
            self.timeline_toggled
        )

        timeline_top.addWidget(
            self.timeline_check
        )

        timeline_top.addStretch()

        self.timeline_label = QLabel(
            "Full year"
        )

        timeline_top.addWidget(
            self.timeline_label
        )

        timeline_layout.addLayout(
            timeline_top
        )

        self.timeline_slider = QSlider(
            Qt.Horizontal
        )

        self.timeline_slider.setMinimum(
            1
        )

        self.timeline_slider.setMaximum(
            365
        )

        self.timeline_slider.setValue(
            365
        )

        self.timeline_slider.setEnabled(
            False
        )

        self.timeline_slider.valueChanged.connect(
            self.timeline_changed
        )

        timeline_layout.addWidget(
            self.timeline_slider
        )

        timeline_dates = QHBoxLayout()

        timeline_dates.addWidget(
            QLabel("Jan 1")
        )

        timeline_dates.addStretch()

        timeline_dates.addWidget(
            QLabel("Dec 31")
        )

        timeline_layout.addLayout(
            timeline_dates
        )

        main.addWidget(
            timeline_group
        )

        self.status = QLabel(
            "Enter a year and press Search."
        )

        self.status.setStyleSheet(
            "padding: 5px;"
        )

        main.addWidget(
            self.status
        )

        self.table = QTableWidget()

        self.table.setColumnCount(
            5
        )

        self.table.setHorizontalHeaderLabels([

            "Date",
            "Hijri Date",
            "Event / Article",
            "Category",
            "Description"
        ])

        self.table.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        self.table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        self.table.setWordWrap(
            True
        )

        header = (
            self.table.horizontalHeader()
        )

        header.setSectionResizeMode(
            0,
            QHeaderView.ResizeToContents
        )

        header.setSectionResizeMode(
            1,
            QHeaderView.ResizeToContents
        )

        header.setSectionResizeMode(
            2,
            QHeaderView.ResizeToContents
        )

        header.setSectionResizeMode(
            3,
            QHeaderView.ResizeToContents
        )

        header.setSectionResizeMode(
            4,
            QHeaderView.Stretch
        )

        self.table.cellDoubleClicked.connect(
            self.show_details
        )

        main.addWidget(
            self.table
        )

        bottom = QHBoxLayout()

        self.count_label = QLabel(
            "0 events"
        )

        bottom.addWidget(
            self.count_label
        )

        bottom.addStretch()

        export_button = QPushButton(
            "📤 Export CSV"
        )

        export_button.clicked.connect(
            self.export_csv
        )

        bottom.addWidget(
            export_button
        )

        clear_button = QPushButton(
            "🗑 Clear"
        )

        clear_button.clicked.connect(
            self.clear
        )

        bottom.addWidget(
            clear_button
        )

        main.addLayout(
            bottom
        )

        self.category_box.currentTextChanged.connect(
            self.apply_filters
        )

        self.search_input.textChanged.connect(
            self.apply_filters
        )

        self.year_input.returnPressed.connect(
            self.load_events
        )

    def timeline_toggled(
        self,
        enabled
    ):

        self.timeline_enabled = enabled

        self.timeline_slider.setEnabled(
            enabled
        )

        self.apply_filters()

    def timeline_changed(
        self,
        value
    ):

        self.timeline_day = value

        if not self.timeline_enabled:

            return

        try:

            year_text = (
                self.year_input
                .text()
                .strip()
            )

            if not year_text:

                self.timeline_label.setText(
                    f"Day {value} of year"
                )

                self.apply_filters()

                return

            year = int(
                year_text
            )

            actual_year = year

            if (
                self.calendar_box.currentText()
                == "Hijri"
            ):

                actual_year = (
                    min(
                        [
                            int(
                                event["year"]
                            )
                            for event in self.events
                            if str(
                                event.get(
                                    "year",
                                    ""
                                )
                            ).isdigit()
                        ],
                        default=year
                    )
                )

            start = date(
                actual_year,
                1,
                1
            )

            selected_date = (
                start
                +
                timedelta(
                    days=value - 1
                )
            )

            self.timeline_label.setText(
                f"Through "
                f"{selected_date.strftime('%B %d')}"
            )

        except:

            self.timeline_label.setText(
                f"Day {value}"
            )

        self.apply_filters()

    def apply_filters(self):

        search = (
            self.search_input
            .text()
            .lower()
            .strip()
        )

        category = (
            self.category_box
            .currentText()
        )

        filtered = []

        for event in self.events:

            if (
                category != "All"
                and
                event["category"]
                != category
            ):

                continue

            if search:

                searchable = (
                    event["event"]
                    + " "
                    + event["category"]
                    + " "
                    + event.get(
                        "description",
                        ""
                    )
                ).lower()

                if search not in searchable:

                    continue

            if self.timeline_enabled:

                try:

                    event_date = date(
                        int(
                            event["year"]
                        ),
                        int(
                            event["month"]
                        ),
                        int(
                            event["day"]
                        )
                    )

                    year_start = date(
                        event_date.year,
                        1,
                        1
                    )

                    day_of_year = (
                        event_date
                        - year_start
                    ).days + 1

                    if (
                        day_of_year
                        >
                        self.timeline_day
                    ):

                        continue

                except:

                    pass

            filtered.append(
                event
            )

        if not search:

            self.display_events(
                filtered
            )

        elif self.worker is None:

            self.display_events(
                filtered
            )

    def toggle_theme(self):

        self.dark_mode = (
            not self.dark_mode
        )

        self.apply_theme()

    def apply_theme(self):

        if self.dark_mode:

            self.theme_button.setText(
                "☀ Light"
            )

            self.setStyleSheet("""
                QWidget {
                    background-color: #181818;
                    color: #eeeeee;
                }

                QLineEdit,
                QComboBox,
                QTextEdit,
                QTableWidget,
                QGroupBox {
                    background-color: #252525;
                    color: #eeeeee;
                    border: 1px solid #444444;
                    padding: 5px;
                }

                QPushButton {
                    background-color: #333333;
                    color: #ffffff;
                    border: 1px solid #555555;
                    padding: 7px 12px;
                    border-radius: 5px;
                }

                QPushButton:hover {
                    background-color: #444444;
                }

                QHeaderView::section {
                    background-color: #333333;
                    color: #ffffff;
                    padding: 6px;
                    border: 1px solid #444444;
                }

                QTableWidget {
                    gridline-color: #444444;
                }

                QTableWidget::item:selected {
                    background-color: #555555;
                }

                QSlider::groove:horizontal {
                    height: 6px;
                    background: #444444;
                }

                QSlider::handle:horizontal {
                    width: 16px;
                    margin: -5px 0;
                    background: #aaaaaa;
                    border-radius: 8px;
                }
            """)

        else:

            self.theme_button.setText(
                "🌙 Dark"
            )

            self.setStyleSheet("""
                QWidget {
                    background-color: #f5f5f5;
                    color: #222222;
                }

                QLineEdit,
                QComboBox,
                QTextEdit,
                QTableWidget,
                QGroupBox {
                    background-color: #ffffff;
                    color: #222222;
                    border: 1px solid #cccccc;
                    padding: 5px;
                }

                QPushButton {
                    background-color: #eeeeee;
                    color: #222222;
                    border: 1px solid #cccccc;
                    padding: 7px 12px;
                    border-radius: 5px;
                }

                QPushButton:hover {
                    background-color: #dddddd;
                }

                QHeaderView::section {
                    background-color: #e8e8e8;
                    color: #222222;
                    padding: 6px;
                    border: 1px solid #cccccc;
                }

                QTableWidget {
                    gridline-color: #cccccc;
                }

                QTableWidget::item:selected {
                    background-color: #cce5ff;
                    color: #000000;
                }

                QSlider::groove:horizontal {
                    height: 6px;
                    background: #cccccc;
                }

                QSlider::handle:horizontal {
                    width: 16px;
                    margin: -5px 0;
                    background: #777777;
                    border-radius: 8px;
                }
            """)

    def load_events(self):

        if not API_KEY.strip():

            QMessageBox.warning(
                self,
                "API Key Missing",
                "Put your API Ninjas API key at the top."
            )

            return

        year_text = (
            self.year_input
            .text()
            .strip()
        )

        if not year_text:

            QMessageBox.warning(
                self,
                "Missing Year",
                "Enter a year first."
            )

            return

        try:

            year = int(
                year_text
            )

        except ValueError:

            QMessageBox.warning(
                self,
                "Invalid Year",
                "Year must be a number."
            )

            return

        self.stop_worker()

        self.events = []

        self.wikipedia_articles = []

        self.on_this_day_events = []

        self.table.setRowCount(
            0
        )

        self.search_button.setEnabled(
            False
        )

        self.today_button.setEnabled(
            False
        )

        self.status.setText(
            "Starting search..."
        )

        self.timeline_slider.setValue(
            365
        )

        self.timeline_label.setText(
            "Full year"
        )

        worker = APIWorker(

            year,

            self.calendar_box.currentText(),

            self.category_box.currentText(),

            self.search_input.text().strip()
        )

        self.worker = worker

        worker.status.connect(
            self.update_status
        )

        worker.events_ready.connect(
            self.events_loaded
        )

        worker.wikipedia_ready.connect(
            self.wikipedia_loaded
        )

        worker.on_this_day_ready.connect(
            self.on_this_day_loaded
        )

        worker.error.connect(
            self.worker_error
        )

        worker.finished.connect(
            self.worker_finished
        )

        worker.start()

    def load_on_this_day(self):

        self.stop_worker()

        self.events = []

        self.wikipedia_articles = []

        self.on_this_day_events = []

        self.table.setRowCount(
            0
        )

        self.search_button.setEnabled(
            False
        )

        self.today_button.setEnabled(
            False
        )

        today = date.today()

        self.status.setText(
            f"Loading On This Day — "
            f"{today.strftime('%B %d')}..."
        )

        worker = APIWorker(

            today.year,

            "Gregorian",

            "All",

            "",

            on_this_day=True
        )

        self.worker = worker

        worker.status.connect(
            self.update_status
        )

        worker.on_this_day_ready.connect(
            self.on_this_day_loaded
        )

        worker.error.connect(
            self.worker_error
        )

        worker.finished.connect(
            self.worker_finished
        )

        worker.start()

    def on_this_day_loaded(
        self,
        events
    ):

        self.on_this_day_events = events

        self.table.setRowCount(
            0
        )

        self.wikipedia_articles = []

        self.display_events(
            events
        )

        today = date.today()

        self.status.setText(
            f"📅 On This Day — "
            f"{today.strftime('%B %d')} — "
            f"{len(events)} results"
        )

    def update_status(
        self,
        text
    ):

        self.status.setText(
            text
        )

    def events_loaded(
        self,
        events
    ):

        self.events = events

        self.apply_filters()

        if events:

            self.status.setText(
                f"Found {len(events)} historical events."
            )

    def wikipedia_loaded(
        self,
        articles,
        query
    ):

        self.wikipedia_articles = (
            articles
        )

        if articles:

            if self.search_input.text().strip():

                self.display_wikipedia(
                    articles
                )

                self.status.setText(
                    f"Showing {len(articles)} Wikipedia "
                    f"results for: {query}"
                )

            elif not self.events:

                self.display_wikipedia(
                    articles
                )

                self.status.setText(
                    f"No events found. Showing "
                    f"{len(articles)} Wikipedia articles."
                )

        else:

            if not self.events:

                self.status.setText(
                    "No historical events or "
                    "Wikipedia results found."
                )

    def display_events(
        self,
        events
    ):

        self.table.setSortingEnabled(
            False
        )

        self.table.setRowCount(
            0
        )

        for event in events:

            row = (
                self.table.rowCount()
            )

            self.table.insertRow(
                row
            )

            values = [

                event.get(
                    "date",
                    ""
                ),

                event.get(
                    "hijri",
                    ""
                ),

                event.get(
                    "event",
                    ""
                ),

                event.get(
                    "category",
                    "Other"
                ),

                event.get(
                    "description",
                    event.get(
                        "event",
                        ""
                    )
                )
            ]

            for column, value in enumerate(
                values
            ):

                item = QTableWidgetItem(
                    str(value)
                )

                item.setToolTip(
                    str(value)
                )

                self.table.setItem(
                    row,
                    column,
                    item
                )

        self.table.setSortingEnabled(
            True
        )

        self.count_label.setText(
            f"{len(events)} events"
        )

    def display_wikipedia(
        self,
        articles
    ):

        self.table.setSortingEnabled(
            False
        )

        self.table.setRowCount(
            0
        )

        for article in articles:

            row = (
                self.table.rowCount()
            )

            self.table.insertRow(
                row
            )

            title = article[
                "title"
            ]

            description = article.get(
                "description",
                ""
            )

            values = [

                "Wikipedia",

                "—",

                title,

                "Wikipedia",

                description
            ]

            for column, value in enumerate(
                values
            ):

                item = QTableWidgetItem(
                    str(value)
                )

                item.setToolTip(
                    str(value)
                )

                self.table.setItem(
                    row,
                    column,
                    item
                )

        self.table.setSortingEnabled(
            True
        )

        self.count_label.setText(
            f"{len(articles)} Wikipedia articles"
        )

    def show_details(
        self,
        row,
        column
    ):

        if (
            self.wikipedia_articles
            and
            row
            <
            len(
                self.wikipedia_articles
            )
            and
            self.table.item(
                row,
                3
            )
            and
            self.table.item(
                row,
                3
            ).text()
            ==
            "Wikipedia"
        ):

            dialog = WikipediaDialog(
                self.wikipedia_articles[
                    row
                ],
                self
            )

            dialog.exec_()

            return

        if not self.table.item(
            row,
            2
        ):

            return

        event_name = (
            self.table.item(
                row,
                2
            ).text()
        )

        date_text = (
            self.table.item(
                row,
                0
            ).text()
        )

        hijri = (
            self.table.item(
                row,
                1
            ).text()
        )

        category = (
            self.table.item(
                row,
                3
            ).text()
        )

        description = (
            self.table.item(
                row,
                4
            ).text()
        )

        event = {

            "event":
                event_name,

            "date":
                date_text,

            "hijri":
                hijri,

            "category":
                category,

            "description":
                description,

            "source":
                "Historical Events Explorer"
        }

        if row < len(
            self.events
        ):

            event["url"] = self.events[
                row
            ].get(
                "url",
                ""
            )

            event["source"] = self.events[
                row
            ].get(
                "source",
                event["source"]
            )

        if (
            row
            <
            len(
                self.on_this_day_events
            )
        ):

            event["url"] = (
                self.on_this_day_events[
                    row
                ].get(
                    "url",
                    ""
                )
            )

        dialog = DetailsDialog(
            event,
            self
        )

        dialog.exec_()

    def show_statistics(self):

        events = self.events

        if self.on_this_day_events:

            events = (
                self.on_this_day_events
            )

        if not events:

            QMessageBox.information(
                self,
                "No Data",
                "Search for a year or use "
                "On This Day first."
            )

            return

        dialog = StatisticsDialog(
            events,
            self
        )

        dialog.exec_()

    def worker_error(
        self,
        title,
        message
    ):

        QMessageBox.critical(
            self,
            title,
            message
        )

        self.status.setText(
            message
        )

    def stop_worker(self):

        if (
            self.worker is not None
            and
            self.worker.isRunning()
        ):

            self.worker.requestInterruption()

            self.worker.quit()

            self.worker.wait(
                1000
            )

            self.worker = None

    def worker_finished(self):

        self.search_button.setEnabled(
            True
        )

        self.today_button.setEnabled(
            True
        )

        self.worker = None

    def export_csv(self):

        if self.table.rowCount() == 0:

            QMessageBox.warning(
                self,
                "Nothing to Export",
                "There are no visible results."
            )

            return

        filename, _ = (
            QFileDialog.getSaveFileName(
                self,
                "Export CSV",
                "historical_events.csv",
                "CSV Files (*.csv)"
            )
        )

        if not filename:

            return

        try:

            with open(
                filename,
                "w",
                newline="",
                encoding="utf-8-sig"
            ) as file:

                writer = csv.writer(
                    file
                )

                writer.writerow([

                    "Date",
                    "Hijri Date",
                    "Event / Article",
                    "Category",
                    "Description"
                ])

                for row in range(
                    self.table.rowCount()
                ):

                    writer.writerow([

                        self.table.item(
                            row,
                            column
                        ).text()

                        for column in range(
                            5
                        )
                    ])

            QMessageBox.information(
                self,
                "Export Complete",
                "CSV exported successfully!"
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Export Error",
                str(error)
            )

    def clear(self):

        self.stop_worker()

        self.events = []

        self.wikipedia_articles = []

        self.on_this_day_events = []

        self.table.setRowCount(
            0
        )

        self.year_input.clear()

        self.search_input.clear()

        self.category_box.setCurrentIndex(
            0
        )

        self.timeline_check.setChecked(
            False
        )

        self.timeline_slider.setValue(
            365
        )

        self.timeline_label.setText(
            "Full year"
        )

        self.count_label.setText(
            "0 events"
        )

        self.status.setText(
            "Enter a year and press Search."
        )

if __name__ == "__main__":

    app = QApplication(
        sys.argv
    )

    app.setStyle(
        "Fusion"
    )

    window = HistoricalEventsApp()

    window.show()

    sys.exit(
        app.exec_()
    )
