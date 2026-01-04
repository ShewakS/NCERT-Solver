from transformers import pipeline
import torch
import sys

def test_load():
    print(f"Python: {sys.version}")
    print(f"Torch: {torch.__version__}")
    
    model_name = "MBZUAI/LaMini-Flan-T5-783M"
    print(f"Attempting to load {model_name}...")
    
    try:
        # Try without device_map first to isolate accelerate issues
        pipe = pipeline("text2text-generation", model=model_name)
        print("Success without device_map!")
    except Exception as e:
        print(f"Failed without device_map: {e}")
        
    try:
        print("Attempting with device_map='auto'...")
        pipe = pipeline("text2text-generation", model=model_name, device_map="auto")
        print("Success with device_map='auto'!")
    except Exception as e:
        print(f"Failed with device_map='auto': {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_load()
