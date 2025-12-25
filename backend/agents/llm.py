from transformers import pipeline
from langchain_huggingface import HuggingFacePipeline

pipe = pipeline(
    "text2text-generation",
    # model="google/flan-t5-base",
    model="google/flan-t5-large",
    max_length=2048,
)

llm = HuggingFacePipeline(pipeline=pipe)
