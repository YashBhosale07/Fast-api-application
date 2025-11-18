FROM ubuntu:22.04

RUN apt-get update && apt-get install -y python3 python3-pip

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "demo:app", "--host", "0.0.0.0", "--port", "8000"]