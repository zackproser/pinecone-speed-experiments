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

## Integration with `pyenv`

![pyenv](https://github.com/pyenv/pyenv) is a tool that allows you to quickly install and switch between multiple versions of python locally, which is very useful. 

Unfortunately, using pyenv successfully with the virtualenv workflow described here involves some more setup: 

1. Install `pyenv-virtualenv` (a plugin to manage virtual environments for `pyenv`) by cloning it from GitHub: 

```bash
git clone https://github.com/pyenv/pyenv-virtualenv.git $(pyenv root)/plugins/pyenv-virtualenv
```

1. Add initialization to your shell. The correct file to edit will vary depending on your preferred shell. I use ZSH, so I edit `~/.zshrc`: 
```bash
# Add this to your .bashrc, .bash_profile, or .zshrc:
# If you already use pyenv and have the following snippet in place: 
# 
# if command -v pyenv 1>/dev/null 2>&1; then
#  eval "$(pyenv init -)"
# fi
#
# then you can add the following within the same if statement, like so: 
#
# if command -v pyenv 1>/dev/null 2>&1; then
#  eval "$(pyenv init -)"
#  eval "$(pyenv virtualenv-init -)"
# fi
#
# Otherwise, ensure this line is present in your preferred shell's configuration file:
eval "$(pyenv virtualenv-init -)"
```

Be sure to reload your shell with `exec "$SHELL"`

1. Create a virtual environment using the specific Python version you want: 
```python
pyenv virtualenv 3.8.1 myenv
```

1. Activate the virtual environment 

```bash
pyenv activate myenv
```

1. Deactivate when you're done

```bash
pyenv deactivate
```

## Use the `pyenv local` command to set a specific virtualenv to be active in a given directory

```bash
pyenv local myenv
```

This will create a `.python-version` file in that directory, and anytime you `cd` into this directory, 
the specified virtual environment will be automatically activated. 

## Finding and modifying virtualenv code with pyenv and the virtualenv plugin

To find where pyenv installed your virtualenv, you can run: 
```bash
pyenv prefix myenv
```

This gives you to the path the to virtual environment names `myenv`. 

Next, navigate to the directory returned by `pyenv prefix myenv` and you'll find the Python installation
for that virtual environment. To find and modify library code, you can navigate to the `site-packages` directory 
where the installed packages reside: 

```bash
# (Replace 3.8 with the exact version of Python you specified for your virtualenv if it's different)

cd $(pyenv prefix myenv)/lib/python3.8/site-packages
```

Here, you'll find the latest code for all the installed packages, and you can edit them as needed to test out 
your changes. Changes made to the library code here will only affect your currently activated Python virtual 
environment. 

## Running your test script against the modified library code in your virtualenv

In your test directory, with your `pyenv-virtualenv` plugin installed and your
virtualenv created and activated as described above, you can now run 

`python -m pinecone-speed-test.py`, for example, in order to perform profiling and 
arbitrary tests against modified library code. 

## Test documents

There are files of various sizes in `./test-documents/` that may be useful for running various 
Pinecone and langhchain operations against.
