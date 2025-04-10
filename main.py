from flask import Flask, request, send_file, render_template_string
import pandas as pd
import os
import zipfile
import tempfile

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string(open('index.html', 'r', encoding='utf-8').read())

@app.route('/converter', methods=['POST'])
def converter():
    arquivos = request.files.getlist('files')
    temp_dir = tempfile.mkdtemp()

    for arquivo in arquivos:
        nome_base = os.path.splitext(arquivo.filename)[0]
        caminho_xlsx = os.path.join(temp_dir, nome_base + '.xlsx')

        try:
            df = pd.read_excel(arquivo, sheet_name=None)
            with pd.ExcelWriter(caminho_xlsx, engine='xlsxwriter') as writer:
                for nome_aba, dados in df.items():
                    dados.to_excel(writer, sheet_name=nome_aba, index=False)
        except Exception as e:
            print(f"Erro ao converter {arquivo.filename}: {e}")

    zip_path = os.path.join(temp_dir, 'convertidos.zip')
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file in os.listdir(temp_dir):
            if file.endswith('.xlsx'):
                zipf.write(os.path.join(temp_dir, file), arcname=file)

    return send_file(zip_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)  # porta específica pro Render