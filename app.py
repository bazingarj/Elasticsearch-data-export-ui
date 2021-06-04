from flask import Flask
from flask import render_template, request, make_response
import json
from elasticsearch import Elasticsearch, helpers, exceptions
import io, csv
from flask import Response

def checkSlash(text, pos, action):
        if action == "add" and text[pos] != '/':
                return text[:pos] + '/' + text[pos:] if pos != -1 else text+"/"
        elif action == "remove" and text[pos] == '/' :
                return  text[:pos] + text[pos+1:]
        return text

def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '.')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '.')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

class Line(object):
    def __init__(self):
        self._line = None
    def write(self, line):
        self._line = line
    def read(self):
        return self._line

def generateCSV(ES_HOST, index_name, query):
  try:
      es = Elasticsearch( ES_HOST )
      data = es.search( index = index_name, body = query, scroll = '5m')
      #print ("total docs:", len(resp["hits"]["hits"]))
      sid = data['_scroll_id']
      scroll_size = len(data['hits']['hits'])
      
      line = Line()
      writer = csv.writer(line, quoting=csv.QUOTE_NONNUMERIC)

      headers = True
      print(scroll_size)
      headersList = []
      while scroll_size > 0:
          "Scrolling... "+str(scroll_size)
          # Before scroll, process current batch of hits
          for i in data['hits']['hits']:
              if headers:
                  headersList = flatten_json(i['_source'])
                  writer.writerow(headersList)
                  yield line.read()
                  headers = False
              tmp = flatten_json(i['_source']) #.values() for only values
              sendToCsv = []
              for j in headersList:
                  sendToCsv.append(tmp[j] if j in tmp else '')
              writer.writerow(sendToCsv)
              yield line.read()

          data = es.scroll(scroll_id=sid, scroll='5m')

          # Update the scroll ID
          sid = data['_scroll_id']

          # Get the number of results that returned in the last scroll
          scroll_size = len(data['hits']['hits'])
  except exceptions.ConnectionError as err:
    client = None
    return 'Elasticsearch client error '+str(err)


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('/index.html')


@app.route('/process', methods=['POST'])
def process():

  ES_HOST = checkSlash(request.form['server_url'], -1, 'add')
  index_name = checkSlash( request.form['index'], 0, 'remove' )
  
  query = request.form['query']

  #output = make_response(dest.getvalue())
  output = Response(generateCSV(ES_HOST, index_name, query), mimetype='text/csv')
  output.headers["Content-Disposition"] = "attachment; filename=export.csv"
  #output.headers["Content-type"] = "text/csv"
  return output

      


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)

