fewshot_examples= """
Assume Table1 and Table2 are structured tables. Table1 is joined to Table2 using relationship. Relationship name is Table1_to_Table2.
Table1 has columns - T1C1, T1C2, T1C3 and Table2 has columns - T2C1, T2C2, T2C3.

Query the fields of tables joined by relationship using the relationship name. Relationship name will be available as another column in the table.
Example: query MyQuery{Table1(where: {Table1_to_Table2: {T2C1: {_eq: "T2C1 value"}, T2C2: {_eq: "T2C2 value"}}, 
                                    T1C1: {_eq: "T1C1 value"}, "T1C3": {_eq: "T1C3 value"}}){
                                        T1C1 T1C2 T1C3 Table1_to_Table2{T2C1 T2C2 T2C3
                                        }}}

All string values should be enclosed in double quotes.
""" 


def generate_openai_functions(schema):
    """Generates functions for GraphQL generation with OpenAI Function Calling"""
    gql_generation_functions = [
        {
            "name": "fetch_query_details_from_natural_language",
            "description": "Given a natural language query, extract the details of the query in natural language. based on the schema provided below.\n {schema}",
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
            "description": "Map the user's input to schema and generate Hasura style GraphQL query to fetch answers for user's questions.",
            "parameters": {
                "type": "object",
                "properties": {
                    "graphql_query": {
                        "type": "string",
                        "description": f"""
                                Generate GraphQL query to fetch answers for user's questions from schema.
                                Use the schema provided below, don't generate table or column names.
                                Schema:
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