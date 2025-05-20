import json
from langchain_openai import ChatOpenAI
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import faithfulness, context_precision, answer_relevancy

llm = ChatOpenAI(model="gpt-4o", temperature=0)

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
        metrics=[faithfulness, answer_relevancy, context_precision],
        llm=llm
    )

    df = results.to_pandas()
    print("\n🔬 Evaluation Metrics:")
    for metric, value in df.iloc[0].items():
        print(f"{metric}: {value}")


if __name__ == "__main__":
    main()
