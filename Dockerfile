FROM python:3

RUN pip install requests
RUN pip install pydantic
RUN pip install openai
RUN pip install typo
# RUN pip install python-dotenv
# RUN pip install -q  torch peft bitsandbytes transformers trl accelerate sentencepiece

#Important so we will have access to the run.sh file 
COPY . . 

CMD ["sh", "run.sh"]
