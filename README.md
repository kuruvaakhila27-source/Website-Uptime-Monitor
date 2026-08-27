# 🌐 Website Uptime Monitor

A real-time website monitoring dashboard built with Python and Streamlit.

It allows users to monitor multiple websites and check their availability, HTTP status, response time, and uptime performance.

## ✨ Features

- 🌐 Monitor multiple websites
- 🟢 Detect whether a website is UP or DOWN
- 🔢 Check HTTP status codes
- ⚡ Measure website response time
- ⚠️ Detect slow-responding websites
- 📊 Real-time monitoring dashboard
- 📈 Response-time analysis chart
- 📋 Complete monitoring history
- 📊 Website uptime statistics
- ⬇️ Export monitoring history as CSV
- ➕ Add and remove websites easily
- 🗑️ Clear monitoring history

## 🛠️ Technologies Used

- Python
- Streamlit
- Requests
- Pandas
- Plotly

## 📂 Project Structure

```text
Website-Uptime-Monitor/
│
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
🚀 How to Run
1. Clone the repository
git clone YOUR_GITHUB_REPOSITORY_URL
2. Open the project folder
cd Website-Uptime-Monitor
3. Create a virtual environment
python -m venv venv
4. Activate the virtual environment
Windows PowerShell:
venv\Scripts\Activate.ps1
5. Install dependencies
pip install -r requirements.txt
6. Run the application
streamlit run app.py
The application will open in your browser.
🔍 How It Works
1. Add Websites
Enter a website URL such as:
- https://google.com
- https://github.com
- https://youtube.com
Each website is stored separately.
2. HTTP Request
The application sends an HTTP request using Python's requests library.
3. Availability Check
- 200–299 → Successful
- 300–399 → Reachable / Redirect
- 400–599 → Website returned an error
- Request exception → Website unavailable or timeout
4. Response Time
The application measures how long the website takes to respond.
5. Uptime History
Monitoring results are stored locally during application usage.
6. Dashboard
The dashboard displays:
- 🟢 Online websites
- 🔴 Offline websites
- ⚡ Response time
- 📈 Uptime percentage
- 📊 Response-time chart
- 🕒 Monitoring history
- ⬇️ CSV export
🎨 Status Legend
Status	Meaning
🟢 UP	Website is reachable
🔴 DOWN	Website is unavailable
⚠️ SLOW	Website response exceeds 1 second


📊 Example
The dashboard can monitor multiple websites simultaneously and display their current status, HTTP response code, response time, and uptime percentage.
🎯 Project Goal
The goal of this project is to provide a simple and practical website monitoring tool that helps users quickly identify website availability and performance issues.