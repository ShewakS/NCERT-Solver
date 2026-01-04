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
        class_name = f"Class {class_no}"
        RELEVANCE_THRESHOLD = 0.35  # Strict threshold for syllabus gating
        
        # If history exists, we should ideally contextualize the question.
        # ... logic as before ...
        final_query = question
        if history and len(history) > 0:
            last_msg = history[-1]
            if last_msg.get('role') == 'assistant':
                final_query = f"{last_msg.get('content')} {question}"
        
        docs = self.retriever.retrieve(final_query, class_no=class_no, language=lang)
        
        # Gating logic: Check if the best retrieved chunk matches the syllabus well enough
        if not docs or (docs[0].score < RELEVANCE_THRESHOLD):
            print(f"[GATING] Question likely out of syllabus (best score: {docs[0].score if docs else 'None'} < {RELEVANCE_THRESHOLD})")
            answer = f"I'm sorry, I couldn't find information about '{question}' in the {class_name} NCERT textbooks. I can only help with topics covered in the syllabus."
            return {"answer": answer, "retrieved": [d.meta for d in docs]}

        answer = self.generator.generate(question=question, docs=docs, language=lang, class_name=class_name)
        return {"answer": answer, "retrieved": [d.meta for d in docs]}
