#!/bin/sh

export MONGO_DB_URI="mongodb+srv://dbMaster:xl4xu2po9BJST0tu@crm-template.rrvgs.mongodb.net/<dbname>?retryWrites=true&w=majority"

python app.py

