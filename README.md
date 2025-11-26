Mobile assistant 👽
----

Personal assistant. Small personal helper to find info in the internet and do some planning.

### Features:
  - support Openrouter/Gigachat/Ollama models
  - voice dialog
  - Answer questions based on websearch
  - simple planning tools

### Install:
1) git clone https://github.com/serser152/mob_friend
2) Create .env like .env.example. Fill the values
3) (optional) Enable https 
```
mv .streamlit/config.toml.example .streamlit/config.toml
cd keys
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -sha256 -days 365
```
remember password!
4) Run on linux:

```
python -m venv venv
source venv/bin/activate
pip install -r requirements
./run.sh
```
enter password for https
the following will be displayed 

```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.16:8501
```


