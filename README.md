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

There are challenges with running `pyinstrument` directly against a test script when you also want your test script to load packages / libraries from your virtualenv. 

Findings: 

1. Name your overall repo checkout directory the same as your test script: `pinecone-speed-test`, in this case. 
2. Ensure that directory has a `__init__.py` file in it, which signals that it is a package
3. Add the pyinstrument code to your actual test script, like so: 

```python
# At the top of your test script: 
from pyinstrument import Profiler
profiler = Profiler()
profiler.start()
 
# Perform whatever jobs or processing is necessary or that you're trying to profile
# <code to profile>


# At the end of your test script, have the pyinstrument profiler print out its findings: 
profiler.stop()
print(profiler.output_text(unicode=True, color=True))
```

You can then run your test script like so: 

```bash
pyhon -m pinecone-speed-test
```

When your test script is finished running you should get output similar to this: 

```bash
  _     ._   __/__   _ _  _  _ _/_   Recorded: 10:02:50  Samples:  1927
 /_//_/// /_\ / //_// / //_'/ //     Duration: 25.185    CPU time: 2.651
/   _/                      v4.5.1

Program: /home/zachary/Pinecone/pinecone-speed-test/pinecone-speed-test.py

25.184 <module>  pinecone-speed-test.py:2
├─ 21.623 Pinecone.from_documents  langchain/vectorstores/base.py:410
│     [108 frames hidden]  langchain, pinecone, urllib3, http, s...
│        8.791 _SSLSocket.read  <built-in>
│        6.136 _SSLSocket.read  <built-in>
├─ 2.070 list_indexes  pinecone/manage.py:182
│     [26 frames hidden]  pinecone, urllib3, http, socket, ssl,...
├─ 0.805 init  pinecone/config.py:235
│     [17 frames hidden]  pinecone, requests, urllib3
└─ 0.664 Pinecone.similarity_search  langchain/vectorstores/pinecone.py:148
      [47 frames hidden]  langchain, tenacity, openai, requests...
```

## Test documents

There are files of various sizes in `./test-documents/`
