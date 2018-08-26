#!/bin/bash
service nginx start
export FLASK_APP=manage.py
export FLASK_CONFIG=development
export SECRET_KEY='feagrhtjeyagdhjsyt'
# POSTGRES_DB=recipe_db
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
# flask db init
# flask db migrate
# flask db upgrade