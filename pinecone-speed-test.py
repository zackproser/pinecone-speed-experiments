
import pinecone
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
import os
import getpass
from langchain.vectorstores import Pinecone

loader = TextLoader("./test-documents/state_of_the_union.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()

# Use the Pinecone environment variables, if set - otherwise, securely prompt the user for them
if "PINECONE_API_KEY" in os.environ:
    pass
else:
    os.environ['PINECONE_API_KEY'] = getpass.getpass(
        'Please enter your PINECONE_API_KEY:')

if "PINECONE_ENVIRONMENT" in os.environ:
    pass
else:
    os.environ['PINECONE_ENVIRONMENT'] = getpass.getpass(
        'Please enter your PINECONE_ENVIRONMENT:')

# initialize pinecone
pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),  # find at app.pinecone.io
    environment=os.getenv("PINECONE_ENV"),  # next to api key in console
)

index_name = "langchain-demo"

# First, check if our index already exists. If it doesn't, we create it
if index_name not in pinecone.list_indexes():
    # we create a new index
    pinecone.create_index(
        name=index_name,
        metric='cosine',
        dimension=1536
    )
# The OpenAI embedding model `text-embedding-ada-002 uses 1536 dimensions`
docsearch = Pinecone.from_documents(docs, embeddings, index_name=index_name)

query = "What did the president say about Ketanji Brown Jackson"
docs = docsearch.similarity_search(query)

print(docs[0].page_content)

index = pinecone.Index(index_name)
vectorstore = Pinecone(index, embeddings.embed_query, "text")

vectorstore.add_texts("More text!")

retriever = docsearch.as_retriever(search_type="mmr")
matched_docs = retriever.get_relevant_documents(query)
for i, d in enumerate(matched_docs):
    print(f"\n## Document {i}\n")
    print(d.page_content)

found_docs = docsearch.max_marginal_relevance_search(query, k=2, fetch_k=10)
for i, doc in enumerate(found_docs):
    print(f"{i + 1}.", doc.page_content, "\n")
