import streamlit as st
import requests
import time
import pandas as pd
import json
import os
from datetime import datetime


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Website Uptime Monitor",
    page_icon="🌐",
    layout="wide"
)


# =========================================================
# CONSTANTS
# =========================================================

DATA_FILE = "monitor_data.json"

DEFAULT_TIMEOUT = 10
SLOW_THRESHOLD = 1000


# =========================================================
# DATA STORAGE
# =========================================================

def load_data():
    """Load websites and history from JSON file."""

    if not os.path.exists(DATA_FILE):
        return {
            "websites": [],
            "history": []
        }

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        return {
            "websites": data.get("websites", []),
            "history": data.get("history", [])
        }

    except Exception:
        return {
            "websites": [],
            "history": []
        }


def save_data(websites, history):
    """Save websites and monitoring history."""

    data = {
        "websites": websites,
        "history": history
    }

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            indent=4
        )


# =========================================================
# INITIAL DATA
# =========================================================

if "websites" not in st.session_state:
    st.session_state.websites = load_data()["websites"]

if "history" not in st.session_state:
    st.session_state.history = load_data()["history"]

if "last_results" not in st.session_state:
    st.session_state.last_results = []


# =========================================================
# URL NORMALIZER
# =========================================================

def normalize_url(url):

    url = url.strip()

    if not url:
        return ""

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    return url.rstrip("/")


# =========================================================
# CHECK WEBSITE
# =========================================================

def check_website(url, timeout):

    url = normalize_url(url)

    start_time = time.perf_counter()

    try:

        response = requests.get(
            url,
            timeout=timeout,
            headers={
                "User-Agent": "Website-Uptime-Monitor/1.0"
            },
            allow_redirects=True
        )

        elapsed = time.perf_counter() - start_time

        response_time = round(
            elapsed * 1000,
            2
        )

        if 200 <= response.status_code < 400:
            status = "UP"
        else:
            status = "DOWN"

        return {
            "Website": url,
            "Status": status,
            "HTTP Status": response.status_code,
            "Response Time (ms)": response_time,
            "Checked At": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "Error": ""
        }

    except requests.RequestException as error:

        elapsed = time.perf_counter() - start_time

        response_time = round(
            elapsed * 1000,
            2
        )

        return {
            "Website": url,
            "Status": "DOWN",
            "HTTP Status": "N/A",
            "Response Time (ms)": response_time,
            "Checked At": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "Error": str(error)
        }


# =========================================================
# CHECK ALL WEBSITES
# =========================================================

def check_all_websites(timeout):

    results = []

    for website in st.session_state.websites:

        result = check_website(
            website,
            timeout
        )

        results.append(result)

        st.session_state.history.append(
            result
        )

    st.session_state.last_results = results

    save_data(
        st.session_state.websites,
        st.session_state.history
    )


# =========================================================
# REMOVE WEBSITE
# =========================================================

def remove_website(website):

    if website in st.session_state.websites:

        st.session_state.websites.remove(
            website
        )

        save_data(
            st.session_state.websites,
            st.session_state.history
        )


# =========================================================
# HEADER
# =========================================================

st.title("🌐 Website Uptime Monitor")

