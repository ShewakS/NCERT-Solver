import json
import time
from pathlib import Path
from backend.rag.pipeline import RAGPipeline

def evaluate_system(eval_file: str = "data/eval_set.jsonl"):
    eval_path = Path(eval_file)
    if not eval_path.exists():
        print(f"Evaluation file {eval_file} not found. Run create_eval_data.py first.")
        return

    print("Initializing RAG Pipeline...")
    try:
        pipeline = RAGPipeline()
    except Exception as e:
        print(f"Failed to init pipeline: {e}")
        return

    print(f"Starting evaluation on {eval_file}...")
    
    total = 0
    correct = 0
    total_latency = 0
    
    results = []
    
    with open(eval_path, "r", encoding="utf-8") as f:
        for line in f:
            data = json.loads(line)
            q = data['question']
            keywords = data.get('ground_truth_keywords', [])
            class_no = data.get('class_no', 5)
            
            start = time.time()
            # Call pipeline
            try:
                res = pipeline.answer(q, class_no=class_no)
                ans = res['answer']
            except Exception as e:
                ans = f"Error: {e}"
            
            latency = time.time() - start
            total_latency += latency
            
            # Simple keyword matching for "accuracy"
            # In a real system, use an LLM-as-a-judge to verify textual entailment
            is_correct = any(k.lower() in ans.lower() for k in keywords)
            if is_correct:
                correct += 1
                
            total += 1
            print(f"[{'PASS' if is_correct else 'FAIL'}] ({latency:.2f}s) Q: {q}")
            
            results.append({
                "question": q,
                "answer": ans,
                "latency": latency,
                "correct": is_correct
            })
            
    if total == 0:
        print("No questions found.")
        return

    avg_latency = total_latency / total
    accuracy = (correct / total) * 100
    
    print("\nXXX Evaluation Results XXX")
    print(f"Total Questions: {total}")
    print(f"Accuracy: {accuracy:.2f}% (Target: >=85%)")
    print(f"Avg Latency: {avg_latency:.2f}s (Target: <=3-5s)")
    
    # Save detailed results
    with open("evaluation_report.json", "w") as f:
        json.dump({"accuracy": accuracy, "avg_latency": avg_latency, "details": results}, f, indent=2)
        print("Report saved to evaluation_report.json")

if __name__ == "__main__":
    evaluate_system()
