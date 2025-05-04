
# RAG com LangChain, FAISS, OpenAI e Cohere

Este projeto implementa um sistema RAG (Retrieval-Augmented Generation) completo com:

- Chunking semântico
- Reranker com Cohere
- Embeddings com OpenAI
- Vetor DB com FAISS
- Simulação de banco de dados
- Perguntas abertas com CLI

## Como rodar

```bash
pip install -r requirements.txt
cp .env.example .env  
python main.py
```

## Estrutura

```
main.py
utils/db_loader.py
.env.example
README.md
requirements.txt
```
