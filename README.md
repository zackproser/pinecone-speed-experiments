# Overview
This is a test repository for profiling the Pinecone Python client. 

It is derived from [this LangChain example / Jupyter notebook](https://github.com/langchain-ai/langchain/blob/master/docs/extras/integrations/vectorstores/pinecone.ipynb)

It installs `pyinstrument` in addition to the requirements for the notebook itself. 

# Usage 

`pip install -r requirements`

Depending on your setup, you may need to `pip3 install -r requirements`.

`pyinstrument pinecone.py`

# Test documents

There are files of various sizes in 
