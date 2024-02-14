# FROM --platform=linux/arm64/v8 python:3.11.6-slim 
FROM python:3.11.6-slim 
# WORKDIR /Users/seanwdc/Desktop/experiments/databricksapp
WORKDIR /home/app
COPY . .
RUN pip3 install -r requirements.txt
EXPOSE 8501
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health
#Run your application
ENTRYPOINT ["python", "-m", "streamlit", "run", "./app.py", "--server.port=8501"]