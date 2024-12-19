from flask import Flask, request
import json
import uuid
import xmltodict
import os
from nfelib.nfe.bindings.v4_0.proc_nfe_v4_00 import NfeProc

app = Flask(__name__)

UPLOAD_FOLDER = "nfes"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Cria o diretório, se não existir

def upload_xml():

    file_name = f"{uuid.uuid4()}.xml"

    try:
        xml_data = request.data.decode("utf-8")

        file_path = os.path.join(UPLOAD_FOLDER, file_name)

        with open(file_path, "w", encoding="utf-8") as xml_file:
            xml_file.write(xml_data)

        return file_path

    except Exception as e:
        os.remove(file_path)
        return f"Erro ao processar o XML: {str(e)}", 500



@app.route("/api/xml", methods=["POST"])
def returnXmlAsJson():
    file_path = upload_xml()

    nfe_proc = NfeProc.from_path(file_path)

    xml_dict = xmltodict.parse(nfe_proc.to_xml())

    os.remove(file_path)

    res = json.dumps(xml_dict, indent=4, ensure_ascii=False)

    print(res)

    return res




if __name__ == "__main__":
    app.run(debug=True)
