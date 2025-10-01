import os

# Dosya yolları
json_main_folder_path = "/Users/user/Desktop/App/AI Projects/Json"
doc_main_folder_path = "/Users/user/Desktop/App/AI Projects/Doc"
output_file_path = os.path.join(json_main_folder_path, "output.json")
input_file_path = os.path.join(doc_main_folder_path, "input.txt")
json_schema_file_path = os.path.join(json_main_folder_path, "schema_info.json")
tables_query_file_path = os.path.join(doc_main_folder_path, "tables_input.txt")
fields_query_file_path = os.path.join(doc_main_folder_path, "fields_input.txt")
indexes_query_file_path = os.path.join(doc_main_folder_path, "indexes_input.txt")

# Tablo, Alan ve Index Alan JSON Şema Dosya Yolları
json_tables_schema_file_path = os.path.join(json_main_folder_path, "tables_schema_info.json")
json_fields_schema_file_path = os.path.join(json_main_folder_path, "fields_schema_info.json")
json_index_schema_file_path = os.path.join(json_main_folder_path, "index_schema_info.json")
AI_response_json_tables_schema_file_path = os.path.join(json_main_folder_path, "AI_response_tables_schema_info.json")
filtered_json_fields_schema_file_path = os.path.join(json_main_folder_path, "filtered_fields_schema_info.json")

# Sorguları oku
input = ""
tables_input = ""
fields_input = ""
indexes_input = ""

with open(input_file_path, "r", encoding="utf-8") as file:
    input = file.read()

with open(tables_query_file_path, "r", encoding="utf-8") as file:
    tables_input = file.read()

with open(fields_query_file_path, "r", encoding="utf-8") as file:
    fields_input = file.read()

with open(indexes_query_file_path, "r", encoding="utf-8") as file:
    indexes_input = file.read()
