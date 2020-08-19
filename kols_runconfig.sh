#!/bin/sh

export MONGO_DB_URI="mongodb+srv://dbuser:dbpass@crm-template.rrvgs.mongodb.net/<dbname>?retryWrites=true&w=majority"
export SECRET_KEY="KOLSKEY124"
python app.py