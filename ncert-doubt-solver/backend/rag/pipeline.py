from typing import Optional, List

from backend.rag.retriever import VectorRetriever
from backend.rag.generator import LLMGenerator
from backend.utils.language_detect import detect_language

class RAGPipeline:
    def __init__(self):
        self.retriever = VectorRetriever()
        self.generator = LLMGenerator()

    def answer(self, question: str, class_no: int, language: Optional[str] = None, history: Optional[List[dict]] = None):
        lang = language or detect_language(question)
        
        # If history exists, we should ideally contextualize the question.
        # For this scaffold, we will simple append the last turn if it exists, or just pass it through.
        # A better approach (OPEA style) is a standalone "Contextualize" step using LLM.
        # Let's do a simple concatenation for now to keep it fast on CPU:
        final_query = question
        if history and len(history) > 0:
            last_msg = history[-1]
            if last_msg.get('role') == 'assistant':
                # very naive contextualization: "Context: <prev_answer>. Question: <new_question>"
                # logic: help retrieval if pronouns are used.
                final_query = f"{last_msg.get('content')} {question}"
        
        docs = self.retriever.retrieve(final_query, class_no=class_no, language=lang)
        answer = self.generator.generate(question=question, docs=docs, language=lang)
        return {"answer": answer, "retrieved": [d.meta for d in docs]}
