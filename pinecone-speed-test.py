
from langchain.vectorstores import Pinecone
import getpass
import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import TextLoader
import pinecone
from pyinstrument import Profiler
profiler = Profiler()
profiler.start()

test_filename_to_load = "larger_test_file.txt"
# test_filename_to_load = "state_of_the_union.txt"

loader = TextLoader(f"./test-documents/{test_filename_to_load}")
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

profiler.stop()
print(profiler.output_text(unicode=True, color=True))
