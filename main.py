from fastapi import FastAPI, UploadFile, HTTPException, File, Form
from fastapi.responses import FileResponse
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from typing import List
import os
import subprocess
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MAX_FILE_SIZE = 40 * 1024 * 1024


def is_valid_pdf(file_path: str) -> bool:
    try:
        reader = PdfReader(file_path)
        return True
    except:
        return False


def scan_file_for_malware(file_path: str) -> bool:

    result = subprocess.run(['clamscan', file_path], stdout=subprocess.PIPE)
    return "OK" in result.stdout.decode()


@app.post("/unir_pdfs/")
async def unir_pdfs(files: List[UploadFile] = File(...)):
    merger = PdfMerger()

    for file in files:
        if file.filename.split(".")[-1] != "pdf":
            raise HTTPException(
                status_code=400, detail="Tipo de archivo invalido, solo se permiten archivos PDF.")

        temp_file_path = f"/tmp/{file.filename}"
        with open(temp_file_path, "wb") as buffer:
            buffer.write(file.file.read())

        if os.path.getsize(temp_file_path) > MAX_FILE_SIZE:
            os.remove(temp_file_path)
            raise HTTPException(
                status_code=400, detail="El archivo es demasiado grande.")

        if not is_valid_pdf(temp_file_path):
            os.remove(temp_file_path)
            raise HTTPException(
                status_code=400, detail="El archivo PDF no es válido.")

        if not scan_file_for_malware(temp_file_path):
            os.remove(temp_file_path)
            raise HTTPException(
                status_code=400, detail="El archivo contiene malware.")

        merger.append(temp_file_path)
        os.remove(temp_file_path)

    output_pdf = "pdf_unido.pdf"
    merger.write(output_pdf)
    merger.close()

    return FileResponse(output_pdf, media_type="application/pdf", filename=output_pdf)


@app.post("/comprimir_pdf/")
async def comprimir_pdf(file: UploadFile = File(...)):
    if file.filename.split(".")[-1] != "pdf":
        raise HTTPException(
            status_code=400, detail="Tipo de archivo invalido, solo se permiten archivos PDF.")

    name = file.filename.split(".")[0]
    temp_file_path = f"/tmp/compress.pdf"
    with open(temp_file_path, "wb") as buffer:
        buffer.write(file.file.read())
    if os.path.getsize(temp_file_path) > MAX_FILE_SIZE:
        os.remove(temp_file_path)
        raise HTTPException(
            status_code=400, detail="El archivo es demasiado grande.")

    if not is_valid_pdf(temp_file_path):
        os.remove(temp_file_path)
        raise HTTPException(
            status_code=400, detail="El archivo PDF no es válido.")

    if not scan_file_for_malware(temp_file_path):
        os.remove(temp_file_path)
        raise HTTPException(
            status_code=400, detail="El archivo contiene malware.")

    os.system(
        f"gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/screen -dNOPAUSE -dQUIET -dBATCH -sOutputFile=/tmp/pdf_comprimido.pdf {temp_file_path}")

    return FileResponse(f"/tmp/pdf_comprimido.pdf", media_type="application/pdf", filename=f"{name}_comprimido.pdf")


@app.post("/dividir_pdf/")
async def dividir_pdf(file: UploadFile = File(...), start: int = Form(...),  end: int = Form(...)):
    if file.filename.split(".")[-1] != "pdf":
        raise HTTPException(
            status_code=400, detail="Tipo de archivo invalido, solo se permiten archivos PDF.")
    temp_file_path = f"/tmp/split.pdf"
    with open(temp_file_path, "wb") as buffer:
        buffer.write(file.file.read())
    if os.path.getsize(temp_file_path) > MAX_FILE_SIZE:
        os.remove(temp_file_path)
        raise HTTPException(
            status_code=400, detail="El archivo es demasiado grande.")

    if not is_valid_pdf(temp_file_path):
        os.remove(temp_file_path)
        raise HTTPException(
            status_code=400, detail="El archivo PDF no es válido.")

    if not scan_file_for_malware(temp_file_path):
        os.remove(temp_file_path)
        raise HTTPException(
            status_code=400, detail="El archivo contiene malware.")

    reader = PdfReader(file.file)
    writer = PdfWriter()
    for i in range(start-1, end):
        writer.add_page(reader.pages[i])

    with open(temp_file_path, "wb") as buffer:
        writer.write(buffer)

    return FileResponse(temp_file_path, media_type="application/pdf", filename="pdf_dividido.pdf")
