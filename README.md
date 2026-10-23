# AI Usage Analytics Dashboard

[![Python syntax](https://github.com/Rajureddy07/AI-Usage-Analytics-Dashboard/actions/workflows/syntax.yml/badge.svg)](https://github.com/Rajureddy07/AI-Usage-Analytics-Dashboard/actions/workflows/syntax.yml)

An interactive dashboard for exploring AI-model usage records with SQL-backed metrics and Plotly visualizations.

![Dashboard](https://github.com/user-attachments/assets/a6e8d7bb-822a-4d0d-a8ad-12d44c6341ae)

## What it explores

- Prompt and token volume by model
- Total and average cost metrics
- Average response time comparisons
- Time-based cost trends
- Model filtering, summary tables, and CSV export

This is a portfolio analytics project. Included CSV records are illustrative sample data; they are not a live API feed or a representation of current provider pricing.

## Stack

Python · PostgreSQL · SQL · Pandas · Streamlit · Plotly

## Project structure

```text
.
├── app.py                # Streamlit analytics interface
├── database.py           # Environment-based command-line query helper
├── data.csv              # Small sample dataset
├── load_sample_data.py   # Idempotent sample-data loader
├── schema.sql            # PostgreSQL table definition
├── requirements.txt
└── .env.example          # Safe configuration template
```

## Quick start

### 1. Create the database

Create a local PostgreSQL database named `ai_data_usage` (or choose another name and set `DB_NAME` in the next step).

### 2. Configure local environment variables

**Windows PowerShell**
```powershell
Copy-Item .env.example .env
```

Edit `.env` and set the database user/password that you use locally. Keep `.env` private; Git ignores it.

### 3. Install dependencies

```bash
python -m venv .venv
```

**Windows PowerShell**
```powershell
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**
```bash
source .venv/bin/activate
```

Install the packages:

```bash
pip install -r requirements.txt
```

### 4. Load sample data

```bash
python load_sample_data.py
```

The loader creates the `usage_data` table if needed and safely upserts records using `(date, model)` as the key. Re-running it will refresh those sample rows.

### 5. Launch the dashboard

```bash
streamlit run app.py
```

Streamlit prints a local URL in the terminal.

## Data model

The dashboard reads `usage_data` with these fields:

| Column | Meaning |
| --- | --- |
| `date` | Observation date |
| `model` | Model label recorded by the dataset |
| `prompts` | Prompt count |
| `tokens` | Token count |
| `cost` | Cost value supplied by the dataset |
| `response_time` | Response-time measurement supplied by the dataset |

Cost units and response-time units depend on the source dataset; verify them before interpreting metrics. The sample loader uses the included CSV, whose values are for demonstration.

## Configuration

| Variable | Default | Purpose |
| --- | --- | --- |
| `DB_HOST` | `localhost` | PostgreSQL host |
| `DB_PORT` | `5432` | PostgreSQL port |
| `DB_NAME` | `ai_data_usage` | Database name |
| `DB_USER` | `postgres` | Database user |
| `DB_PASSWORD` | required | Local database password |

## Screenshots

<details>
  <summary>Business insights</summary>

  ![Business insights](https://github.com/user-attachments/assets/bc383f63-c817-4fcb-b8b7-aef94b44c5db)
</details>

<details>
  <summary>SQL analytics</summary>

  ![SQL analytics](https://github.com/user-attachments/assets/27ec6e99-0f92-4ab2-a80a-3d203267cadd)
</details>

<details>
  <summary>Charts and model comparison</summary>

  ![Charts](https://github.com/user-attachments/assets/040e14da-39ce-4939-92a4-9bcf92875382)
  ![Model comparison](https://github.com/user-attachments/assets/9a50ebd4-21ae-4840-9054-ab7f7c5eeab2)
</details>

## Security and limitations

- Never commit `.env`, passwords, production database dumps, or confidential usage records.
- Rotate any credential that has ever been committed to a public repository.
- Metrics are only as accurate as the data and units loaded into PostgreSQL.
- The application is a local analytics prototype; no live-provider integration or production deployment is implied.

## Author

G. Rajasekhar Reddy · [GitHub](https://github.com/Rajureddy07)
