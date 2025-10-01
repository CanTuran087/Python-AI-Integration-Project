import os, json
from openai import OpenAI
from dotenv import load_dotenv
from File_Paths import input_file_path, json_tables_schema_file_path, AI_response_json_tables_schema_file_path

# .env dosyasını yükle
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Kullanıcı girdisini oku
with open(input_file_path, "r", encoding="utf-8") as f:
    input_text = f.read()

# Tabloları oku (schema'dan veya doğrudan liste olarak)
with open(json_tables_schema_file_path, "r", encoding="utf-8") as f:
    data = json.load(f)
    table_schema_info = data.get("tables", data)

# GPT mesajları
messages = [
    {
        "role": "system",
        "content": (
            "Sen bir PostgreSQL veritabani asistanisin. "
            "Verilen tablo semasina gore SQL sorgulari olusturabilirsin. "
            "JOIN islemleri yapmaktan cekinme."
        )
    },
    {
        "role": "system",
        "content": json.dumps(table_schema_info, ensure_ascii=False)
    },
    {
        "role": "user",
        "content": (
            f"Asagidaki kullanici istegine göre hangi tablolara ihtiyac olduğunu belirle:\n\n"
            f"{input_text}\n\n"
            "Sadece gerçekten ihtiyac duyulan tablolari bir JSON listesi olarak ver. "
            "Lutfen cevapta sadece JSON iceriğini gönder, baska aciklama yapma, kod blogu kullanma."
        )
    }
]

# GPT'den yanıt al
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages
)

# Cevabı temizle ve işle
ai_tables_response = response.choices[0].message.content.strip()

# Eğer yanıt kod bloğu ile geldiyse temizle
if ai_tables_response.startswith("```json"):
    ai_tables_response = ai_tables_response.replace("```json", "").replace("```", "").strip()

# JSON olarak kaydet
try:
    json_data = json.loads(ai_tables_response)

    # Eğer düz liste geldiyse: ["table1", "table2"]
    if isinstance(json_data, list):
        tables_formatted = {"tables": [{"name": t} for t in json_data]}
    # Eğer zaten doğru formatta geldiyse (nadir durumlar için)
    elif isinstance(json_data, dict) and "tables" in json_data:
        tables_formatted = json_data
    else:
        raise ValueError("Beklenmeyen format: " + str(json_data))

    # JSON dosyasına yaz
    with open(AI_response_json_tables_schema_file_path, "w", encoding="utf-8") as f:
        json.dump(tables_formatted, f, ensure_ascii=False, indent=4)

    print(f"✅ Gereken tablolar '{AI_response_json_tables_schema_file_path}' dosyasına yazıldı.")

except (json.JSONDecodeError, ValueError) as e:
    print("❌ JSON format hatası:", e)
    print("Gelen içerik:\n", ai_tables_response)