from flask import Flask, render_template, request
import json
from main import bing_serach
app = Flask(__name__)
@app.route("/", methods=['GET','POST'])
def websearch():
    try:
        if(request.args.get('auth') == 'Forninja'):
            if request.args.get('q'):
                query = request.args.get('q')
                ifextract =  request.args.get('ifextract')
                if ifextract == '1':
                    return bing_serach(query,ifextract=True)
                elif ifextract == '0':
                    return bing_serach(query,ifextract=False)
                else:
                    return '<h1>Invalid Value of ifextract</h1><br>it can Two Value either 0 or 1<br> for 1 it will provide Webpage Extracted'
            else:
                return '<h1>Enter Valid Query</h1> <br> GET parameters<br>1. q(query) = Search query in quote_plus ex: Is+Mango+Sweet<br>1. ifextract(ifextract) = 0,1 for 1 it will provide extracted webpage for suitable websites'
        else:
            return 'Access Denied'
    except:
        return 'Unknown Error as whole'
@app.route("/log",)
def log():
    try:
        if(request.args.get('auth') == 'Forninja'):
            try:
                with open('log.txt','r',encoding='utf-8') as f:
                    return f.read()
            except:
                return 'Some error while setting '
        else:
            return 'Access Denied'
    except:
        return 'Unknown Error as whole'

if __name__ == '__main__':
    app.run(debug=True, port=1777)