import json
import psycopg2
from pgvector.psycopg2 import register_vector
import ollama

DB_CONFIG = {
    "host": "localhost",
    "port": 5433,
    "dbname": "support",
    "user": "support",
    "password": "support",
}

EMBEDDING_MODEL = "nomic-embed-text"


def get_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    return conn


def setup_database():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    conn.commit()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS knowledge_base (
            id SERIAL PRIMARY KEY,
            content TEXT NOT NULL,
            embedding vector(768),
            metadata JSONB
        );
    """)
    conn.commit()
    cur.close()
    conn.close()


def get_vector_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    register_vector(conn)
    return conn


def embed(text: str) -> list[float]:
    response = ollama.embed(model=EMBEDDING_MODEL, input=text)
    return response.embeddings[0]


def ingest(content: str, metadata: dict = {}) -> None:
    embedding = embed(content)
    conn = get_vector_connection()
    cur = conn.cursor()

def retrieve(query: str, top_k: int = 3) -> list[dict]:
    query_embedding = embed(query)
    conn = get_vector_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, content, metadata,
               1 - (embedding <=> %s::vector) AS similarity
        FROM knowledge_base
        ORDER BY embedding <=> %s::vector
        LIMIT %s;
        """,
        (query_embedding, query_embedding, top_k)
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        {
            "id": row[0],
            "content": row[1],
            "metadata": row[2],
            "similarity": round(float(row[3]), 4)
        }
        for row in rows
    ]