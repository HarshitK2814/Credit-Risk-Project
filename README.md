# 💳🔎 **CredLens: A Real-Time, Explainable Credit Intelligence Platform**

🚀 **CredTech Hackathon Submission**  

👥 **Team Name:** Risk Raiders  

👨‍💻 **Team Members:**  
- Harshit Kumar  
- Harshit Kumawat  
- Shashank Shekhar  

🔗 **Live Demo URL:** `[YOUR DEPLOYED FRONTEND URL HERE]`  
🔗 **Live Backend API:** `[YOUR DEPLOYED BACKEND URL HERE]`  


---

## 📖 1. Project Overview

Traditional credit ratings are **slow, opaque, and outdated** often lag behind real-world events. **CredLens** is a modern solution to this problem. It's a **real-time, explainable credit intelligence platform** that ingests High-frequency **market data**, Fundamental **financial metrics**, and Unstructured **news headlines** data to generate a dynamic and **transparent Stability Score**.

Our platform moves beyond a simple "black box" prediction. It provides deep, feature-level explanations for every score, empowering analysts to understand the "why" behind the number and make truly informed decisions.

<!-- 
======================================================================
!!! REPLACE THIS COMMENT WITH YOUR MAIN DASHBOARD SCREENSHOT !!!
Instructions:
1. Take a wide screenshot of the final application.
2. Drag and drop the image into this README file on GitHub.
3. Replace this entire block with the generated image link.
======================================================================
-->
![CredLens Dashboard](https://i.imgur.com/your-main-screenshot-url.png)

## ✨2. Key Features

* ✅ **Multi-Source Data Ingestion:** Ingests data from three distinct sources: **Yahoo Finance** (structured market/fundamental data), **FRED** (structured macroeconomic data), and **NewsAPI** (unstructured news headlines).
* ✅ **"Fundamentals First" Hybrid Scoring Model:** A unique two-part architecture that anchors a company's score in its fundamental financial health and then applies a penalty based on a sophisticated, AI-driven technical risk assessment.
* ✅ **Advanced Explainable AI (XAI):** Uses the industry-standard SHAP (SHapley Additive exPlanations) to provide clear, feature-level breakdowns of what drives each score, making the model's reasoning transparent.
* ✅ **Interactive & Polished Dashboard:** A fluid and intuitive Streamlit UI featuring interactive score gauges, a "Feature Deep Dive" explorer for historical trend analysis, and sentiment-highlighted news headlines.
* ✅ **Intelligent & Robust Fallbacks:** The system is fully resilient. It gracefully handles API failures and can produce a qualitative, rule-based **Heuristic Assessment** for stocks that cannot be scored by the ML model due to insufficient data.
* ✅ **Lightweight MLOps Pipeline:** The entire backend is containerized with **Docker** for perfect reproducibility. It includes an API endpoint to trigger automated background retraining of core models, ensuring the system's intelligence stays fresh without any downtime.

## 🏗️3. System Architecture

Our platform utilizes a modern, decoupled architecture for scalability and maintainability.

*   **Frontend:** A responsive dashboard built with **Streamlit** and deployed on Streamlit Community Cloud.
*   **Backend:** A high-performance API server built with **FastAPI** and deployed as a Docker container on Railway.
*   **ML Engine:** Uses **XGBoost** for the specialized technical model and **Optuna** for efficient, intelligent hyperparameter optimization.

```
+------------------+      +---------------------+      +----------------+
|      User        | ---> |  Streamlit Frontend | <--> |  FastAPI Backend |
+------------------+      +---------------------+      +----------------+
                                                           |
                                     +---------------------+---------------------+
                                     |                     |                     |
                               +---------------+   +---------------+   +---------------+
                               | Yahoo Finance |   |     FRED      |   |    NewsAPI    |
                               +---------------+   +---------------+   +---------------+
```

## ⚖️4. Key Architectural Decisions & Trade-offs

This project's final architecture is the result of solving several complex, real-world challenges.

#### 🔹1. The Challenge: A Flawed, Biased Model
*   **Problem:** Our initial models exhibited a strong "mean-reversion bias," giving dangerously high scores (90+) to volatile stocks like `SMCI` that had recently crashed, ignoring obvious fundamental risks.
*   **Decision:** We abandoned the single-model approach and re-architected to a **"Fundamentals First" two-part system.** A stable, rule-based `fundamental_score` (based on debt, profitability, etc.) acts as an anchor. A specialized `technical_model` then calculates a `technical_penalty` based on market risk. The final score is `fundamental_score - technical_penalty`.
*   **Outcome:** This completely eliminated the bias. A company with poor fundamentals can now **never** achieve a high score, regardless of its market behavior. This makes the final score far more robust and trustworthy.

#### 🔹2. The Challenge: Real-Time Updates vs. UI Latency
*   **Problem:** Retraining a model on every request would provide maximum data freshness but would cause an unacceptable 15-30 second delay in the UI.
*   **Decision:** We implemented a **hybrid training architecture** using FastAPI's `BackgroundTasks`. The user receives an instant score based on the latest data applied to a pre-trained model. In the background, an asynchronous task is triggered to retrain the model with that new data.
*   **Outcome:** The UI is instantaneous, while the model's intelligence is continuously updated, providing the best of both worlds.

## 📊5. Model Performance & Explainability

Our model's goal is to predict periods of future negative returns combined with high volatility. We use a holdout test set and achieve realistic, powerful AUC scores. For example, for a stock like **NVDA**, the model achieved a **Final Test Set AUC Score of ~0.91**.

The platform's core strength is its explainability, which allows an analyst to understand the reasoning behind any score.

<!-- 
======================================================================
!!! REPLACE THIS COMMENT WITH YOUR "WHY THIS SCORE?" SCREENSHOT !!!
Instructions:
1. Take a screenshot of the Key Drivers chart for a stock like BA or SMCI.
2. Drag and drop the image into this README file on GitHub.
3. Replace this entire block with the generated image link.
======================================================================
-->
![Explanation Chart](https://i.imgur.com/your-explanation-screenshot-url.png)

## ⚙️6. How to Run Locally

1️⃣  **Clone Repository:**
    ```bash
    git clone [your-repo-url]
    cd [your-repo-folder]
    ```

2️⃣  **Set Up Environment:**
    *   Create a Python virtual environment: `python -m venv venv`
    *   Activate it: `.\venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
    *   Install dependencies: `pip install -r requirements.txt`

3️⃣  **Configure API Keys:**
    *   In the root directory, create a file named `.env`.
    *   Add your secret keys to this file:
      ```
      NEWS_API_KEY="YOUR_NEWS_API_KEY"
      FRED_API_KEY="YOUR_FRED_API_KEY"
      ```

4️⃣  **Run the Application:**
    *   **Terminal 1 (Backend):** `uvicorn backend.main:app --reload`
    *   **Terminal 2 (Frontend):** `streamlit run frontend/app.py`

5️⃣  Open your browser to the local Streamlit URL 👉 (usually `http://localhost:8501`).

## 🏆 Why CredLens Stands Out  

✨ **Transparent & Explainable → From "Black Box" to Glass Box**  
We don't just provide a score; we provide the reasoning. Using **SHAP** and a clear UI, analysts can instantly see the specific drivers — from market volatility to fundamental debt — that influenced the final number. This builds trust and transforms the platform from a simple predictor into a true intelligence tool.  

✨ **Robust & Reliable → A "Fundamentals First" Architecture**  
Our biggest innovation is our **two-part scoring system**. A stable, rule-based **Fundamental Score** acts as a powerful anchor, preventing the model from being fooled by irrational market hype or biased technical signals. This guarantees that a company with poor financial health can never receive a misleadingly high score — solving a critical flaw found in simpler models.  

✨ **Real-Time Insights, Zero Latency → A Hybrid Training Model**  
Our platform is built for the **now**. It provides **instantaneous scores** based on the latest available data, but intelligently queues up a **full model retraining in the background** using FastAPI's asynchronous tasks. This gives the user a **real-time experience without lag**, while ensuring the system's intelligence is constantly refreshed.  

✨ **Production-Ready & Resilient → Built for the Real World**  
The entire backend is **containerized with Docker** for reproducibility and deployed securely using environment variables. The system is resilient to failure, automatically falling back to a **heuristic assessment** if an ML model cannot be trained — ensuring the user always gets a useful insight.  

---

🔥 **CredLens is not just another score generator — it’s the future of explainable, real-time credit intelligence.**  


## 3. System Architecture & Design

Our platform is built on a modern, decoupled, and scalable architecture. The following diagrams illustrate the key components, data flows, and operational logic that make CredLens a robust and intelligent system.

### System Architecture Diagram

This diagram provides a high-level overview of the core components and their relationships, showcasing the separation between the user-facing frontend, the intelligent backend, and external data services.

```mermaid
graph TD
    %% --- Custom Styling ---
    classDef userStyle fill:#2ECC71,stroke:#333,color:#fff
    classDef frontendStyle fill:#3498DB,stroke:#333,color:#fff
    classDef backendStyle fill:#F39C12,stroke:#333,color:#fff
    classDef apiStyle fill:#95A5A6,stroke:#333,color:#fff

    %% --- Components ---
    subgraph "User Tier"
        User[fa:fa-user Analyst]:::userStyle
    end

    subgraph "Frontend Tier (Streamlit Cloud)"
        Frontend[fa:fa-window-maximize Streamlit Dashboard]:::frontendStyle
    end

    subgraph "Backend Tier (Docker on Railway)"
        BackendAPI[fa:fa-server FastAPI Server]:::backendStyle
        ScoringEngine[fa:fa-cogs Scoring Engine]:::backendStyle
        DataFetcher[fa:fa-database Data Fetcher]:::backendStyle
    end

    subgraph "External Services"
        ExternalAPIs[fa:fa-cloud-download External APIs <br> (Yahoo Finance, FRED, NewsAPI)]:::apiStyle
    end

    %% --- Connections ---
    User -- Interacts --> Frontend
    Frontend -- "API Request (HTTPS)" --> BackendAPI
    BackendAPI -- Manages --> DataFetcher
    BackendAPI -- Manages --> ScoringEngine
    DataFetcher -- Fetches from --> ExternalAPIs
```

### Scoring Logic Flowchart

This flowchart details the innovative **"Fundamentals First"** architecture, which is our unique selling proposition. It ensures that every score is anchored in financial reality, preventing the model from developing dangerous biases.

```mermaid
graph TD
    %% --- Custom Styling ---
    classDef inputStyle fill:#3498DB,stroke:#333,color:#fff
    classDef processStyle fill:#2ECC71,stroke:#333,color:#fff
    classDef modelStyle fill:#8E44AD,stroke:#333,color:#fff
    classDef finalStyle fill:#E74C3C,stroke:#333,color:#fff

    %% --- Flowchart ---
    Start((Ticker Request)):::inputStyle --> FundData[Fetch Fundamental Data <br> (Debt, P/E, Cash)]
    Start --> TechData[Fetch Market & News Data]

    FundData --> FundScore{Calculate Fundamental Score <br> (0-100 Score)}:::processStyle
    
    TechData --> TechModel[Load/Train Technical ML Model <br> (XGBoost + Optuna)]:::modelStyle
    TechModel --> TechRisk{Predict Technical Risk Probability <br> (0.0 to 1.0)}:::modelStyle
    TechRisk --> TechPenalty[Convert to Technical Penalty <br> (0-50 Points)]:::processStyle
    
    FundScore --> FinalCalc[Final Score = <br> Fundamental Score - Technical Penalty]:::finalStyle
    TechPenalty --> FinalCalc
    
    FinalCalc --> Output((Final Stability Score)):::finalStyle
```

### MLOps - Automated Retraining Flowchart

To ensure our models never become stale, we've implemented a lightweight MLOps pipeline. This process runs in the background, triggered either manually via an API endpoint or on a schedule, to keep our core models up-to-date without any service downtime.

```mermaid
graph TD
    %% --- Custom Styling ---
    classDef triggerStyle fill:#8E44AD,stroke:#333,color:#fff
    classDef processStyle fill:#3498DB,stroke:#333,color:#fff
    classDef successStyle fill:#2ECC71,stroke:#333,color:#fff

    %% --- Flowchart ---
    Trigger((fa:fa-clock-o Start Retraining Job)):::triggerStyle --> Fetch[Fetch Fresh Data for Core Tickers <br> (AAPL, MSFT, etc.)]
    Fetch --> Engineer[Engineer All Features]:::processStyle
    Engineer --> Tune[Run Optuna Hyperparameter Tuning]:::processStyle
    Tune --> Train[Train a New, Optimized Model]:::processStyle
    Train --> Save[Overwrite Old .joblib File <br> with New Model]:::processStyle
    Save --> End((fa:fa-check-circle Job Complete)):::successStyle
```

### Deployment Diagram

The entire application is deployed on modern, scalable cloud infrastructure using a fully containerized approach.

```mermaid
graph TD
    %% --- Custom Styling ---
    classDef userStyle fill:#2ECC71,stroke:#333,color:#fff
    classDef cloudStyle fill:#ECF0F1,stroke:#bdc3c7
    classDef containerStyle fill:#3498DB,stroke:#2980B9,color:#fff
    classDef serviceStyle fill:#9B59B6,stroke:#8E44AD,color:#fff

    %% --- Diagram ---
    subgraph "User's Machine"
        Browser[fa:fa-globe Browser]:::userStyle
    end

    subgraph "Cloud Infrastructure"
        subgraph "Streamlit Community Cloud"
            style Streamlit Community Cloud fill:#f0f8ff,stroke:#333,stroke-dasharray: 5 5
            Frontend[
                **Streamlit Frontend Service**<br/>
                `app.py`
            ]:::serviceStyle
        end

        subgraph "Railway"
            style Railway fill:#e6e6fa,stroke:#333,stroke-dasharray: 5 5
            Backend[
                **FastAPI Backend Service**<br/>
                fa:fa-docker Docker Container
            ]:::containerStyle
        end
    end
    
    Browser -- "HTTPS" --> Frontend
    Frontend -- "REST API (HTTPS)" --> Backend

