import json
import os
import uuid
from datetime import datetime, timezone

import boto3
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr

app = FastAPI(title="portfolio-backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

S3_BUCKET = os.environ.get("S3_BUCKET", "")

PROFILE = {
    "name": "Anas Nadaf",
    "title": "AI & ML Engineer",
    "summary": "AI and ML engineer building AI pipelines and ML solutions.",
    "email": "anaswillreply@gmail.com",
}

TECHNOLOGIES = [
    {"name": "Python", "slug": "python"},
    {"name": "Go", "slug": "go"},
    {"name": "FastAPI", "slug": "fastapi"},
    {"name": "React", "slug": "react"},
    {"name": "PostgreSQL", "slug": "postgresql"},
    {"name": "SQLite", "slug": "sqlite"},
    {"name": "Apache Kafka", "slug": "apachekafka"},
    {"name": "OpenSearch", "slug": "opensearch"},
    {"name": "Elasticsearch", "slug": "elasticsearch"},
    {"name": "DuckDB", "slug": "duckdb"},
    {"name": "PyTorch", "slug": "pytorch"},
    {"name": "Hugging Face", "slug": "huggingface"},
    {"name": "scikit-learn", "slug": "scikitlearn"},
    {"name": "Pandas", "slug": "pandas"},
    {"name": "NumPy", "slug": "numpy"},
    {"name": "Ray", "slug": "ray"},
    {"name": "MLflow", "slug": "mlflow"},
    {"name": "DVC", "slug": "dvc"},
    {"name": "Streamlit", "slug": "streamlit"},
    {"name": "Plotly", "slug": "plotly"},
    {"name": "Prometheus", "slug": "prometheus"},
    {"name": "Docker", "slug": "docker"},
    {"name": "Kubernetes", "slug": "kubernetes"},
    {"name": "WebAssembly", "slug": "webassembly"},
]


class ContactMessage(BaseModel):
    name: str
    email: EmailStr
    message: str


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/profile")
def profile():
    return PROFILE


@app.get("/api/technologies")
def technologies():
    return [
        {"name": t["name"], "logo": f"https://cdn.simpleicons.org/{t['slug']}"}
        for t in TECHNOLOGIES
    ]


@app.post("/api/contact")
def contact(msg: ContactMessage):
    if not S3_BUCKET:
        raise HTTPException(status_code=503, detail="storage not configured")
    key = f"contact/{datetime.now(timezone.utc):%Y%m%d}/{uuid.uuid4()}.json"
    body = msg.model_dump()
    body["received_at"] = datetime.now(timezone.utc).isoformat()
    boto3.client("s3").put_object(
        Bucket=S3_BUCKET,
        Key=key,
        Body=json.dumps(body).encode(),
        ContentType="application/json",
    )
    return {"status": "received"}