st.caption(
    "Monitor website availability, response time, HTTP status "
    "and uptime performance."
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("⚙️ Monitor Controls")

    # -----------------------------------------------------
    # ADD WEBSITE
    # -----------------------------------------------------

    st.subheader("➕ Add Website")

    with st.form(
        "add_website_form",
        clear_on_submit=True
    ):

        website_input = st.text_input(
            "Website URL",
            placeholder="example.com"
        )

        add_button = st.form_submit_button(
            "➕ Add Website",
            use_container_width=True
        )

    if add_button:

        normalized = normalize_url(
            website_input
        )

        if not normalized:

            st.warning(
                "Please enter a website URL."
            )

        elif normalized in st.session_state.websites:

            st.warning(
                "⚠️ Website already exists."
            )

        else:

            st.session_state.websites.append(
                normalized
            )

            save_data(
                st.session_state.websites,
                st.session_state.history
            )

            st.success(
                f"✅ Added: {normalized}"
            )

    st.divider()

    # -----------------------------------------------------
    # TIMEOUT
    # -----------------------------------------------------

    st.subheader("⏱️ Timeout")

    timeout = st.slider(
        "Request timeout (seconds)",
        min_value=3,
        max_value=30,
        value=DEFAULT_TIMEOUT
    )

    st.divider()

    # -----------------------------------------------------
    # MONITORED WEBSITES
    # -----------------------------------------------------

    st.subheader("🌐 Monitored Websites")

    if st.session_state.websites:

        for index, website in enumerate(
            st.session_state.websites,
            start=1
        ):

            st.markdown(
                f"**{index}.** {website}"
            )

            if st.button(
                "❌ Remove",
                key=f"remove_button_{index}_{website}",
                use_container_width=True
            ):

                remove_website(
                    website
                )

                st.rerun()

    else:

        st.info(
            "No websites added yet."
        )

    st.divider()

    # -----------------------------------------------------
    # CLEAR HISTORY
    # -----------------------------------------------------

    if st.button(
        "🧹 Clear History",
        use_container_width=True
    ):

        st.session_state.history = []

        save_data(
            st.session_state.websites,
            st.session_state.history
        )

        st.session_state.last_results = []

        st.success(
            "Monitoring history cleared."
        )

        st.rerun()

    # -----------------------------------------------------
    # REMOVE ALL WEBSITES
    # -----------------------------------------------------

    if st.button(
        "🗑️ Remove All Websites",
        use_container_width=True
    ):

        st.session_state.websites = []

        save_data(
            st.session_state.websites,
            st.session_state.history
        )

        st.session_state.last_results = []

        st.success(
            "All websites removed."
        )

        st.rerun()


# =========================================================
# MAIN CONTROL BUTTONS
# =========================================================

control1, control2 = st.columns(2)


with control1:

    check_all = st.button(
        "🔍 Check All Websites",
        use_container_width=True,
        type="primary"
    )


with control2:

    refresh = st.button(
        "🔄 Refresh Dashboard",
        use_container_width=True
    )

    if refresh:
        st.rerun()


# =========================================================
# CHECK WEBSITES
# =========================================================

if check_all:

    if not st.session_state.websites:

        st.warning(
            "⚠️ Add at least one website first."
        )

    else:

        progress = st.progress(0)

        total_websites = len(
            st.session_state.websites
        )

        results = []

        for index, website in enumerate(
            st.session_state.websites
        ):

            result = check_website(
                website,
                timeout
            )

            results.append(result)

            st.session_state.history.append(
                result
            )

            progress.progress(
                (index + 1) / total_websites
            )

        st.session_state.last_results = results

        save_data(
            st.session_state.websites,
            st.session_state.history
        )

        st.success(
            "✅ Website checks completed successfully."
        )


# =========================================================
# LATEST RESULTS
# =========================================================

st.divider()

st.subheader(
    "📡 Latest Monitoring Results"
)

if st.session_state.last_results:

    for result in st.session_state.last_results:

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:

            st.write("🌐 Website")

            st.write(
                result["Website"]
            )

        with col2:

            st.write("📡 Status")

            if result["Status"] == "UP":

                st.success("🟢 UP")

            else:

                st.error("🔴 DOWN")

        with col3:

            st.write("🔢 HTTP Status")

            st.metric(
                "Code",
                result["HTTP Status"]
            )

        with col4:

            st.write("⚡ Response")

            st.metric(
                "Time",
                f'{result["Response Time (ms)"]} ms'
            )

        with col5:

            st.write("🕒 Checked")

            st.caption(
                result["Checked At"]
            )

        if result["Error"]:

            st.error(
                f'Error: {result["Error"]}'
            )

        if (
            result["Status"] == "UP"
            and
            result["Response Time (ms)"] > SLOW_THRESHOLD
        ):

            st.warning(
                "⚠️ Website is reachable but responding slowly."
            )

else:

    st.info(
        "No monitoring results yet. "
        "Add websites and click Check All Websites."
    )


# =========================================================
# DASHBOARD
# =========================================================

st.divider()

st.subheader(
    "📊 Monitoring Dashboard"
)

if st.session_state.last_results:

    results_df = pd.DataFrame(
        st.session_state.last_results
    )

    total = len(results_df)

    up_count = (
        results_df["Status"] == "UP"
    ).sum()

    down_count = (
        results_df["Status"] == "DOWN"
    ).sum()

    avg_response = round(
        results_df["Response Time (ms)"].mean(),
        2
    )

    uptime_percentage = round(
        (up_count / total) * 100,
        2
    )

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        st.metric(
            "🌐 Websites",
            total
        )

    with c2:
        st.metric(
            "🟢 Online",
            up_count
        )

    with c3:
        st.metric(
            "🔴 Offline",
            down_count
        )

    with c4:
        st.metric(
            "⚡ Avg Response",
            f"{avg_response} ms"
        )

    with c5:
        st.metric(
            "📈 Uptime",
            f"{uptime_percentage}%"
        )

else:

    st.info(
        "Run a website check to display dashboard metrics."
    )


# =========================================================
# CURRENT STATUS
# =========================================================

st.divider()

st.subheader(
    "📋 Current Status"
)

if st.session_state.last_results:

    current_df = pd.DataFrame(
        st.session_state.last_results
    )

    display_df = current_df[
        [
            "Website",
            "Status",
            "HTTP Status",
            "Response Time (ms)",
            "Checked At"
        ]
    ]

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No current status available."
    )


