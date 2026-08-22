# Customer Intelligence Platform

> An end-to-end Customer Analytics, Machine Learning, Business
> Intelligence, and Full-Stack application for understanding customer
> behavior, value, retention, segmentation, and churn risk.

## Table of Contents

-   [1. Introduction](#1-introduction)
-   [2. Project Objectives](#2-project-objectives)
-   [3. Business Problem](#3-business-problem)
-   [4. Key Features](#4-key-features)
-   [5. Technology Stack](#5-technology-stack)
-   [6. System Architecture](#6-system-architecture)
-   [7. Project Structure](#7-project-structure)
-   [8. Current Project Status](#8-current-project-status)
-   [9. Prerequisites](#9-prerequisites)
-   [10. Installation](#10-installation)
-   [11. PostgreSQL Setup](#11-postgresql-setup)
-   [12. Environment Variables](#12-environment-variables)
-   [13. Python Virtual Environment](#13-python-virtual-environment)
-   [14. Backend Dependencies](#14-backend-dependencies)
-   [15. Frontend Dependencies](#15-frontend-dependencies)
-   [16. Data Pipeline](#16-data-pipeline)
-   [17. Machine Learning Pipeline](#17-machine-learning-pipeline)
-   [18. Database Import](#18-database-import)
-   [19. Running the Backend](#19-running-the-backend)
-   [20. Running the Frontend](#20-running-the-frontend)
-   [21. API Verification](#21-api-verification)
-   [22. Dashboard](#22-dashboard)
-   [23. Customer Analytics](#23-customer-analytics)
-   [24. Customer Segmentation](#24-customer-segmentation)
-   [25. Retention Analytics](#25-retention-analytics)
-   [26. Churn Prediction](#26-churn-prediction)
-   [27. Development Workflow](#27-development-workflow)
-   [28. Troubleshooting](#28-troubleshooting)
-   [29. Security and Git](#29-security-and-git)
-   [30. Recommended Next Steps](#30-recommended-next-steps)
-   [31. Production Readiness](#31-production-readiness)
-   [32. Conclusion](#32-conclusion)

------------------------------------------------------------------------

# 1. Introduction

The **Customer Intelligence Platform** is a full-stack analytics and
machine-learning application designed to convert customer transaction
data into actionable business intelligence.

The system combines:

1.  Data preprocessing
2.  Feature engineering
3.  Customer segmentation
4.  Churn prediction
5.  Retention analytics
6.  PostgreSQL data storage
7.  FastAPI REST APIs
8.  React-based visualization

The platform follows an end-to-end architecture:

``` text
Raw Transaction Data
        |
        v
Data Preprocessing
        |
        v
Feature Engineering
        |
        +----------------------+
        |                      |
        v                      v
Customer Segmentation     Churn Prediction
        |                      |
        +----------+-----------+
                   |
                   v
          Processed Data
                   |
                   v
              PostgreSQL
                   |
                   v
                FastAPI
                   |
                   v
              React Frontend
                   |
                   v
        Customer Intelligence
             Dashboard
```

The project is intended to demonstrate practical skills across **Data
Analytics, Machine Learning, Backend Development, Database Engineering,
and Business Intelligence**.

------------------------------------------------------------------------

# 2. Project Objectives

The primary objectives are:

-   Process raw customer transaction data.
-   Clean and prepare data for analytics and machine learning.
-   Generate customer-level behavioral features.
-   Calculate RFM and additional customer-value features.
-   Store processed information in PostgreSQL.
-   Build reusable REST APIs using FastAPI.
-   Segment customers into meaningful behavioral/value groups.
-   Predict customer churn risk.
-   Identify customers that may contribute to revenue at risk.
-   Analyze customer retention.
-   Build an interactive business dashboard.
-   Provide a professional end-to-end analytics project suitable for
    portfolio/resume presentation.

------------------------------------------------------------------------

# 3. Business Problem

Businesses often have large amounts of transaction data but limited
visibility into questions such as:

-   Who are the most valuable customers?
-   Which customers are loyal?
-   Which customers are becoming inactive?
-   Which customer segments generate the most revenue?
-   Which customers are at risk of churn?
-   How much revenue is associated with high-risk customers?
-   How frequently do customers purchase?
-   How can retention strategies be targeted?

This project addresses these questions by transforming raw transactional
records into customer intelligence.

------------------------------------------------------------------------

# 4. Key Features

## 4.1 Executive Dashboard

The dashboard provides high-level KPIs including:

-   Total Customers
-   Total Orders
-   Total Revenue
-   Revenue at Risk
-   Monthly Revenue Trend
-   Customer Segment Distribution
-   Top Customers

The currently verified dashboard displays approximately:

``` text
Total Customers : 5,878
Total Orders    : 36,969
Total Revenue   : £17,684,595
```

These values are dependent on the current dataset and may change after
reprocessing.

------------------------------------------------------------------------

## 4.2 Customer Analytics

The customer module is designed to provide:

-   Customer profiles
-   Customer value metrics
-   Purchase behavior
-   Transaction information
-   Customer segment
-   Search/filter functionality
-   Customer-level analytics

------------------------------------------------------------------------

## 4.3 Customer Segmentation

Customer behavior is analyzed using features such as:

-   Recency
-   Frequency
-   Monetary value
-   Average order value
-   Customer lifetime
-   Total quantity
-   Unique products
-   Purchase intervals
-   Active months
-   Monthly orders
-   Monthly revenue

Business-oriented segments may include:

-   Champions
-   Loyal Customers
-   Potential Loyalists
-   At-Risk Customers
-   New Customers

The exact segments depend on the implemented segmentation logic.

------------------------------------------------------------------------

## 4.4 Retention Analytics

The retention module is designed to analyze:

-   Repeat purchases
-   Customer activity
-   Purchase intervals
-   Returning customers
-   Retention rates
-   Cohort retention
-   Customer lifetime

------------------------------------------------------------------------

## 4.5 Churn Prediction

The churn module is designed to:

-   Predict churn probability.
-   Classify customer risk.
-   Identify high-risk customers.
-   Calculate potential revenue at risk.
-   Support customer-retention decisions.

Typical risk categories are:

``` text
Low Risk
Medium Risk
High Risk
```

------------------------------------------------------------------------

# 5. Technology Stack

## Backend

  Technology     Purpose
  -------------- ----------------------
  Python 3.11    Core language
  FastAPI        REST API framework
  Uvicorn        ASGI server
  SQLAlchemy     ORM
  PostgreSQL     Database
  Psycopg2       PostgreSQL driver
  Pandas         Data processing
  NumPy          Numerical processing
  Scikit-learn   Machine learning
  Joblib         Model persistence

## Frontend

  Technology         Purpose
  ------------------ -----------------------
  React              Frontend application
  JavaScript         Application logic
  HTML/CSS           UI
  npm                Dependency management
  Charting library   Data visualization

## Development

-   Visual Studio Code
-   Git
-   GitHub
-   PostgreSQL / pgAdmin
-   PowerShell
-   Docker (optional)

------------------------------------------------------------------------

# 6. System Architecture

``` text
                       +----------------+
                       |   Raw Dataset  |
                       +-------+--------+
                               |
                               v
                    +----------------------+
                    | Preprocessing        |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Feature Engineering  |
                    +----------+-----------+
                               |
                 +-------------+-------------+
                 |                           |
                 v                           v
       +-------------------+       +-------------------+
       | Segmentation      |       | Churn Model       |
       +---------+---------+       +---------+---------+
                 |                           |
                 +-------------+-------------+
                               |
                               v
                    +----------------------+
                    | Processed CSV / ML   |
                    | Model Outputs        |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | PostgreSQL Database  |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | FastAPI Backend      |
                    +----------+-----------+
                               |
                               | REST API
                               v
                    +----------------------+
                    | React Frontend       |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Intelligence         |
                    | Dashboard            |
                    +----------------------+
```

------------------------------------------------------------------------

# 7. Project Structure

The current project is organized approximately as follows:

``` text
Customer Intelligence Platform/
│
├── .venv/
│
├── backend/
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── analytics.py
│   │   ├── churn.py
│   │   ├── customers.py
│   │   └── segmentation.py
│   │
│   ├── __init__.py
│   ├── .env
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
│
├── data/
│   ├── raw/
│   └── processed/
│       ├── customer_features.csv
│       └── transactions.csv
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── ...
│
├── ml/
│   ├── preprocessing.py
│   ├── feature_engineering.py
│   ├── segmentation.py
│   └── churn_model.py
│
├── models/
│   └── trained model files
│
├── notebooks/
│   └── 01_data_exploration.ipynb, 02_customer_features.ipynb, 03_rfm_segmentation.ipynb, 
        04_chum_prediction.ipynb, 05_retention_analysis.ipynb
│
├── sql/
│   └── SQL scripts(customer_analysis.sql, retention.sql, schema.sql, segmentation.sql)
│
├── .gitignore
├── docker-compose.yml
├── README.md
└── requirements.txt
```

The exact contents may evolve during development.

------------------------------------------------------------------------

# 8. Current Project Status

## Completed and verified

-   Data preprocessing pipeline
-   Customer feature generation
-   Transaction processing
-   PostgreSQL connection
-   SQLAlchemy database models
-   Database table creation
-   Customer data import
-   Transaction data import
-   Chunk-based transaction loading
-   FastAPI backend
-   CORS configuration
-   Customer routes
-   Segmentation routes
-   Churn routes
-   Analytics routes
-   React frontend
-   Frontend/backend integration
-   Dashboard KPI cards
-   Revenue trend chart
-   Customer segment chart
-   Dashboard data loading

The currently verified data import contains approximately:

``` text
5,878 customers
769,025 transaction records checked
36,969 unique invoices/orders
```

## Still requiring complete verification

-   Customers page
-   Segmentation page
-   Retention page
-   Churn Prediction page
-   End-to-end churn-risk calculation
-   Revenue-at-risk validation
-   Production deployment
-   Automated tests

Therefore, the project is currently in **development/testing stage**,
with the core dashboard operational.

------------------------------------------------------------------------

# 9. Prerequisites

Install the following before starting.

## Python

Recommended:

``` text
Python 3.11
```

Verify:

``` powershell
python --version
```

------------------------------------------------------------------------

## Node.js

Install a current Node.js LTS version.

Verify:

``` powershell
node --version
npm --version
```

------------------------------------------------------------------------

## PostgreSQL

Install PostgreSQL and make sure the PostgreSQL server is running.

Verify:

``` powershell
psql --version
```

------------------------------------------------------------------------

## Git

Verify:

``` powershell
git --version
```

------------------------------------------------------------------------

# 10. Installation

Clone the repository if necessary:

``` powershell
git clone <YOUR_REPOSITORY_URL>
cd "Customer Intelligence Platform"
```

Or, if the project already exists locally:

``` powershell
cd "C:\path\to\Customer Intelligence Platform"
```

------------------------------------------------------------------------

# 11. PostgreSQL Setup

Create the project database.

Example:

``` sql
CREATE DATABASE customer_intelligence;
```

Make sure the PostgreSQL service is running.

The application should connect using a URL following this structure:

``` text
postgresql+psycopg2://USERNAME:PASSWORD@HOST:PORT/DATABASE
```

For local development:

``` text
postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/customer_intelligence
```

Do not put the real password in this README.

------------------------------------------------------------------------

# 12. Environment Variables

Create:

``` text
backend/.env
```

Example:

``` env
DATABASE_URL=postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/customer_intelligence
```

Replace `YOUR_PASSWORD` with the actual PostgreSQL password.

Never commit real credentials.

------------------------------------------------------------------------

# 13. Python Virtual Environment

From the project root:

``` powershell
python -m venv .venv
```

Activate:

``` powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation:

``` powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then:

``` powershell
.\.venv\Scripts\Activate.ps1
```

Upgrade pip:

``` powershell
python -m pip install --upgrade pip
```

------------------------------------------------------------------------

# 14. Backend Dependencies

Install from the project's dependency file:

``` powershell
pip install -r requirements.txt
```

If the requirements file is incomplete, the primary packages include:

``` powershell
pip install fastapi uvicorn[standard] sqlalchemy psycopg2-binary python-dotenv pandas numpy scikit-learn joblib
```

Verify:

``` powershell
pip list
```

The project's `requirements.txt` should be treated as the source of
truth once finalized.

------------------------------------------------------------------------

# 15. Frontend Dependencies

Open another terminal:

``` powershell
cd frontend
```

Install:

``` powershell
npm install
```

Run:

``` powershell
npm run dev
```

The development server should normally run on:

``` text
http://localhost:5173
```

------------------------------------------------------------------------

# 16. Data Pipeline

The data pipeline converts raw transaction data into customer-level
analytical data.

``` text
Raw Transactions
       |
       v
Preprocessing
       |
       v
Clean Transaction Data
       |
       v
Feature Engineering
       |
       v
Customer-Level Features
       |
       +-------------------+
       |                   |
       v                   v
Segmentation        Churn Prediction
       |                   |
       +---------+---------+
                 |
                 v
        Processed Outputs
```

------------------------------------------------------------------------

# 17. Machine Learning Pipeline

The current ML scripts are:

``` text
ml/preprocessing.py
ml/feature_engineering.py
ml/segmentation.py
ml/churn_model.py
```

Run them from the project root.

### Step 1 --- Preprocessing

``` powershell
python ml/preprocessing.py
```

### Step 2 --- Feature Engineering

``` powershell
python ml/feature_engineering.py
```

### Step 3 --- Segmentation

``` powershell
python ml/segmentation.py
```

### Step 4 --- Churn Model

``` powershell
python ml/churn_model.py
```

After execution, verify:

``` text
data/processed/
```

and:

``` text
models/
```

for the expected output files.

------------------------------------------------------------------------

# 18. Database Import

When FastAPI starts, the application:

1.  Creates required tables.
2.  Locates processed customer data.
3.  Imports customer records.
4.  Locates processed transaction data.
5.  Reads transactions in chunks.
6.  Checks for existing records.
7.  Inserts only new records.
8.  Starts the API.

The chunked approach avoids unnecessarily loading a very large
transaction file into memory.

Seeing output such as:

``` text
New customers: 0
Skipped customers: 5878
```

means the customer records already exist.

Similarly:

``` text
New transactions: 0
Skipped transactions: 769025
```

means those records were already present and duplicate insertion was
avoided.

This is expected behavior.

------------------------------------------------------------------------

# 19. Running the Backend

From the project root:

``` powershell
.\.venv\Scripts\Activate.ps1
```

Then:

``` powershell
python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Expected:

``` text
INFO: Uvicorn running on http://127.0.0.1:8000
INFO: Application startup complete.
```

Keep this terminal running.

------------------------------------------------------------------------

# 20. Running the Frontend

Open a second terminal:

``` powershell
cd "C:\path\to\Customer Intelligence Platform\frontend"
```

Install dependencies if necessary:

``` powershell
npm install
```

Start:

``` powershell
npm run dev
```

Then open the frontend URL displayed by Vite, normally:

``` text
http://localhost:5173
```

------------------------------------------------------------------------

# 21. API Verification

Before opening the frontend, verify the backend.

## Root endpoint

``` text
http://127.0.0.1:8000/
```

Expected:

``` json
{
  "application": "Customer Intelligence Platform",
  "version": "1.0.0",
  "status": "running"
}
```

## Health endpoint

``` text
http://127.0.0.1:8000/health
```

Expected:

``` json
{
  "status": "healthy"
}
```

## Swagger

``` text
http://127.0.0.1:8000/docs
```

Swagger should show the registered:

-   Customers APIs
-   Segmentation APIs
-   Churn APIs
-   Analytics APIs

------------------------------------------------------------------------

# 22. Dashboard

The current dashboard is operational.

It provides:

``` text
+-------------------+-------------------+
| Total Customers   | Total Orders      |
| 5,878             | 36,969            |
+-------------------+-------------------+
| Total Revenue     | Revenue at Risk   |
| £17,684,595       | £0                |
+-------------------+-------------------+
```

It also contains:

-   Revenue Trend
-   Customer Segments
-   Top Customers

The current dashboard successfully communicates with the FastAPI
backend.

------------------------------------------------------------------------

# 23. Customer Analytics

The Customers module should provide a detailed view of individual
customers.

Recommended information:

-   Customer ID
-   Recency
-   Frequency
-   Monetary value
-   Average order value
-   Customer lifetime
-   Total quantity
-   Unique products
-   Segment
-   Churn probability
-   Risk level

Recommended functionality:

-   Search customer
-   Filter customers
-   Sort by value
-   Sort by recency
-   View customer details
-   View transaction history

------------------------------------------------------------------------

# 24. Customer Segmentation

The segmentation pipeline uses customer behavioral features.

Typical workflow:

``` text
Customer Transactions
        |
        v
Customer Aggregation
        |
        v
Feature Engineering
        |
        v
Feature Scaling
        |
        v
Clustering
        |
        v
Customer Cluster
        |
        v
Business Segment
```

The segmentation dashboard should ideally provide:

-   Number of segments
-   Customers per segment
-   Revenue per segment
-   Average customer value
-   Average frequency
-   Average recency
-   Segment descriptions

The currently visible dashboard contains segment categories such as:

``` text
Loyal Customers
Champions
```

The full segmentation output should be validated against the ML
pipeline.

------------------------------------------------------------------------

# 25. Retention Analytics

Retention analytics should answer:

-   How many customers return?
-   How frequently do they return?
-   What is the repeat-purchase rate?
-   Which cohorts retain best?
-   Which segments have weak retention?
-   How long do customers remain active?

Useful future metrics:

``` text
Repeat Customer Rate
Retention Rate
Average Purchase Interval
Customer Lifetime
Active Months
Cohort Retention
```

A recommended visualization is a cohort retention matrix.

------------------------------------------------------------------------

# 26. Churn Prediction

The churn pipeline should follow:

``` text
Customer Features
       |
       v
Feature Preparation
       |
       v
Trained ML Model
       |
       v
Churn Probability
       |
       v
Risk Category
       |
       v
Revenue at Risk
```

Recommended model evaluation:

``` text
Accuracy
Precision
Recall
F1 Score
ROC-AUC
Confusion Matrix
```

For churn prediction, do not rely only on accuracy when the classes are
imbalanced.

The dashboard currently shows:

``` text
Revenue at Risk: £0
0 high-risk customers
```

This should be validated against the actual churn predictions. It can be
correct if there are genuinely no high-risk customers, but it may also
indicate that the final churn model output has not yet been fully
connected to the dashboard.

------------------------------------------------------------------------

# 27. Development Workflow

Use the following workflow whenever the project is rebuilt from the
beginning.

## Step 1 --- Start PostgreSQL

Ensure the PostgreSQL service is running.

## Step 2 --- Activate Python

``` powershell
.\.venv\Scripts\Activate.ps1
```

## Step 3 --- Process data

``` powershell
python ml/preprocessing.py
python ml/feature_engineering.py
python ml/segmentation.py
python ml/churn_model.py
```

## Step 4 --- Start backend

``` powershell
python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

## Step 5 --- Verify backend

Open the root, health, and Swagger endpoints.

## Step 6 --- Start frontend

In another terminal:

``` powershell
cd frontend
npm install
npm run dev
```

## Step 7 --- Test the application

Open the frontend and test:

``` text
Dashboard
Customers
Segmentation
Retention
Churn Prediction
```

------------------------------------------------------------------------

# 28. Troubleshooting

## 28.1 PostgreSQL connection error

If you see:

``` text
could not translate host name
```

check:

-   PostgreSQL is running.
-   The host is correct.
-   The port is correct.
-   The database exists.
-   The username/password are correct.
-   `DATABASE_URL` is correctly formatted.

Correct pattern:

``` text
postgresql+psycopg2://USER:PASSWORD@localhost:5432/DATABASE
```

------------------------------------------------------------------------

## 28.2 Dashboard cannot load data

First verify:

``` text
/health
```

Then open:

``` text
/docs
```

If both work, refresh the React application and inspect:

``` text
F12 -> Console
F12 -> Network
```

Also watch the FastAPI terminal.

### HTTP 404

Usually means:

``` text
Frontend API URL != FastAPI route
```

### HTTP 500

Usually means a backend/database/query/model error.

### CORS error

Check the frontend origin in the FastAPI CORS configuration.

### Connection refused

Usually means the FastAPI server is not running or the frontend is using
the wrong backend port.

------------------------------------------------------------------------

## 28.3 Frontend dependency error

Run:

``` powershell
cd frontend
npm install
npm run dev
```

If necessary:

``` powershell
Remove-Item -Recurse -Force node_modules
Remove-Item package-lock.json
npm install
npm run dev
```

------------------------------------------------------------------------

## 28.4 Backend module error

Always start Uvicorn from the **project root**:

``` powershell
python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Do not normally run:

``` powershell
python backend/main.py
```

when the project is structured around the `backend` package.

------------------------------------------------------------------------

## 28.5 Duplicate data

The import process checks existing customer and transaction records.

Therefore, rerunning the backend should not necessarily create duplicate
records.

Expected behavior can be:

``` text
New customers: 0
Skipped customers: 5878
New transactions: 0
Skipped transactions: 769025
```

------------------------------------------------------------------------

# 29. Security and Git

Never commit credentials.

Recommended `.gitignore`:

``` gitignore
# Python
.venv/
__pycache__/
*.pyc

# Environment files
.env
backend/.env

# Node
node_modules/
dist/

# IDE
.vscode/

# Logs
*.log

# OS
.DS_Store
Thumbs.db
```

Never publish:

-   PostgreSQL passwords
-   API keys
-   Secret tokens
-   Private credentials
-   Production database credentials

Use environment variables.

------------------------------------------------------------------------

# 30. Recommended Next Steps

The project should now proceed in the following order.

## Phase 1 --- Finish Customers

Implement and verify:

-   Customer table
-   Search
-   Filters
-   Sorting
-   Customer detail page
-   Transaction history
-   Customer metrics

## Phase 2 --- Finish Segmentation

Verify:

-   Cluster generation
-   Segment mapping
-   Segment counts
-   Segment revenue
-   Segment-level KPIs
-   Segment visualization

## Phase 3 --- Finish Retention

Implement:

-   Repeat customer rate
-   Retention rate
-   Cohort analysis
-   Retention trend
-   Customer activity analysis

## Phase 4 --- Finish Churn

Verify:

-   Trained model
-   Model loading
-   Churn probability
-   Risk categories
-   High-risk customers
-   Revenue at risk
-   Model evaluation metrics

## Phase 5 --- Improve Dashboard

Add:

-   Date filters
-   Country filters
-   Segment filters
-   Churn-risk distribution
-   Retention chart
-   Revenue by segment
-   Customer lifetime value
-   Geographic analysis
-   Export/report functionality

## Phase 6 --- Testing

Add:

-   Backend unit tests
-   API integration tests
-   Database tests
-   ML evaluation scripts
-   Frontend tests
-   End-to-end tests

------------------------------------------------------------------------

# 31. Production Readiness

The current system is a local development application.

Before deployment, implement:

## Backend

-   Authentication
-   Authorization
-   HTTPS
-   Production ASGI configuration
-   Structured logging
-   Error monitoring
-   API versioning
-   Rate limiting

## Database

-   Database migrations
-   Index optimization
-   Backups
-   Connection pooling
-   Production credentials
-   Access control

## Machine Learning

-   Model versioning
-   Reproducible training
-   Model evaluation
-   Feature versioning
-   Drift monitoring
-   Prediction monitoring

## Frontend

Build the production application:

``` powershell
npm run build
```

Then deploy the generated production assets using the selected hosting
platform.

## Infrastructure

Docker can be used to standardize deployment:

``` text
React
  |
  v
Backend Container
  |
  v
PostgreSQL Container
```

The existing `docker-compose.yml` can be expanded as the project becomes
deployment-ready.

------------------------------------------------------------------------

# 32. Conclusion

The **Customer Intelligence Platform** is an end-to-end project
combining:

-   Data Analytics
-   Machine Learning
-   Customer Segmentation
-   Churn Prediction
-   Retention Analytics
-   PostgreSQL
-   FastAPI
-   React
-   Business Intelligence

The implemented architecture successfully connects:

``` text
Data
  ↓
Processing
  ↓
Feature Engineering
  ↓
Machine Learning
  ↓
PostgreSQL
  ↓
FastAPI
  ↓
React
  ↓
Interactive Dashboard
```

The currently verified implementation successfully loads customer and
transaction data, starts the FastAPI backend, connects the React
frontend, and displays the customer intelligence dashboard.

The next major objective is to fully validate and complete:

``` text
Customers
Segmentation
Retention
Churn Prediction
```

After these modules are completed and tested, the project can be
extended with authentication, advanced analytics, automated testing,
Docker deployment, model monitoring, and production infrastructure.

------------------------------------------------------------------------

## Quick Start

### Terminal 1 --- Backend

From the project root:

``` powershell
.\.venv\Scripts\Activate.ps1
python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

### Terminal 2 --- Frontend

``` powershell
cd frontend
npm install
npm run dev
```

### Browser

Open the frontend URL shown by Vite, normally:

``` text
http://localhost:5173
```

### Backend verification

``` text
http://127.0.0.1:8000/
http://127.0.0.1:8000/health
http://127.0.0.1:8000/docs
```

------------------------------------------------------------------------

## Project Status

**Development Status: Dashboard Operational --- Remaining Modules Under
Validation**

The core data-processing, database, backend, frontend integration, and
dashboard pipeline has been successfully established. The next
development stage is to complete and validate the Customers,
Segmentation, Retention, and Churn Prediction modules.

------------------------------------------------------------------------

**Customer Intelligence Platform**\
*End-to-end Customer Analytics, Machine Learning, and Business
Intelligence*
