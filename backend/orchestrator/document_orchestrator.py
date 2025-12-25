from agents.ingestion_agent import IngestionAgent
from agents.indexing_agent import IndexingAgent
from agents.qa_agent import QAAgent

class DocumentOrchestrator:

    def upload_and_process(self, document):
        chunks = IngestionAgent().process(document.file.path)
        IndexingAgent().index(chunks)

    def ask(self, question):
        return QAAgent().answer(question)
