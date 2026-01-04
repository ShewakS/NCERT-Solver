from backend.rag.pipeline import RAGPipeline

p = RAGPipeline()

examples = [
    {"class_no": 5, "question": "What are the parts of a plant?", "language": "en"},
    {"class_no": 5, "question": "पौधे के भाग कौन-कौन से हैं?", "language": "hi"},
]

for ex in examples:
    print('-' * 80)
    print(f"Q ({ex['language']}): {ex['question']}")
    res = p.answer(question=ex['question'], class_no=ex['class_no'], language=ex['language'])
    print('Answer:')
    print(res['answer'])
    print('\nRetrieved chunks metadata:')
    for m in res['retrieved']:
        print(m)
    print('\n')
