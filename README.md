# Overview
This is a work-in-progress [WIP] test repository for profiling the Pinecone Python client. 

It is derived from [this LangChain example / Jupyter notebook](https://github.com/langchain-ai/langchain/blob/master/docs/extras/integrations/vectorstores/pinecone.ipynb)

It installs `pyinstrument` in addition to the requirements for the notebook itself. It uses virtualenv to allow the user to modify library code locally, which is
useful for chasing down slow codepaths and testing out fixes.

# Usage 

## Set up virtualenv 

In order to be able to modify libraries like `langchain` and the Pinecone client, it's necessary to set up a virtualenv:

```bash
# Install virtualenv 
pip install virtualenv

# Create a new virtualenv for Python 3.8
virtualenv -p python3.8 myenv

# Activate the virtualenv
source myenv/bin/activate

# Now, you can install the requirements, but they'll be available in 
# `myenv/lib/python/3.8/site-packages/<package-name>/`
pip3 install -r requirements.txt
```

## Export env vars in your shell 

If you don't have them set, the script will prompt you for them. 

## IMPORTANT - you must run your test scripts in `module` mode 

Note the `-m`
```bash
python -m pinecone-speed-test.py
```

## Profiling code
`pyinstrument pinecone-speed-test.py`

## Test documents

There are files of various sizes in `./test-documents/`
