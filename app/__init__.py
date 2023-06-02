import os
import re
import subprocess
import uuid
from flask import Flask, request
from flask_cors import CORS


regex = re.compile(
    r'^(?P<major>0|[1-9]\d*)'
    r'\.'
    r'(?P<minor>0|[1-9]\d*)'
    r'\.'
    r'(?P<patch>0|[1-9]\d*)'
    r'(?:-'
    r'(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)'
    r'(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?'
    r'(?:\+'
    r'(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$'
)


def create_app():
    app = Flask(__name__)
    CORS(app)

    # a simple page that says hello
    @app.route('/hello', methods = ['POST'])
    def hello():
        data = request.files
        file = data["contract"]
        # id = uuid.uuid4()
        fp = open(file.filename, 'w')
        for line in file:
            version = line.decode().replace("pragma solidity ^", "")
            version = version.replace(";\n", "")
            if regex.match(version):
                version = line.decode().replace("pragma solidity ^", "")
                version = version.replace(";\n", "")
                subprocess.run("solc-select use {} --always-install".format(version), shell=True)
            
            fp.write(line.decode().replace("@openzeppelin", "node_modules/@openzeppelin"))
        fp.close()


        process = subprocess.run("slither ./{} --checklist --filter-paths '@openzepellin/'".format(file.filename), stdout=subprocess.PIPE, shell=True)
        os.remove(file.filename)
        return process.stdout.decode()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=os.getenv("PORT", default=5000))