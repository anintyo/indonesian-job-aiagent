from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from src.tools.sql_tool import get_schema, run_query

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

_SQL_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """Kamu adalah expert SQL yang membantu menjawab pertanyaan tentang lowongan kerja di Indonesia.

Skema tabel:
{schema}

Ketentuan:
- Hanya tulis query SELECT, tidak ada yang lain
- Kolom salary_min dan salary_max dalam satuan Rupiah (bisa NULL jika tidak ada info gaji)
- Kolom work_type berisi: "Full time", "Paruh waktu", "Kontrak/Temporer", "Kasual"
- Gunakan LIKE untuk pencarian teks, case-insensitive dengan LOWER()
- Jika user tanya tentang jumlah, gunakan COUNT
- Batasi hasil dengan LIMIT 10 kecuali user minta semua
- Kembalikan HANYA query SQL, tanpa penjelasan apapun"""),
    ("human", "{query}")
])

_ANSWER_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """Kamu adalah asisten pencari kerja yang membantu user menemukan lowongan yang tepat.
Berikan jawaban yang natural dan informatif dalam Bahasa Indonesia berdasarkan hasil query SQL.
Jika hasilnya kosong, katakan tidak ada lowongan yang sesuai dengan kriteria tersebut.
Jangan sebutkan detail teknis seperti nama kolom atau SQL."""),
    ("human", """Pertanyaan user: {query}

Hasil dari database:
{results}

Berikan jawaban yang membantu.""")
])


def run(query: str) -> str:
    schema = get_schema()

    sql_chain = _SQL_PROMPT | llm
    sql = sql_chain.invoke({"schema": schema, "query": query}).content.strip()

    # Bersihkan markdown code block jika ada
    if sql.startswith("```"):
        sql = "\n".join(sql.split("\n")[1:-1]).strip()

    try:
        rows = run_query(sql)
    except Exception as e:
        return f"Terjadi kesalahan saat mengambil data: {str(e)}"

    answer_chain = _ANSWER_PROMPT | llm
    return answer_chain.invoke({"query": query, "results": rows}).content
