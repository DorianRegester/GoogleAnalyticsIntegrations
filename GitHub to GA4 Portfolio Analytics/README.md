# GitHub-to-GA4 Portfolio Analytics Engine (v1.0.0)

**GitHub-to-GA4 Portfolio Analytics Engine** is an automated monitoring solution designed to provide enterprise-grade visibility into open-source portfolio performance. While GitHub provides basic traffic insights for individual repositories, this engine aggregates data across a large-scale library of 75+ plugins and tools, syncing high-resolution traffic, clones, and file-level engagement directly into **Google Analytics 4 (GA4)**.

Developed by **Dorian D. Regester**, a digital analytics professional and implementation engineer and owner of **scriptedinsights.com**. This project solves the "noise" problem of managing 75+ distributed assets by consolidating engagement metrics into a single, actionable dashboard.

---

## 🚀 Architecture Overview

The engine operates via a four-stage automated pipeline:
1.  **Trigger:** A GitHub Action fires daily (scheduled via Cron).
2.  **Extraction:** A Python script utilizes the GitHub REST API to fetch traffic, clone, and popular path data.
3.  **Transport:** Data is securely transmitted via the **GA4 Measurement Protocol**.
4.  **Visualization:** Metrics are surfaced in GA4 via Custom Dimensions and the Exploration suite.

---

## 🛠 Setup & Implementation

### 1. Repository Configuration
*   Create a new public repository named `github-analytics-engine`.
*   Initialize with a `.gitignore` using the **Python template**.

### 2. Secure "Vault" Configuration (Secrets)
Despite the public nature of the repo, sensitive credentials are stored as **GitHub Actions Secrets**.
*   **GitHub PAT:** Generate a Fine-grained Personal Access Token with **Read-only** access to "Metadata" and "Administration" for all repositories.
*   **GA4 Credentials:** Obtain your `Measurement ID` and create a `Measurement Protocol API secret` within your GA4 Data Stream settings.
*   **Add Secrets:** In repo **Settings > Secrets and variables > Actions**, create the following:
    *   `PAT_TOKEN`: Your GitHub PAT.
    *   `GA4_MEASUREMENT_ID`: Your `G-XXXXXXXX` ID.
    *   `GA4_API_SECRET`: Your GA4 API Secret.

### 3. Automation Script (`sync_portfolio.py`)
The Python engine (stored in the root directory) handles the heavy lifting:
*   Loops through all 75+ repositories in a single API call (`per_page=100`).
*   Extracts daily views, clones, stars, and forks.
*   Drills down into the top 5 **Popular Paths** (files/folders) to identify which specific implementation guides or plugins are driving interest.

### 4. GitHub Actions Trigger (`sync.yml`)
Located in `.github/workflows/`, this YAML configuration automates the sync:
*   **Schedule:** Runs automatically at midnight daily.
*   **Manual Override:** Includes `workflow_dispatch` to allow for "on-demand" syncing.

---

## 📊 GA4 Configuration

To surface this data, you must register the following in your GA4 interface (**Admin > Custom Definitions**):

### Custom Dimensions (Event scope)
*   `repo_name`: Identifies the specific repository.
*   `file_path`: Identifies the specific folder or plugin file being viewed.

### Custom Metrics
*   `daily_views`: Standard traffic count.
*   `daily_clones`: Repository download/clone count.
*   `stars`: Total repository stargazers.

---

## 📈 Viewing the Data

Once the initial sync is complete, leverage the **Explore** tab in GA4 to build a "Portfolio Performance" report:
*   **Dimensions:** `Repo Name`, `File Path`.
*   **Metrics:** `Event Count`, `Daily Views`.
*   **Insight:** Use the "Rows" layout with `Repo Name` to immediately identify which of your 75+ analytics plugins are gaining the most traction at the file level.

---

## 🛠 Technical Details

*   **API Strategy:** Uses the GitHub Traffic API specifically for views and clones, combined with the general Repos API for metadata.
*   **Data Transport:** Employs the **GA4 Measurement Protocol** (v2) to bypass browser-based tracking limitations.
*   **Security:** Implements environment-variable injection to ensure zero exposure of PAT or API secrets in the public codebase.
*   **Scalability:** Configured to handle 100+ repositories with efficient pagination logic.

---

## 📄 License
MIT License - Developed by **Dorian D. Regester** ([scriptedinsights.com](https://scriptedinsights.com)).
