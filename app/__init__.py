import os
import subprocess
import uuid
from flask import Flask, request
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app)

    # a simple page that says hello
    @app.route('/hello', methods = ['POST'])
    def hello():
        data = request.files
        file = data["contract"]
        id = uuid.uuid4()
        fp = open("{}.sol".format(str(id)), 'w')
        for i,line in enumerate(file):
            if i == 0:
                version = line.decode().replace("pragma solidity ^", "")
                version = version.replace(";\n", "")
                subprocess.run("solc-select use {} --always-install".format(version), shell=True)
            fp.write(line.decode())
        fp.close()

        process = subprocess.run("slither ./{}.sol --checklist".format(str(id)), stdout=subprocess.PIPE, shell=True)
        os.remove("{}.sol".format(str(id)))
        return process.stdout.decode()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=os.getenv("PORT", default=5000))