import os
import json
from pprint import pprint
from superrag.functions import generate_openai_functions
from superrag.openai_utils import chat_completion_request


class HasuraQueryEngine:
    def __init__(self, model, schema, debug=False):
        self.model = model
        self.schema = schema
        self.debug = debug

    def parse_chat_reponse(self, chat_response):
        """Parses chat response and returns JSON response"""
        try:
            chat_response = chat_response.json()
            assistant_message = chat_response["choices"][0]["message"]
            if self.debug is True:
                print(assistant_message)
        except Exception as e:
            msg = "Unable to generate GraphQL query. Error:"+str(e)+"\n"+str(chat_response)
            print(chat_response)
            print(msg)
            raise Exception(msg)
        response = json.loads(assistant_message["function_call"]["arguments"], strict=False)
        return response


    def generate_gql_query(self, user_query, query_filters={}):
        messages = []
        # =================================================== #
        # Step 1: Get query details from user query           #
        # =================================================== #

        gql_generation_functions = generate_openai_functions(self.schema)
        messages.append({"role": "system", 
        "content": "You are a Hasura GraphQL expert. Your goal is to understand user's query in natural language and create Hasura style GraphQL query using user's query and query filters."})
        messages.append({"role": "user", "content": user_query})
        query_filter_statement = ""
        if query_filters:
            query_filter_statement += "Query filters:\n"
            query_filter_statement += "\n".join(key+": "+value for key, value in query_filters.items())
            query_filter_statement += "\n\n"

        messages.append({"role": "user", "content": query_filter_statement})
        messages.append({"role": "user", "content": "Start all queries with keyword 'query'."})
        messages.append({"role": "user", "content": "Return all the columns of the table(s)."})

        # chat_response = chat_completion_request(messages, self.model, gql_generation_functions,
        #     function_call={"name": "fetch_query_details_from_natural_language"})
        # chat_response = chat_response
        # query_details = self.parse_chat_reponse(chat_response)

        # =================================================== #
        # Step 2: Generate query                              #
        # =================================================== #    
        # if self.debug is True:
        #     print("Query details",query_details)
        # messages.append({"role": "system", "content": f"User's search criteria is {query_details}" })
        # messages.append({"role": "system", 
        # "content": "Generate Hasura style GraphQL query based on user's search criteria. User's search criteria needs to be converted to Hasura style query."})
        chat_response = chat_completion_request(messages, self.model,  gql_generation_functions, 
            function_call={"name": "generate_graphql_query"})
        json_response = self.parse_chat_reponse(chat_response)
        query = json_response["graphql_query"]
        return query

