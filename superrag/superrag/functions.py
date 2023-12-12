fewshot_examples= """
Assume Table1 and Table2 are structured tables. Table1 is joined to Table2 using relationship. Relationship name is Table1_to_Table2.
Table1 has columns - T1C1, T1C2, T1C3 and Table2 has columns - T2C1, T2C2, T2C3.

1. Query the fields of tables joined by relationship using the relationship name. Relationship name will be available as another column in the table.
Example: query MyQuery{Table1(where: {Table1_to_Table2: {T2C1: {_eq: "T2C1 value"}, T2C2: {_eq: "T2C2 value"}}, 
                                    T1C1: {_eq: "T1C1 value"}, "T1C3": {_eq: "T1C3 value"}}){
                                        T1C1 T1C2 T1C3 Table1_to_Table2{T2C1 T2C2 T2C3
                                        }}}

2. If Query filters are available, then use them in the where condition of the query.
""" 


def generate_openai_functions(schema):
    """Generates functions for GraphQL generation with OpenAI Function Calling"""
    gql_generation_functions = [
        {
            "name": "fetch_query_details_from_natural_language",
            "description": "Given a natural language query, extract the details of the query in natural language.",
            "parameters": {
                "type": "object",
                "properties": {
                "query_detail": {
                    "type": "string",
                    "description": "Summary of requested query.",
                },
                "query_where_parameters": {
                    "type": "string",
                    "description": "Where parameters of requested query.",
                },
                "query_table": {
                    "type": "string",
                    "description": "Table names of requested query.",
                },
                "query_columns": {
                    "type": "string",
                    "description": "Result column names of requested query.",
                },
                "query_limit": {
                    "type": "string",
                    "description": "Limit of requested query.",
                },
                "query_order_by": {
                    "type": "string",
                    "description": "Order by of requested query.",
                }
                },
            },
        },
        {
            "name": "generate_graphql_query",
            "description": "Map the user's query and query filters to schema and generate Hasura style GraphQL query to fetch answers for user's questions.",
            "parameters": {
                "type": "object",
                "properties": {
                    "graphql_query": {
                        "type": "string",
                        "description": f"""
                                Generate GraphQL query to fetch answers for user's questions and filters from schema.
                                Use the schema provided below, don't generate table or column names.
                                {schema}

                                Important instructions:
                                {fewshot_examples}

                                """
                    } # Add placeholder for optional examples
                }
            }
        }
    ]
    return gql_generation_functions