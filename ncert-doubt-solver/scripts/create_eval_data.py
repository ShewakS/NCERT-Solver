import random
import json
from pathlib import Path
from backend.ingestion.chunker import chunk_text

def generate_eval_data(output_file: str = "data/eval_set.jsonl"):
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # In a real scenario, we would iterate over all vectors/chunks in the DB.
    # Here, we will simulate by reading a sample text if available, or just creating dummy data for demonstration.
    
    print("Generating synthetic evaluation data...")
    
    # Example patterns to generate questions
    templates = [
        ("What is {topic}?", "Direct"),
        ("Explain the concept of {topic}.", "Direct"),
        ("How does {topic} relate to other concepts?", "Logical"),
    ]
    
    # Topics extracted from a hypothetical Class 5 Science book
    topics = ["force", "energy", "photosynthesis", "gravity", "magnetism", "friction"]
    
    with open(output_path, "w", encoding="utf-8") as f:
        for topic in topics:
            # Generate 2 questions per topic
            for _ in range(2):
                tmpl, q_type = random.choice(templates)
                question = tmpl.format(topic=topic)
                
                entry = {
                    "question": question,
                    "ground_truth_keywords": [topic], # Simple keyword check
                    "type": q_type,
                    "class_no": 5
                }
                f.write(json.dumps(entry) + "\n")
                
    print(f"Generated {len(topics)*2} questions in {output_file}")

if __name__ == "__main__":
    generate_eval_data()
