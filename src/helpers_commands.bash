conda activate mini-rag

export PS1="\[\033[01;32m\]\u@\h:\w\n\[\033[00m\]\$ "

pip install -r requirements.txt

uvicorn main:app --reload

