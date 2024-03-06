# vaulthunter.py


> [!WARNING]
> This is a hacky weekend project, likely to go unmaintained. Should it evolve, it is likely to see major refactoring.
## Features

- **Embedding Generation**: Utilizes a Hugging Face access token to generate embeddings from your Obsidian vault, using the [`sentence-transformers/all-mpnet-base-v2`](https://huggingface.co/sentence-transformers/all-mpnet-base-v2) model.
- **Local Storage in Chroma DB**: Stores the generated embeddings locally, ensuring quick and easy retrieval.
- **RAG with Mistral 7b Instruct**: Use the embeddings for Retrieval-Augmented Generation (RAG), providing responses based on your vault's content. It's like asking your notes a question and getting an answer, with references!
- **Electron Frontend**: A simple, prototype frontend for interacting with *vaulthunter*. It's the window to your digital memory, no matter how it looks.

## Getting Started

### Prerequisites

- Python ~3.11+ (I'm not actually sure, don't quote me)
- Node.js for the Electron frontend (we promise it's not as scary as it looks)
- An Obsidian vault (obviously, where else would the treasure be?)

### Installation

Clone this repository:

```bash
git clone https://github.com/phasewalk1/vaulthunter.py
cd vaulthunter.py
```

Activate the pipenv environment:

```bash
pipenv shell
```

Create a `Pipfile.lock`
```bash
pipenv install --ignore-pipfile
```

Sync dependencies
```bash
pipenv sync
```

### Usage
One last thing before we're ready to go, you'll need a Hugging Face access token, see [here](https://huggingface.co/docs/hub/security-tokens) for instructions on getting one if needed. Once
you have it, put it in a `.env` file in the root, like so:
```.env
HUGGINGFACE_ACCESS_TOKEN="z1000"
```

Now you can start hunting treasures in your vault!:

```bash
python vaulthunter.py --vault <path-to-your-vault>
```

And let the magic unfold. Your personal AI companion is now ready to dive into your vault and fetch the pearls of wisdom you've accumulated.
