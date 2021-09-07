#Pytorch-Chatbot 


## to run with venv for development:

1 -. create venv if not done created
```bash
python3 -m venv /path/to/directory
```

2 -. activate venv
```bash
source /path/to/venv/bin/activate
```

3 -. install dependencies
```bash
pip3 install --no-cache-dir -r requirements.txt
```

4 -.
```bash
python3 -m nltk.downloader punkt
```

5 -. To install/reinstall the library locally, run python setup.py install in the project root directory.
```bash
python3 setup.py install
```

6 -. run the application

```bash
python3  src/demos/train.py
python3  src/demos/chat.py
```