# =========================================================
# RESPONSE TIME CHART
# =========================================================

st.divider()

st.subheader(
    "📈 Response Time Analysis"
)

if st.session_state.history:

    history_df = pd.DataFrame(
        st.session_state.history
    )

    chart_df = history_df[
        [
            "Checked At",
            "Website",
            "Response Time (ms)"
        ]
    ].copy()

    chart_df["Checked At"] = pd.to_datetime(
        chart_df["Checked At"]
    )

    chart_df = chart_df.sort_values(
        "Checked At"
    )

    pivot_df = chart_df.pivot_table(
        index="Checked At",
        columns="Website",
        values="Response Time (ms)",
        aggfunc="mean"
    )

    st.line_chart(
        pivot_df,
        use_container_width=True
    )

else:

    st.info(
        "Run website checks to generate the response-time chart."
    )


# =========================================================
# UPTIME HISTORY
# =========================================================

st.divider()

st.subheader(
    "📊 Website Uptime History"
)

if st.session_state.history:

    history_df = pd.DataFrame(
        st.session_state.history
    )

    websites = history_df[
        "Website"
    ].unique()

    uptime_rows = []

    for website in websites:

        website_data = history_df[
            history_df["Website"] == website
        ]

        total_checks = len(
            website_data
        )

        successful_checks = (
            website_data["Status"] == "UP"
        ).sum()

        failed_checks = (
            total_checks -
            successful_checks
        )

        uptime = round(
            (
                successful_checks /
                total_checks
            ) * 100,
            2
        )

        uptime_rows.append(
            {
                "Website": website,
                "Total Checks": total_checks,
                "Successful Checks": successful_checks,
                "Failed Checks": failed_checks,
                "Uptime %": uptime
            }
        )

    uptime_df = pd.DataFrame(
        uptime_rows
    )

    st.dataframe(
        uptime_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No uptime history available yet."
    )


# =========================================================
# COMPLETE HISTORY
# =========================================================

st.divider()

st.subheader(
    "🕒 Complete Monitoring History"
)

if st.session_state.history:

    history_df = pd.DataFrame(
        st.session_state.history
    )

    st.dataframe(
        history_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "Monitoring history will appear here."
    )


# =========================================================
# DOWNLOAD HISTORY
# =========================================================

if st.session_state.history:

    st.divider()

    history_df = pd.DataFrame(
        st.session_state.history
    )

    csv_data = history_df.to_csv(
        index=False
    )

    st.download_button(
        "⬇️ Download Monitoring History",
        data=csv_data,
        file_name="website_monitor_history.csv",
        mime="text/csv",
        use_container_width=True
    )


# =========================================================
# HOW IT WORKS
# =========================================================

st.divider()

st.subheader(
    "💡 How This Project Works"
)

st.markdown(
    """
### 1️⃣ Add Websites

Enter a website URL such as:

- `https://google.com`
- `https://github.com`
- `https://youtube.com`

Each website is stored separately.

### 2️⃣ HTTP Request

The application sends an HTTP request using Python's
`requests` library.

### 3️⃣ Availability Check

- `200–299` → Successful
- `300–399` → Reachable / Redirect
- `400–599` → Website returned an error
- Request exception → Website unavailable / timeout

### 4️⃣ Response Time

The application measures how long the website takes
to respond.

### 5️⃣ Uptime History

Every check is stored in `monitor_data.json`.

### 6️⃣ Dashboard

The dashboard displays:

- 🟢 Online websites
- 🔴 Offline websites
- ⚡ Response time
- 📈 Uptime percentage
- 📊 Response-time chart
- 🕒 Complete monitoring history
- ⬇️ CSV export
"""
)


# =========================================================
# LEGEND
# =========================================================

st.divider()

st.subheader(
    "🎨 Status Legend"
)

legend1, legend2, legend3 = st.columns(3)

with legend1:
    st.success(
        "🟢 UP — Website is reachable"
    )

with legend2:
    st.error(
        "🔴 DOWN — Website is unavailable"
    )

with legend3:
    st.warning(
        "⚠️ SLOW — Response exceeds 1 second"
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "🌐 Website Uptime Monitor • Python + Streamlit + Requests"
)