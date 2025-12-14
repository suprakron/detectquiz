from flask import Flask, jsonify
import pyodbc

app = Flask(__name__)
def get_quiz_data():
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=HP\\SQLEXPRESS;"
        "DATABASE=detectquiz;"
        "Trusted_Connection=yes;"
    )
    cursor = conn.cursor()
    query = """
    SELECT TOP (1000)
        [id],
        [subject_code],
        [subject_name],
        [test_name],
        [answer_key],
        [full_score],
        [teacher_name],
        CONVERT(datetime, [created_at]) AS created_at,
        CONVERT(datetime, [exam_date]) AS exam_date
    FROM [detectquiz].[dbo].[quiz_answerexam]
    """
    cursor.execute(query)
    columns = [col[0] for col in cursor.description]
    results = []
    for row in cursor.fetchall():
        row_dict = {col: (str(val) if hasattr(val, "isoformat") else val) for col, val in zip(columns, row)}
        results.append(row_dict)
    cursor.close()
    conn.close()
    return results

@app.route('/api/quiz', methods=['GET'])
def quiz_api():
    data = get_quiz_data()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)

# import pyodbc
# import json

# conn = pyodbc.connect(
#     "DRIVER={ODBC Driver 17 for SQL Server};"
#     "SERVER=HP\\SQLEXPRESS;"
#     "DATABASE=detectquiz;"
#     "Trusted_Connection=yes;"
# )

# cursor = conn.cursor()

# query = """
# SELECT TOP (1000)
#     [id],
#     [subject_code],
#     [subject_name],
#     [test_name],
#     [answer_key],
#     [full_score],
#     [teacher_name],
#     CONVERT(datetime, [created_at]) AS created_at,
#     CONVERT(datetime, [exam_date]) AS exam_date
# FROM [detectquiz].[dbo].[quiz_answerexam]
# """

# cursor.execute(query)

# columns = [column[0] for column in cursor.description]

# results = []
# for row in cursor.fetchall():
#     row_dict = {col: (str(val) if isinstance(val, (bytes, bytearray)) else val) for col, val in zip(columns, row)}
#     results.append(row_dict)

# json_data = json.dumps(results, indent=4, default=str)

# print(json_data)

# cursor.close()
# conn.close()
