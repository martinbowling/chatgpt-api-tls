# ChatGPT api

* It is an unoffical api for development purpose only.


# How to install

* Make sure that python and virual environment is installed.

* Create a new virtual environment

```python
# one time
virtualenv -p $(which python3) pyenv

# everytime you want to run the server
source pyenv/bin/activate
```

* Now install the requirements

```
pip install -r requirements.txt
```



* Now run the server

```
python server.py
```

* The server runs at port `31337`. If you want to change, you can change it in server.py


# Api Documentation

* There is a single end point only. It is available at `/chat`

```sh
curl -XGET http://localhost:31337/chat?q=Write%20a%20python%20program%20to%20reverse%20a%20list
```

# Credit

* Original FauxAPI was inspired by [Daniel Gross's whatsapp gpt](https://github.com/danielgross/whatsapp-gpt) 
* [OpenAI](https://openai.com/) for creating the ChatGPT API
* [FlorianREGAZ](https://github.com/FlorianREGAZ) for the TLS Client
* [rawandahmad698](https://github.com/rawandahmad698/PyChatGPT) for original CLI TLS ChatGPT Client
