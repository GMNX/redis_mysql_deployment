FROM python:3.8

RUN python -m pip install typer redis mysql-connector-python

RUN mkdir /myapp
WORKDIR /myapp

COPY ./program.py program.py

ENTRYPOINT ["tail"]
CMD ["-f","/dev/null"]