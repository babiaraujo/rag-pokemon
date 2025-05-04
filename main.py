import os
from dotenv import load_dotenv
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.retrievers.document_compressors import CohereReranker
from langchain.retrievers import ContextualCompressionRetriever
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from utils.db_loader import load_documents_from_database

load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")
cohere_key = os.getenv("COHERE_API_KEY")

if not openai_key or not cohere_key:
    raise EnvironmentError("Missing OPENAI_API_KEY or COHERE_API_KEY in .env")

documents = load_documents_from_database()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=600,
    chunk_overlap=100,
    separators=["\n\n", "\n", ".", " ", ""]
)
chunks = splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()
vector_store = FAISS.from_documents(chunks, embeddings)

retriever = vector_store.as_retriever(search_kwargs={"k": 10})
reranker = CohereReranker(cohere_api_key=cohere_key, top_n=5)
compressed_retriever = ContextualCompressionRetriever(
    base_compressor=reranker,
    base_retriever=retriever
)

llm = OpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0,
    streaming=True,
    callbacks=[StreamingStdOutCallbackHandler()]
)

qa_chain = RetrievalQAWithSourcesChain.from_chain_type(
    llm=llm,
    retriever=compressed_retriever,
    return_source_documents=True
)

while True:
    question = input("\nDigite sua pergunta (ou 'sair' para encerrar): ").strip().lower()
    if question in {"sair", "exit", "quit"}:
        break
    result = qa_chain({"question": question})
    print("\n>>> Resposta:\n", result["answer"])
    print("\n>>> Fontes:\n", result["sources"])
