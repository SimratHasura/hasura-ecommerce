import os
import yaml


def generate_schema(query_tables=[], metadata_file=None, debug=False):
    """Loads the metadata if available and raises error if not available"""
    hard_coded_tmp_schema_dict = {
    "product": """
        Table name: product
        Table description: Contains information about products

        Columns:
        id: int
        created_at: timestamp
        updated_at: timestamp
        price: numeric
        image_urls: jsonb
        category_display_name: text
        brand: text
        name: text
        description: text
    """
    }

    schema_to_be_returned = "".join("\n\n"+hard_coded_tmp_schema_dict.get(table_schema,"") 
                                    for table_schema in query_tables)
    return schema_to_be_returned
    # -------
    # Uncomment below code when v3 metadata is available
    # -------
    # if not metadata_file:
    #     # Get the path to directory two level above this file
    #     metadata_file = os.path.join(
    #         os.path.dirname(
    #             os.path.dirname(
    #                 os.path.abspath(__file__)
    #                 )
    #             ), 
    #         "metadata/metadata.hml")
    # with open(metadata_file, "r") as f:
    #     table_schemas = []
    #     relationships = {}
    #     # yaml.FullLoader
    #     # yaml.load(f, Loader=yaml.FullLoader) yaml.safe_load_all(f) yaml.load(f, Loader=yaml.FullLoader): # 
    #     for section in yaml.safe_load_all(f):
    #         if section['kind'] == 'ObjectType':
    #             # If query_tables is empty, then select all tables
    #             if not query_tables:
    #                 table_schemas.append(section)
    #             elif query_tables and section['definition']['name'] in query_tables:
    #                 table_schemas.append(section)
    #         # V3 currently doesn't support relationships. Msg dated - 17th Nov 2023
    #         # if section['kind'] == 'Relationship':
    #         #     relation = {
    #         #         'relationship_name': section['definition']['name'], 
    #         #         'from': section['definition']['source'], 
    #         #         'to': section['definition']['target']['model']['name'],
    #         #         'relationship_type': section['definition']['target']['model']['relationshipType']
    #         #     }
    #         #     if relation['from'] in query_tables and relation['to'] in query_tables:
    #         #         table_relations = relationships.get(relation['from'], [])
    #         #         table_relations.append(relation)
    #         #         relationships[relation['from']] = table_relations

    # schema_txt = ""
    # for table_schema in table_schemas:
    #     schema_txt += "Table name: " + table_schema['definition']['name'] + "\n"
    #     for field in table_schema['definition']['fields']:
    #         schema_txt += f"{field['name']}: {field['type']}\n"
    #     # table_relationship = relationships.get(table_schema['definition']['name'], [])
    #     # for relation in table_relationship:
    #     #     schema_txt += f"{relation['relationship_name']}: table relationship/join from {relation['from']} to {relation['to']}\n"
    #     schema_txt += "\n\n"

    # schema_txt += """
    # Table name: base_products_category_enum
    # Table descripton: Enum table for category column in base_products table

    # Values in category column:
    # laptop
    # clothing
    # television

    # Table name: product_description
    # Table descripton: Text description of products used for product search based on similarity with user query
    # near_text: string
    # """
    
    if debug is True:   
        print(schema_txt)
    return schema_txt

if __name__ == "__main__":
    generate_schema()
        