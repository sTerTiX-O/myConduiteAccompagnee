from flask import Flask
from flask import Response
from flask import request

app = Flask(__name__)

@app.route("/prenom/<prenom>/nom/<nom>", methods=['GET'])
def hello_world(prenom, nom):
    monHeaderAuthentification = request.headers.get('x-mca-auth')
    theResponseValue = "{} {} is Fat (x-mca-auth={})!".format(prenom, nom, monHeaderAuthentification)
    theResponse = Response(theResponseValue, mimetype='text/plain')
    return theResponse


if __name__ == "__main__":
    app.run(debug=True)
