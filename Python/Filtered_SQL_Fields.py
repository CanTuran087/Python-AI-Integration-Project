import json
import Gpt_Table_Response
from File_Paths import (AI_response_json_tables_schema_file_path,
                        json_fields_schema_file_path,
                        filtered_json_fields_schema_file_path)

# AI yanıtından gelen tablo adlarını oku
with open(AI_response_json_tables_schema_file_path, "r", encoding="utf-8") as tf:
    tables_data = json.load(tf)
    tableNames = [tbl["name"] for tbl in tables_data["tables"]]

# Tüm tablo alanlarını oku
with open(json_fields_schema_file_path, "r", encoding="utf-8") as ff:
    allFields = json.load(ff)["fields"]

filteredFields = [
    field for field in allFields if field["table name"] in tableNames
]

# Filtrelenmiş Alan Şema Bilgisi
with open(filtered_json_fields_schema_file_path, "w", encoding="utf-8") as f:
        json.dump({"fields" : filteredFields}, f, ensure_ascii=False, indent=4)

with open(filtered_json_fields_schema_file_path, "r", encoding="utf-8") as f:
    schema_info = json.dumps(json.load(f)["fields"], ensure_ascii=False, indent=2)

print(f"✅ Filtrelenmiş alanlar {filtered_json_fields_schema_file_path} dosyasına yazıldı.")