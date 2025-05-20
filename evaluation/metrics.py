import json
from langchain_openai import ChatOpenAI
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import faithfulness, context_precision, answer_relevancy

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def load_dataset(path):
    with open(path, "r", encoding="utf-8") as f:
        data = [json.loads(line) for line in f]
    return Dataset.from_list(data)

def main():
    print("🔍 Loading data...")
    dataset = load_dataset("evaluation/rag_samples.jsonl")

    print("📊 Evaluating RAG quality with RAGAS...")
    results = evaluate(
        dataset=dataset,
        metrics=[faithfulness, answer_relevancy],
        llm=llm
    )

    print("\n🧠 RAG Evaluation Results:")
    print(results.to_pandas())

if __name__ == "__main__":
    main()
