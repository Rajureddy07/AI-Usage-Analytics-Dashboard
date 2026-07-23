# 🚀 AI Usage Analytics Dashboard

## 📌 Project Overview

The **AI Usage Analytics Dashboard** is a Data Analytics project built using **Python, PostgreSQL, Streamlit, Pandas, and Plotly**.

This dashboard helps analyze AI model usage by tracking:
- 📈 Prompts
- 🔢 Tokens
- 💰 Cost
- ⚡ Response Time

It provides interactive visualizations and business insights to help understand AI usage patterns and compare model performance.

---

## ✨ Features

- 📊 Interactive Dashboard using Streamlit
- 🗄️ PostgreSQL Database Integration
- 🔍 AI Model Filtering
- 📈 KPI Metrics
  - Total Prompts
  - Total Tokens
  - Total Cost
  - Average Response Time
- 📊 Interactive Charts
  - Bar Chart
  - Pie Chart
  - Line Chart
- 📋 SQL Analytics Summary
- 🔗 SQL JOIN Operations
- 📥 Download Analytics Report (CSV)
- 📊 AI Model Performance Comparison
- 💡 Business Insights
  - Most Used Model
  - Highest Cost Model
  - Fastest Model

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Backend Programming |
| PostgreSQL | Database |
| SQL | Data Analysis & Queries |
| Pandas | Data Processing |
| Streamlit | Dashboard Development |
| Plotly | Interactive Charts |
| Git & GitHub | Version Control |

---

## 📂 Project Structure

```
AI-Usage-Analytics/
│
├── app.py
├── database.py
├── requirements.txt
├── README.md
└── screenshots/
```

---

## 🗄️ Database

### Database Name

```
ai_data_usage
```

### Tables

### usage_data

Stores AI usage records.

| Column |
|---------|
| id |
| date |
| model |
| prompts |
| tokens |
| cost |
| response_time |
| model_id |

---

### models

Stores AI model information.

| Column |
|---------|
| model_id |
| model_name |
| company |

---

## 📊 SQL Concepts Used

- SELECT
- GROUP BY
- SUM()
- AVG()
- ORDER BY
- LIMIT
- INNER JOIN

---

## 📈 Dashboard Features

### Business Insights

- Most Used AI Model
- Highest Cost AI Model
- Fastest AI Model

### KPI Cards

- Total Prompts
- Total Tokens
- Total Cost
- Average Response Time

### Charts

- Bar Chart
- Pie Chart
- Line Chart

### Analytics Table

Model-wise summary including:

- Total Prompts
- Total Tokens
- Total Cost
- Average Response Time

---

## 📷 Dashboard Screenshots

### Dashboard Overview

![Dashboard 1](https://github.com/user-attachments/assets/a6e8d7bb-822a-4d0d-a8ad-12d44c6341ae)

---

### Business Insights

![Dashboard 2](https://github.com/user-attachments/assets/bc383f63-c817-4fcb-b8b7-aef94b44c5db)

---

### SQL Analytics Summary

![Dashboard 3](https://github.com/user-attachments/assets/27ec6e99-0f92-4ab2-a80a-3d203267cadd)

---

### Charts

![Dashboard 4](https://github.com/user-attachments/assets/040e14da-39ce-4939-92a4-9bcf92875382)

---

### AI Model Comparison

![Dashboard 5](https://github.com/user-attachments/assets/9a50ebd4-21ae-4840-9054-ab7f7c5eeab2)

---

## 🚀 How to Run

### Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/AI-Usage-Analytics.git
```

### Move into the Project

```bash
cd AI-Usage-Analytics
```

### Create a Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure PostgreSQL

Update your PostgreSQL credentials in the project or use a `.env` file.

### Run the Dashboard

```bash
streamlit run app.py
```

---

## 📚 Learning Outcomes

Through this project, I learned:

- PostgreSQL Database Integration
- SQL Query Writing
- SQL JOIN Operations
- Data Analysis using Pandas
- Dashboard Development with Streamlit
- Data Visualization with Plotly
- Business Analytics
- Git & GitHub

---

## 🎯 Future Improvements

- User Authentication
- Cloud Database Integration
- Live AI Usage Tracking
- Machine Learning Predictions
- Deployment on Streamlit Community Cloud

---

## 👨‍💻 Author

**G. Rajasekhar Reddy**

Final Year B.E. Computer Science & Engineering (Data Science)

GitHub: https://github.com/Rajureddy07

LinkedIn: *(Add your LinkedIn profile here)*

---

⭐ If you found this project useful, consider giving it a star!
