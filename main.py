
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
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

if not OPENAI_API_KEY or not COHERE_API_KEY:
    raise ValueError("API keys missing in .env")

raw_docs = load_documents_from_database()
splitter = RecursiveCharacterTextSplitter(
    chunk_size=600,
    chunk_overlap=100,
    separators=["\n\n", "\n", ".", " ", ""]
)
docs = splitter.split_documents(raw_docs)

embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(docs, embeddings)

reranker = CohereReranker(cohere_api_key=COHERE_API_KEY, top_n=5)
base_retriever = vectorstore.as_retriever(search_kwargs={"k": 10})
compression_retriever = ContextualCompressionRetriever(
    base_compressor=reranker,
    base_retriever=base_retriever
)

llm = OpenAI(
    temperature=0,
    model_name="gpt-3.5-turbo",
    streaming=True,
    callbacks=[StreamingStdOutCallbackHandler()]
)

qa_chain = RetrievalQAWithSourcesChain.from_chain_type(
    llm=llm,
    retriever=compression_retriever,
    return_source_documents=True
)

while True:
    query = input("\ndigite sua pergunta (ou 'sair' para encerrar): ")
    if query.strip().lower() in ["sair", "exit", "quit"]:
        break
    result = qa_chain({"question": query})
    print("\n>>> resposta:")
    print(result["answer"])
    print("\n>>> fontes:")
    print(result["sources"])
