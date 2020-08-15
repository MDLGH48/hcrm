#!/bin/sh

export MONGO_DB_URI="mongodb+srv://<user>:<pass>@<cluster>.<blah>.mongodb.net/<dbname>?retryWrites=true&w=majority"

python app.py

