# Email bot

## How to install
1. `virtualenv -p python3 venv`
2. `. ./venv/bin/activate`
3. `pip install -r requirements.txt`
4. `sudo chmod -R 777 .`

## How to train
`python -m email_bot build `

## How to run
1. `sudo docker run -ti -d -p 0.0.0.0:9200:9200 -p 0.0.0.0:7151:7151 -p 0.0.0.0:9300:9300 mindmeldworkbench/dep:es_7 `
2. `sudo docker run -it -d -p 5000:5000 chaliy/wiki-lang-detect:latest`
3. `mindmeld num-parse`
4. `python ./run_server.py` or `./run_editor.py` or `./run_api.py`
