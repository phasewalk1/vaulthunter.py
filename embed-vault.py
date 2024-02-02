import os
import torch.nn.functional as F
from torch import Tensor
import torch
import numpy as np
from sklearn.manifold import TSNE
from transformers import AutoTokenizer, AutoModel


def read_vault(vault_path):
    texts = []
    print("Reading files from vault: ", vault_path)
    for root, dirs, files in os.walk(vault_path):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as md_file:
                    texts.append(md_file.read())

    print(f"Read {len(texts)} files")
    return texts


def average_pool(last_hidden_states: Tensor, attention_mask: Tensor) -> Tensor:
    last_hidden = last_hidden_states.masked_fill(~attention_mask[..., None].bool(), 0.0)
    return last_hidden.sum(dim=1) / attention_mask.sum(dim=1)[..., None]


def batch_embed(texts, batch_size=10, device="cpu"):
    print("Loading tokenizer and model...")
    if torch.cuda.is_available():
        print("Using GPU")
        device = "cuda"
    else:
        print("Using CPU")
    tokenizer = AutoTokenizer.from_pretrained("Supabase/gte-small")
    model = AutoModel.from_pretrained("Supabase/gte-small").to(device)

    all_embeddings = []

    for i in range(0, len(texts), batch_size):
        batch_texts = texts[i : i + batch_size]
        batch_dict = tokenizer(
            batch_texts,
            max_length=512,
            padding=True,
            truncation=True,
            return_tensors="pt",
        ).to(device)

        with torch.no_grad():
            outputs = model(**batch_dict)
        batch_embeddings = average_pool(
            outputs.last_hidden_state, batch_dict["attention_mask"]
        )
        batch_embeddings = F.normalize(batch_embeddings, p=2, dim=1)

        all_embeddings.append(batch_embeddings.cpu())

    all_embeddings = torch.cat(all_embeddings, dim=0)

    return all_embeddings


def export_embeddings(embeddings, file_path):
    if file_path.endswith(".npy"):
        np.save(file_path, embeddings.numpy())
    else:
        torch.save(embeddings, file_path)


def main():
    ## vault_path = os.path.expanduser("~/<your-vault-path>")
    texts = read_vault(vault_path)
    embeddings = batch_embed(texts)
    export_embeddings(embeddings, "embeddings.pt")
    print("Embeddings saved to embeddings.pt")


if __name__ == "__main__":
    main()
