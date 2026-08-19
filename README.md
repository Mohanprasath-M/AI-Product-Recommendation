# NexusAI — AI Product Recommendation & Customer Intelligence Platform

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB.svg)](https://reactjs.org/)
[![Vite](https://img.shields.io/badge/Vite-5.4-646CFF.svg)](https://vitejs.dev/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.4-38B2AC.svg)](https://tailwindcss.com/)
[![Scikit-Learn](https://img.shields.io/badge/ML-Scikit--Learn-F7931E.svg)](https://scikit-learn.org/)
[![MySQL](https://img.shields.io/badge/MySQL-Workbench%20Ready-4479A1.svg)](https://www.mysql.com/products/workbench/)
[![Tests](https://img.shields.io/badge/Tests-12%20Passed-brightgreen.svg)]()

A complete, production-level, full-stack **AI Product Recommendation & Customer Intelligence Platform** combining real-time behavioral event streaming, local machine learning & NLP engines (100% locally executed without external API dependencies), customer segmentation, lifetime value forecasting, churn risk detection, and dynamic A/B test tuning.

---

## 🌟 Key Platform Features

- **Hybrid Recommendation Engine**:
  - **Content-Based Filtering**: TF-IDF vectorization over item tags/specs & cosine similarity matrix.
  - **Collaborative Filtering**: Interaction matrix weighting + TruncatedSVD Matrix Factorization latent factors.
  - **Real-Time Behavioral Booster**: Session intent weighting with recency decay factors.
  - **Association / Market Basket Rules**: "Frequently Bought Together" affinity mining.
  - **Transparent Explainability**: Human-readable explanations ("Why Recommended") attached to every recommendation item.
  - **Cold Start Fallback Strategies**: Smooth fallbacks for new users or items with zero history.
- **Customer Intelligence Suite**:
  - **Statistical CLV**: Historical vs. forward-looking 12-month retention estimated Customer Lifetime Value.
  - **Churn Risk Model**: Multi-signal scoring (inactivity cadence, purchase lapse, cart abandonment).
  - **Behavioral Funnel Analysis**: Step-by-step conversion tracking (`Search` → `View` → `Click` → `Wishlist` → `Cart` → `Purchase`).
  - **Recommended Actions**: Automated AI retention next-best-action suggestions.
- **Customer Segmentation (K-Means)**:
  - Unsupervised clustering ($k=5$) with automated persona generation (e.g., *High-Value VIPs*, *Loyal Frequent Buyers*, *Budget & Discount Seekers*).
- **Review Sentiment & Topic NLP**:
  - Local NLP classifier (TF-IDF + Logistic Regression) classifying reviews into `POSITIVE`, `NEUTRAL`, `NEGATIVE`.
  - Automated positive/negative topic extraction (e.g. `+sound`, `+comfort`, `-battery`).
- **Real-Time Event Streaming**:
  - Live WebSockets + Redis caching & pub/sub with live dashboard activity feeds.
- **Role-Based Access Control (RBAC)**:
  - `CUSTOMER`, `ADMIN`, and `ANALYST` dedicated portals with 1-click persona switching.

---

## 🏛️ System Architecture

```mermaid
flowchart TB
    subgraph Frontend["React 18 + Vite + TypeScript + Tailwind CSS"]
        UI_Customer["Customer Storefront & Feed"]
        UI_Admin["Executive & Product Admin"]
        UI_Analyst["Analyst & NLP Suite"]
        WS_Client["WebSocket Live Client"]
    end

    subgraph Backend["FastAPI Backend (Port 8000)"]
        API_Auth["JWT Auth & RBAC"]
        API_Catalog["Product Catalog CRUD"]
        API_Rec["Hybrid Recommendation API"]
        API_Analytics["Customer & Search Intelligence"]
        API_ML["Model Registry & Retraining"]
        WS_Server["WebSocket Event Hub"]
    end

    subgraph MLEngines["Local Machine Learning Engine"]
        CB["TF-IDF Content Similarity"]
        SVD["SVD Matrix Factorization"]
        KM["K-Means Segmentation"]
        NLP["Review Sentiment Classifier"]
        MBA["Market Basket Association"]
    end

    subgraph Storage["Storage & Caching Layer"]
        MySQL[(MySQL / Workbench / SQLite DB)]
        Redis[(Redis Pub/Sub & Memory Cache)]
        ModelStore[(Serialized Joblib Models)]
    end

    UI_Customer -->|Browse / Track| Backend
    UI_Admin -->|Configure / Retrain| Backend
    UI_Analyst -->|Analyze| Backend
    WS_Server <--> WS_Client

    API_Rec --> MLEngines
    API_Analytics --> MLEngines
    Backend --> MySQL
    Backend --> Redis
    MLEngines --> ModelStore
```

---

## 🗄️ Database Setup & MySQL Workbench Support

The database natively supports **MySQL 8.0+**, **PostgreSQL**, and **SQLite**.

### Running inside MySQL Workbench:
1. Open **MySQL Workbench**.
2. Connect to your MySQL Server (e.g., `localhost:3306`).
3. Open the file [`scripts/schema_mysql.sql`](file:///c:/Users/kisho/Downloads/AI-Product-Recommendation/scripts/schema_mysql.sql).
4. Click the ⚡ **Execute** button in MySQL Workbench.
5. In your `.env` file, configure:
   ```env
   DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/ai_recommendation_db
   ```

*Note: For zero-config immediate local development without MySQL installed, SQLite is enabled by default (`sqlite:///./ai_recommendation.db`).*

---

## 🚀 Quickstart Guide

### 1. Install Dependencies

#### Backend:
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate      # Windows (or: source venv/bin/activate on Linux/Mac)
pip install -r requirements.txt
cd ..
```

#### Frontend:
```bash
cd frontend
npm install
cd ..
```

### 2. Generate Demo Datasets & Train Models
Generates 1,000+ customers, 500+ products, 20,000+ interactions, 5,000+ purchases, and 5,000+ reviews:
```bash
# Generate synthetic dataset
python scripts/generate_demo_data.py

# Seed database
python scripts/seed_database.py

# Train ML models (TF-IDF, SVD, K-Means, NLP Sentiment)
python scripts/train_models.py

# Run benchmark evaluation
python scripts/evaluate_models.py
```

### 3. Run Application (2 Terminals)

#### Terminal 1 — Backend (FastAPI on Port 8000):
```bash
cd backend
.\venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```
- Interactive API Docs (Swagger): `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`

#### Terminal 2 — Frontend (React + Tailwind on Port 5173):
```bash
cd frontend
npm run dev
```
- Storefront Web App: `http://localhost:5173`

---

## 👥 Default Demo User Accounts

| Role | Email | Password | Access Capabilities |
| :--- | :--- | :--- | :--- |
| **Admin** | `admin@platform.ai` | `Admin@123456` | Executive KPIs, Catalog CRUD, MLOps retraining, A/B weights |
| **Analyst** | `analyst@platform.ai` | `Analyst@123456` | Funnel analytics, K-Means clustering, NLP Sentiment, Search stats |
| **Customer** | `customer@platform.ai` | `Customer@123456` | Personalized feed, shopping cart, checkout, review submission |

*(You can also use the ⚡ 1-Click Quick Persona Switcher in the top navigation bar to switch between roles anytime).*

---

## 🧪 Running Automated Tests

Run backend unit and integration tests with `pytest`:
```bash
cd backend
.\venv\Scripts\activate
pytest tests -v
```

Build the frontend bundle:
```bash
cd frontend
npm run build
```

---

## 📡 API Endpoints Overview

- `POST /api/auth/login` — JWT access and refresh token issuance.
- `GET /api/products` — Catalog with search, multi-category/brand filtering, and sorting.
- `GET /api/recommendations/{customer_id}` — Personalized hybrid AI recommendations with explainability reasons.
- `GET /api/recommendations/product/{id}/similar` — Content-based product similarity.
- `GET /api/recommendations/product/{id}/bought-together` — Market basket association items.
- `POST /api/events/track` — Real-time event tracking (`VIEW_PRODUCT`, `ADD_TO_CART`, `PURCHASE`).
- `POST /api/reviews` — Review submission with automated NLP sentiment classification.
- `GET /api/analytics/overview` — Executive KPIs, revenue trends, and conversion metrics.
- `POST /api/ml/train` — Trigger background ML retraining.
- `WS /ws` — Real-time WebSocket event broadcaster.

---

## 📄 License
MIT License. Built for production-grade AI Product Recommendation & Customer Intelligence.
