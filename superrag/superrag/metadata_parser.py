import os
import yaml


def generate_schema(query_tables=[], metadata_file=None, debug=False):
    """Loads the metadata if available and raises error if not available"""
    schema_txt = """
    Table name: product
        Table description: Contains information about products
        Columns:
            Column name: id
                Column type: int
                Column description: Unique identifier for each product
            Column name: created_at
                Column type: timestamp
                Column description: Timestamp when product was created
            Column name: updated_at
                Column type: timestamp
                Column description: Timestamp when product was last updated
            Column name: price
                Column type: numeric
                Column description: Price of the product
            Column name: image_url
                Column type: jsonb
                Column description: Image url of the product
            Column name: category_display_name
                Column type: text
                Column description: Display category name of the product. 
                Column values: 
                    "Home Furnishing", "Computers", "Baby Care", "Wearable Smart Devices", 
                    "Furniture", "Home Entertainment", "Home & Kitchen", "Clothing", 
                    "Beauty and Personal Care", "Sunglasses", "Tools & Hardware", 
                    "Household Supplies", "Home Improvement", "Footwear", "Gaming", 
                    "Mobiles & Accessories", "Sports & Fitness", "Health & Personal Care Appliances", 
                    "Home Decor & Festive Needs", "Pens & Stationery", "Watches", "Food & Nutrition", 
                    "Kitchen & Dining", "Pet Supplies", "Jewellery", "Cameras & Accessories", 
                    "Automotive", "eBooks", "Toys & School Supplies", "Eyewear", 
                    "Automation & Robotics", "Bags, Wallets & Belts"
            Column name: brand
                Column type: text
                Column description: Brand of the product
            Column name: name
                Column type: text
                Column description: Name of the product
            Column name: description
                Column type: text
                Column description: Description of the product
    """

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

    
    if debug is True:   
        print(schema_txt)
    return schema_txt

if __name__ == "__main__":
    generate_schema()
        