# vaulthunter.py

**vaulthunter** transforms your [Obsidian](https://obsidian.md) vault into a dynamic knowledge base, accessible through an innovative AI interface. Leveraging modern embedding technologies and open source LLMs like [`Mistral-7B-Instruct-v0.2`](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2), this tool enables personalized and context-aware interactions with your digital notes. It's designed for those who seek to enhance their productivity and knowledge retrieval processes by integrating cutting-edge AI capabilities directly with their personal database.

## Overview

The code in this repository is a prototype that aims to marry your Obsidian vault's knowledge with the power of AI. It generates embeddings from your Obsidian notes, stores them locally, and utilizes them to augment RAG-generated responses from `Mistral`. Think of it as having a chat with your digital brain, where it can reference back to "When did I apply for the internship at Nvidia?" and give you the exact date, citing the `Job Search.md` note as its source. 

This concoction is served with an (admittedly) ugly, prototype Electron frontend for the chat interface. But hey, it's the brains we're after here, not the looks, right?

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

## Contributions

This is a very simple demo and, should it evolve, will likely go through major refactors. However, contributions in the form of thoughts, requests, bug reports, or code are more than welcome! Let's build the ultimate knowledge companion together.

## License

**vaulthunter** is open-sourced under the MIT license. Feel free to fork, modify, and use it in your projects.
