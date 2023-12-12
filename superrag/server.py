from superrag import SuperRAG

from fastapi import FastAPI
from fastapi import Body

from fastapi.middleware.cors import CORSMiddleware
from http.server import BaseHTTPRequestHandler, HTTPServer

from pydantic import BaseModel

app = FastAPI()
sr_product = SuperRAG(query_tables=["product"])

# Add CORSMiddleware to the application instance
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class UserQuery(BaseModel):
    natural_query: str
    query_filters: dict

@app.get('/hello_world')
def hello_world():
    return {"message": "Hello World"}

@app.post('/query_product')
def query_product(incoming_query: UserQuery):
    # return sr_product.generate_query(natural_query)
    return sr_product.execute_query(incoming_query.natural_query, query_filters=incoming_query.query_filters)

# Only for testing, just returns the query
@app.post('/generate_product_query')
def generate_product_query(incoming_query: UserQuery):
    # return sr_product.generate_query(natural_query)
    return sr_product.generate_query(incoming_query.natural_query, query_filters=incoming_query.query_filters)
# Admin queries here

