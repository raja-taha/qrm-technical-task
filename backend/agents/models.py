from sentence_transformers import SentenceTransformer
from transformers import pipeline

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

qa_pipeline = pipeline(
    "text2text-generation",
    model="google/flan-t5-base"
)