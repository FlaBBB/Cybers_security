import openai

openai.api_key = "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"

def ask_chatgpt(msg):
    completion = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [
            {"role": "system", "content": """rules:
        1. ini adalah simulasi tanya jawab, saya memberi pertanyaan, kamu menjawab
        2. jawaban hanya menggunakan huruf kecil, tidak ada huruf kapital
        3. hanya berikan jawaban singkat, tidak perlu penjelasan
        4. tidak perlu memberikan titik di belakang

        *contoh: 
        ```
        question: arti wholesome
        answer: baik
        ```"""},
            {"role": "user", "content": msg},
        ]
    )
    
    return completion.choices[0].message

print(ask_chatgpt("ubah 2/5 menjadi bentuk desimal?"))