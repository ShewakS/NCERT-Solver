import requests
import time
import json

def demo():
    url = "http://localhost:8000/api/chat/"
    print("Waiting for server to be ready...")
    
    # Poll server
    for i in range(300): # Wait up to 5 minutes for model download
        try:
            r = requests.get("http://localhost:8000/")
            if r.status_code == 200:
                print("Server is up!")
                break
        except:
            time.sleep(1)
            print(".", end="", flush=True)
    else:
        print("\nServer failed to start in time.")
        return

    # Question 1: Direct
    q1 = {
        "class_no": 5,
        "question": "What is the shape of the Earth?",
        "history": []
    }
    print(f"\n[User]: {q1['question']}")
    try:
        res = requests.post(url, json=q1).json()
        print(f"[Bot]: {res['answer']}")
        
        # Question 2: Logical/Conversational
        q2_text = "Does it have corners?"
        # history from prev
        history = [
            {"role": "user", "content": q1['question']},
            {"role": "assistant", "content": res['answer']}
        ]
        q2 = {
            "class_no": 5,
            "question": q2_text,
            "history": history
        }
        print(f"\n[User]: {q2_text}")
        res2 = requests.post(url, json=q2).json()
        print(f"[Bot]: {res2['answer']}")
        
    except Exception as e:
        print(f"Error querying server: {e}")

if __name__ == "__main__":
    demo()
