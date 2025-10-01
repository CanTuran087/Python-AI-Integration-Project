import os, json, psycopg2
from datetime import date, datetime
from openai import OpenAI
from dotenv import load_dotenv
from Database_Connect import ConnectionSQL
from File_Paths import tables_input, fields_input, input, output_file_path
from Filtered_SQL_Fields import schema_info

# .env dosyasını yükle
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# SQL sorgusunu çalıştıran fonksiyon
def query_database(sql_query: str):
    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(**ConnectionSQL.get_connection_info())
        cursor = conn.cursor()
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        results = []
        for row in rows:
            result_dict = dict(zip(columns, row))
            for column, value in result_dict.items():
                if isinstance(value, (date, datetime)):
                    result_dict[column] = value.strftime('%Y-%m-%d')
            results.append(result_dict)
        return results
    except Exception as e:
        return {"error": str(e)}
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# GPT’ye tanıtılacak tool
tools = [
    {
        "type": "function",
        "function": {
            "name": "query_database",
            "description": "SQL sorgusunu PostgreSQL veritabaninda calistirir.",
            "parameters": {
                "type": "object",
                "properties": {
                    "sql_query": {
                        "type": "string",
                        "description": f"SQL SELECT sorgusu. Örneğin, tablo isimlerini öğrenmek için: {tables_input}, alan isimlerini öğrenmek için: {fields_input}"
                    }
                },
                "required": ["sql_query"]
            }
        }
    }
]

# Mesajları tanımla
messages = [
    {"role": "system", "content": "Sen bir PostgreSQL veritabani asistanisin. Kullanicinin dogal dildeki sorgularini SQL'e cevir ve calistir."},
    {"role": "system", "content": schema_info},
    {"role": "user", "content": input}
]

# GPT'den tool çağrısı al
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages,
    tools=tools,
    tool_choice="auto"
)

# Tool çağrısı ve argüman alma
tool_call = response.choices[0].message.tool_calls[0]
arguments = json.loads(tool_call.function.arguments)

# Tool çağrısını mesaja ekle
messages.append({"role": "assistant", "tool_calls": [tool_call]})

# SQL sorgusunu çalıştır
result = query_database(arguments["sql_query"])

# Tool cevabını mesajlara ekle
messages.append({
    "role": "tool",
    "tool_call_id": tool_call.id,
    "content": json.dumps({"sql_query": arguments["sql_query"], "result": result}, ensure_ascii=False, indent=4)
})

# Açıklama isteme
messages.append({
    "role": "user",
    "content": f"Asagidaki SQL sorgusunu acikla ve sorgudan gelen degerleri yaz:\n\nSQL:\n```sql\n{arguments['sql_query']}\n```\n\nSonuclar:\n{json.dumps(result, ensure_ascii=False, indent=4)}"
})

# Açıklama alma
final_response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages
)

# Son JSON çıktısı
output = {
    "sql_query": arguments["sql_query"],
    "result": result,
    "gpt_explanation": final_response.choices[0].message.content
}

# JSON dosyasına yaz
try:
    with open(output_file_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
except TypeError as e:
    print("JSON'a yazma hatası:", e)
    print("Dump edilemeyen veri:", output)

# Yazdır
print("SQL Sorgusu:")
print(f"```sql\n{arguments['sql_query']}\n```")
print("\nVeritabanından Gelen Sonuçlar:")
print(json.dumps(result, ensure_ascii=False, indent=4))
print("\nGPT Açıklaması:")
print(final_response.choices[0].message.content)