from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Document
from orchestrator.document_orchestrator import DocumentOrchestrator
from agents.vector_store import get_vector_store

class DocumentUploadView(APIView):

    def post(self, request):
        file = request.FILES['file']
        document = Document.objects.create(file=file)

        orchestrator = DocumentOrchestrator()
        orchestrator.upload_and_process(document)

        return Response({"message": "Document processed successfully"})

class AskQuestionView(APIView):

    def post(self, request):
        question = request.data.get("question")

        orchestrator = DocumentOrchestrator()
        answer = orchestrator.ask(question)

        return Response({"answer": answer})

class ReadStoreView(APIView):

    def get(self, request):
        try:
            store = get_vector_store()
            
            # Get the index information
            total_vectors = store.index.ntotal
            
            # Get documents from the store
            documents = store.docstore._dict if hasattr(store, 'docstore') else {}
            
            return Response({
                "status": "success",
                "total_vectors": total_vectors,
                "document_count": len(documents),
                "documents": [
                    {"id": doc_id, "content": doc.page_content[:200]}  # First 200 chars
                    for doc_id, doc in documents.items()
                ],
                "vector_store_path": "vector_store"
            })
        except Exception as e:
            return Response({
                "status": "error",
                "message": str(e)
            }, status=500)