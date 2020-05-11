from flask import Flask
from schema import Query
from flask_graphql import GraphQLView
from graphene import Schema
import os

# Allows GraphQL to be used as a testing interface
# To disable, change graphiql to False
view_func = GraphQLView.as_view(
    'graphql', schema=Schema(query=Query), graphiql=True)

# Adds graphql as a flask
app = Flask(__name__)
app.add_url_rule('/graphql', view_func=view_func)

# Creates the server on port 5000 if the script is run directly
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000))
