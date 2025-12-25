from langchain_core.output_parsers import StrOutputParser
from .vector_store import get_vector_store
from .llm import llm
from .prompts import qa_prompt

class QAAgent:

    def answer(self, question):
        store = get_vector_store()
        retriever = store.as_retriever(search_kwargs={"k": 5})

        docs = retriever.invoke(question)
        context = "\n\n".join(doc.page_content for doc in docs)

        chain = qa_prompt | llm | StrOutputParser()

        return chain.invoke({
            "context": context,
            "question": question
        })
