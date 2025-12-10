
🚀 Overview

SenseX is a fully automated, production-style Machine Learning pipeline built to process sensor data, train predictive models, and deploy them using Docker and AWS.
This project focuses on predictive maintenance, transforming raw sensor inputs into actionable insights.

It replicates how real ML systems run in companies — with pipelines, automation, deployment, and monitoring.

🧠 Core Features
✔ Data Engineering

Reads and preprocesses sensor data

Schema validation + drift detection

Missing value checks

Scaling, encoding, and feature transformation

✔ Model Engineering

Trains multiple ML models

Selects the best-performing model

Saves the final model in a registry (saved_models/)

✔ Deployment Ready

FastAPI endpoint for real-time predictions

Dockerized application

Automated CI/CD with GitHub Actions

AWS deployment (ECR + EC2)

🏗 Architecture
Raw Data → Data Ingestion → Validation → Transformation → Model Training → Evaluation → Model Pusher → Deployment

📁 Project Structure
sensor/
 ├── components/
 ├── pipelines/
 ├── config/
 ├── utils/
 ├── artifacts/
 └── saved_models/
main.py
app.py
Dockerfile
requirements.txt

⚙️ Tech Stack

Python 3.10

Scikit-learn

Pandas / NumPy

FastAPI

Docker

GitHub Actions (CI/CD)

AWS EC2 + ECR

▶️ How to Run Locally
1️⃣ Create Environment
conda create -n sensor python=3.10 -y
conda activate sensor

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Run Training Pipeline
python main.py

4️⃣ Start FastAPI Server
uvicorn app:app --reload


API will start at:
📍 http://127.0.0.1:8000

🐳 Docker Usage
Build Image
docker build -t sensor-app .

Run Container
docker run -p 8080:8080 sensor-app

☁️ AWS Deployment (Summary)

Build Docker image

Push to AWS ECR

Pull image on EC2 instance

Run the container

GitHub Actions automates builds + deployments

🎯 Why I Built SenseX

To understand how real machine learning projects work outside notebooks.

I wanted hands-on experience with:

ML pipelines

Dockerization

CI/CD workflows

Cloud deployment

Production-level logging and structure

SenseX helped me develop end-to-end ML engineering skills.