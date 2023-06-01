import os
import subprocess
import uuid
from flask import Flask, request


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
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
        return str(process.stdout)

    return app

