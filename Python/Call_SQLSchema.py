import psycopg2
import json
from Database_Connect import ConnectionSQL
from File_Paths import (json_tables_schema_file_path,
                        json_fields_schema_file_path,
                        json_index_schema_file_path,
                        tables_input,
                        fields_input,
                        indexes_input)
from dotenv import load_dotenv

load_dotenv()

def get_field_info(pcursor, pinput, pisfield) -> dict:
    pcursor.execute(pinput)
    inputs = pcursor.fetchall()

    inputData = []
    inputTxt = ""
    for inp in inputs:
        if pisfield == 0:
            inputData.append({
                "name": inp[0],
                "description": inp[1] if len(inp) > 1 else None,
                "fields": inp[2]
            })
            inputTxt = "tables"
        
        elif pisfield == 1:
            inputData.append({
                "table name": inp[0],
                "fields name": inp[1],
                "field description": inp[2] if len(inp) > 2 else None,
                "data type": inp[3]
            })
            inputTxt = "fields"
    
    return {inputTxt: inputData}

# Şema bilgisini çeker
def get_schema_info():
    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(**ConnectionSQL.get_connection_info())
        cursor = conn.cursor()

        tables = get_field_info(cursor, tables_input, 0)
        fields = get_field_info(cursor, fields_input, 1)

        with open(json_tables_schema_file_path, "w", encoding="utf-8") as f:
            json.dump(tables, f, ensure_ascii=False, indent=4)
        
        with open(json_fields_schema_file_path, "w", encoding="utf-8") as f:
            json.dump(fields, f, ensure_ascii=False, indent=4)

        print("✅ Şema bilgileri JSON dosyalarına başarıyla yazıldı.")

    except Exception as e:
        print(f"❌ Şema çekme sırasında hata oluştu: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# JSON'a yaz
get_schema_info()