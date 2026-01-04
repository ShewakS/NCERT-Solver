from typing import List
import requests
from backend.rag.prompts import RAG_PROMPT_TEMPLATE
from backend.config import OLLAMA_API_URL, OLLAMA_MODEL

class LLMGenerator:
    def __init__(self):
        """Generator using Ollama with llama2 model."""
        self.api_url = f"{OLLAMA_API_URL}/api/generate"
        self.model = OLLAMA_MODEL
        
        # Check if Ollama is running
        try:
            response = requests.get(f"{OLLAMA_API_URL}/api/tags", timeout=5)
            if response.status_code == 200:
                print(f"✓ Ollama connected successfully")
                print(f"✓ Using model: {self.model}")
            else:
                print(f"⚠ Ollama API responded with status {response.status_code}")
        except Exception as e:
            print(f"⚠ WARNING: Cannot connect to Ollama at {OLLAMA_API_URL}")
            print(f"  Error: {e}")

    def generate(self, question: str, docs: List, language: str) -> str:
        """Generate answer from retrieved documents using Ollama."""
        
        if not docs:
            return "I don't know - I couldn't find relevant information in the NCERT textbook for your question."

        # Prepare context from retrieved PDF chunks
        context_parts = []
        for i, doc in enumerate(docs):
            meta = doc.meta or {}
            source = f"[{meta.get('source_pdf', 'Unknown')} - Page {meta.get('page', '?')}]"
            context_parts.append(f"{doc.text}")
        
        context_str = "\n\n".join(context_parts[:5])  # Limit to top 5 chunks to avoid token limit
        
        # Create prompt
        prompt = RAG_PROMPT_TEMPLATE.format(context=context_str, question=question)

        try:
            print(f"[OLLAMA] Generating answer for: {question[:50]}...", flush=True)
            
            # Call Ollama API with proper format
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.4,
                    "num_predict": 512,
                    "top_p": 0.9,
                    "top_k": 40,
                    "stop": ["</s>", "<|user|>", "<|assistant|>", "<|system|>"]
                }
            }
            
            response = requests.post(
                self.api_url,
                json=payload,
                timeout=120
            )
            
            print(f"[OLLAMA] Response status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                answer = result.get("response", "").strip()
                
                print(f"[OLLAMA] Generated answer length: {len(answer)} chars")
                
                if not answer or len(answer) < 5:
                    return "I don't know - this topic is not covered in the NCERT textbook."
                
                return answer
            else:
                error_detail = ""
                try:
                    error_data = response.json()
                    error_detail = error_data.get("error", "")
                except:
                    error_detail = response.text[:200]
                
                print(f"[OLLAMA ERROR] Status {response.status_code}: {error_detail}")
                return f"Error: Could not generate answer. Please make sure Ollama is running and llama2 model is available. Try: ollama run llama2"
                
        except requests.exceptions.Timeout:
            print("[OLLAMA ERROR] Request timed out")
            return "Error: Response generation timed out. The model is taking too long to respond."
        except requests.exceptions.ConnectionError:
            print("[OLLAMA ERROR] Connection failed")
            return "Error: Cannot connect to Ollama. Make sure Ollama is running (run: ollama serve)"
        except Exception as e:
            print(f"[OLLAMA ERROR] Unexpected error: {str(e)}")
            return f"Error: {str(e)}"

if __name__ == "__main__":
    print("Testing Ollama generator with llama2...")
    gen = LLMGenerator()
    
    from collections import namedtuple
    Doc = namedtuple("Doc", ["text", "score", "meta"])
    docs = [
        Doc(text="Photosynthesis is the process by which plants make their own food using sunlight, water, and carbon dioxide.", 
            score=0.9, 
            meta={"source_pdf": "Science Chapter 2", "page": 15})
    ]
    
    q = "What is photosynthesis?"
    print(f"Q: {q}")
    print(f"A: {gen.generate(q, docs, 'en')}")
