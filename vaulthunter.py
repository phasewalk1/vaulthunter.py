import os
import sys
import markdown
import re
import torch
from sentence_transformers import SentenceTransformer, util


model = SentenceTransformer("all-MiniLm-L6-v2")


def parse_markdown_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()
    html = markdown.markdown(text)
    plaintext = re.sub(r"<.*?>", "", html)
    return plaintext


def generate_embeddings(model, vault_path):
    embeddings = {}
    print(f"Generating embeddings from vault: {vault_path}")
    for root, _, files in os.walk(vault_path):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                content = parse_markdown_file(file_path)
                embedding = model.encode(content, convert_to_tensor=True)
                embeddings[file_path.split(vault_path)[1]] = embedding
                print("Generated embeddings for", file)
            else:
                print("Skipping: ", file)
    print(f"Read {len(embeddings)} files")
    return embeddings


def export_embeddings(embeddings, output_path):
    print(f"Exporting embeddings to {output_path}")
    embeddings_to_save = {
        path: embedding.cpu().numpy() for path, embedding in embeddings.items()
    }
    torch.save(embeddings_to_save, output_path)


def load_embeddings(embeddings_path):
    print(f"Loading embeddings from {embeddings_path}")
    embeddings = torch.load(embeddings_path)
    embeddings = {
        path: torch.tensor(embedding) for path, embedding in embeddings.items()
    }


def query_to_embedding(query):
    return model.encode(query, convert_to_tensor=True)


def search_embeddings_by_similarity(query, embeddings, return_n=10):
    query_embedding = query_to_embedding(query)
    scores = {}
    for file_path, file_embedding in embeddings.items():
        similarity = util.pytorch_cos_sim(query_embedding, file_embedding)
        scores[file_path] = similarity.item()
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_scores[:return_n]


def interactive_similarity_search(embeddings):
    while True:
        query = input("Enter a query or 'exit' to quit: ")
        if query == "exit":
            break
        outputs = search_embeddings_by_similarity(query, embeddings)
        for file_path, score in outputs:
            print(f"{file_path}: {score:.2f}")


def main_embed():
    vault_path = os.path.expanduser("~/Documents/phasewalk1-master")
    embeddings = generate_embeddings(model, vault_path)
    return embeddings


def main():
    args = sys.argv[1:]
    embeddings = None

    if len(args) != 0 and args[0] == "gen":
        embeddings = main_embed()
    else:
        embeddings_path = input("Enter the path to the embeddings file: ")
        embeddings = load_embeddings(embeddings_path)

    interactive_similarity_search(embeddings)


if __name__ == "__main__":
    main()
