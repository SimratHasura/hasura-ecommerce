import os
import json
import requests
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from graphql import validate


class HasuraConnection:
    def __init__(self, graphql_endpoint=None, admin_secret=None):
        self.client = self.get_client(graphql_endpoint, admin_secret)

    def get_client(self, graphql_endpoint, admin_secret):
        """Fetches Hasura client"""
        
        gql_headers = {'x-hasura-admin-secret': admin_secret}
        # Create a GraphQL client with the request transport
        transport = RequestsHTTPTransport(
            url=graphql_endpoint, 
            headers=gql_headers)
        client = Client(transport=transport, 
                        fetch_schema_from_transport=True)
        return client

    def execute_query(self, query):
        """Executes Hasura GraphQL query and returns result and status"""
        try:
            gql_query = gql(query)
            result = self.client.execute(gql_query)
        except Exception as e:
            return None, False
        return result, True


    def validate_query(self, query):
        """"Validates Hasura GraphQL query and returns validation result"""
        self.client.connect_sync()
        gql_query = gql(query)
        result_err = []
        try:
            result_err = validate(schema=self.client.schema, 
                                document_ast=gql_query)
        except Exception as e:
             print("Exception in validating query", query, "Error:", e) # Handle 
        self.client.close_sync()
        return result_err


    def process_validation_result(self, validation_result):
        """Processes validation result and returns list of fields that are not available in database schema"""
        information_not_available = []
        for error in validation_result:
            if "is not defined by type" in error.message:
                error_parts = error.message.split("'")
                # check if field is available in database schema
                if error_parts[1] not in error_parts[3]:
                    information_not_available.append("Information/Relationship is not available : {0}".format(error_parts[1]))
        return information_not_available
