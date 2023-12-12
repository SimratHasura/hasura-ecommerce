import os
import json
from pprint import pprint
from superrag.metadata_parser import generate_schema
from superrag.hasura_utils import HasuraConnection
from superrag.query_generation import HasuraQueryEngine

from dotenv import load_dotenv
load_dotenv()

class SuperRAG:
    """
    Instant RAG data API that fetches only relevant context.
    Current implementation is single query session. 
    """
    def __init__(self, query_tables=[], role="admin", metadata_file=None, model=None, graphql_endpoint=None, admin_secret=None, validate=True, debug=False):
        self.role = role
        self.debug = debug
        self.query_tables = query_tables
        self.schema = generate_schema(query_tables=self.query_tables, metadata_file=metadata_file, debug=debug)
        if model is None:
            model = os.getenv("MODEL")
        if graphql_endpoint is None:
            graphql_endpoint = os.getenv("GRAPHQL_ENDPOINT")
        if admin_secret is None:
            admin_secret = os.getenv("ADMIN_SECRET")
        

        if model is None:
            raise Exception("Model can't be empty. Set it as env variables or pass it during class initialization.") 
        
        if graphql_endpoint is None or admin_secret is None:
            print("Hasura project details not found, query can't be validated.")
            self.validate = False
        else:
            self.validate = validate

        self.hasura_conn = HasuraConnection(graphql_endpoint, admin_secret)
        self.hq_engine = HasuraQueryEngine(model, self.schema, debug)


    def update_query_tables(self, query_tables=[]):
        self.query_tables = query_tables
        self.schema = generate_schema(query_tables=self.query_tables)

    def execute_query(self, user_query, query_filters={}):
        response_dict = {}
        generated_query = self.hq_engine.generate_gql_query(user_query, query_filters)
        result, status = self.hasura_conn.execute_query(generated_query)
        response_dict["query"] = generated_query
        response_dict["query_result"] = result
        response_dict["query_execution_status"] = status
        return result, response_dict

    def generate_query(self, user_query, query_filters={}):

        # Generate Hasura GQL query
        print("Inputs to generate query", user_query, query_filters)
        query = self.hq_engine.generate_gql_query(user_query, query_filters)
        response =  {
            "query":query,
            "query_status": None
        }

        if self.validate is True:
            # Validate filters

            # Validate generated query
            val_result = self.hasura_conn.validate_query(query)
            if len(val_result) > 0:
                response["query_status"] = False
            else:
                response["query_status"] = True

            # Identify missing information
            information_not_available = self.hasura_conn.process_validation_result(val_result)
            if self.debug is True:
                print(query)
            if information_not_available:
                response["information_not_available"] = information_not_available
            
            if self.debug is True:
                print(val_result)
                response["validation_result"]= val_result

        return response
            

    
if __name__ == "__main__":

    debug = False
    query_tables = ["base_products"]
    SR = SuperRAG(query_tables=query_tables, debug=debug)

    # --- Single table query
    # Case 1
    query = "show me all products under $500"
    response = SR.generate_query(query)
    pprint("Query::" + query)
    print(json.dumps(str(response), indent=4))
    print("\n\n")

    # Case 2
    query = "show me all products with fastest delivery"
    response = SR.generate_query(query)
    pprint("Query::" + query)
    print(json.dumps(str(response), indent=4))

    print("\n\n")


    # --- Relationship queries
    # # Case 1
    # query = "show me all products with rating more than 4"
    # response = SR.generate_query(query)
    # pprint("Query::" + query)
    # pprint("Response::" + str(response))
    # print("\n\n")

    # # Case 2
    # query = "show me all products with seller rating more than 4"
    # response = SR.generate_query(query)
    # pprint("Query::" + query)
    # pprint("Response::" + str(response))
    # print("\n\n")

        