import flask
from flask import request, jsonify
import sqlite3
import numpy as np

# Debug allows for changes to be seen in real time.
app = flask.Flask(__name__)
app.config["DEBUG"] = True

def dictFactory(cursor, row):
    """
    Function that parses the entries of the database and returns them as a list of dictionaries.

    @param cursor -- A cursor object using sqlite.
    @param row -- The row of the database being parsed.
    """
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/', methods=['GET'])
def homePage():
    return '''
    <h1>Datascience Jobs Database</h1>
    <h3>You have reached: /home/</h3>
    <p>To view all entries in the database: '127.0.0.1:5000/api/v1/jobs/datascience/all' </p>
    <p>To filter entries based on country : '127.0.0.1:5000/api/v1/jobs/datascience?country=United%20States' </p>
    <p>To filter entries based on post id : '127.0.0.1:5000/api/v1/jobs/datascience?id=81953194' </p>
'''

@app.route('/api/v1/jobs/datascience/all', methods=['GET'])
def apiViewAll():
    conn = sqlite3.connect('data/phosphorus_database.db')
    conn.row_factory = dictFactory
    cur = conn.cursor()
    all_books = cur.execute('SELECT * FROM tblPhos;').fetchall()

    return jsonify(all_books)

@app.errorhandler(404)
def pageNotFound(e):
    return "<h1>Error 404</h1><p>Page not found.</p>", 404

@app.route('/api/v1/jobs/datascience', methods=['GET'])
def apiViewByFilter():
    '''
    Function that allows users to filter the results in the API based on specified input.
    '''
    query_parameters = request.args

    Id = query_parameters.get('Id')
    FoodName = query_parameters.get('FoodName')
    servingSize = query_parameters.get('servingSize')
    phosphorusMg = query_parameters.get('phosphorusMg')
    phosphorusCategory = query_parameters.get('phosphorusCategory')
    foodSubCategory = query_parameters.get('foodSubCategory')
    foodCategory = query_parameters.get('foodCategory')
    query = "SELECT * FROM tblPhos WHERE"
    to_filter = []

    if Id:
        query += ' Id=? AND'
        to_filter.append(Id)

    if FoodName:
        query += ' FoodName=? AND'
        to_filter.append(FoodName)

    if servingSize:
        query += ' servingSize=? AND'
        to_filter.append(servingSize)

    if phosphorusMg:
        query += ' phosphorusMg=? AND'
        to_filter.append(phosphorusMg)

    if phosphorusCategory:
        query += ' phosphorusCategory=? AND'
        to_filter.append(phosphorusCategory)

    if foodSubCategory:
        query += ' foodSubCategory=? AND'
        to_filter.append(foodSubCategory)

    if foodCategory:
        query += ' foodCategory=? AND'
        to_filter.append(foodCategory)

    if not (Id or FoodName or servingSize or phosphorusMg or phosphorusCategory or foodSubCategory or foodCategory):
        return pageNotFound(404)

    query = query[:-7] + ';'

    conn = sqlite3.connect('data/phosphorus_database.db')
    conn.row_factory = dictFactory
    cur = conn.cursor()
    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)

app.run()
