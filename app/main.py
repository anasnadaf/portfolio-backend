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
    "title": "ML & Backend Engineer",
    "summary": (
        "I build ML pipelines and backend systems: counterparty extraction, "
        "transaction categorisation with LLMs, Ray-based inference services, "
        "and evaluation tooling."
    ),
    "email": "anaswillreply@gmail.com",
}

TECHNOLOGIES = [
    {"name": "Python", "slug": "python"},
    {"name": "Go", "slug": "go"},
    {"name": "FastAPI", "slug": "fastapi"},
    {"name": "React", "slug": "react"},
    {"name": "PostgreSQL", "slug": "postgresql"},
    {"name": "Apache Kafka", "slug": "apachekafka"},
    {"name": "OpenSearch", "slug": "opensearch"},
    {"name": "Elasticsearch", "slug": "elasticsearch"},
    {"name": "DuckDB", "slug": "duckdb"},
    {"name": "PyTorch", "slug": "pytorch"},
    {"name": "Hugging Face", "slug": "huggingface"},
    {"name": "scikit-learn", "slug": "scikitlearn"},
    {"name": "Ray", "slug": "ray"},
    {"name": "Prometheus", "slug": "prometheus"},
    {"name": "Docker", "slug": "docker"},
    {"name": "DVC", "slug": "dvc"},
    {"name": "Plotly", "slug": "plotly"},
    {"name": "OpenAI", "slug": "openai"},
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
