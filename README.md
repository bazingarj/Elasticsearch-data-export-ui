# Elasticsearch-data-export-ui

This is very userful tool to allow dumping of Elasticsearch data using a Query.

To use it normally on server First run 
```pip install -r requirements.txt```
```python3 app.py```

after running the commands go to localhost:8000 or SERVER_IP:8000

To run it via docker directly run :

sudo docker run -p 8000:8000 -d bazingarj/elasticsearch-data-export-ui:1.0


This project only support csb export for now.

