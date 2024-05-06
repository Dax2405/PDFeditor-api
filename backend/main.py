from fastapi import FastAPI, UploadFile, HTTPException, File
from fastapi.responses import FileResponse
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from typing import List
import os


app = FastAPI()


@app.post("/unir_pdfs/")
async def unir_pdfs(files: List[UploadFile] = File(...)):
    merger = PdfMerger()

    for file in files:
        if file.filename.split(".")[-1] != "pdf":
            raise HTTPException(
                status_code=400, detail="Tipo de archivo invalido, solo se permiten archivos PDF.")
        merger.append(file.file)

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
    with open(f"temp_{name}.pdf", "wb") as buffer:
        buffer.write(file.file.read())

    os.system(
        f"gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/screen -dNOPAUSE -dQUIET -dBATCH -sOutputFile={name}_comprimido.pdf temp_{name}.pdf")

    return FileResponse(f"{name}_comprimido.pdf", media_type="application/pdf", filename=f"{name}_comprimido.pdf")


@app.post("/dividir_pdf/")
async def dividir_pdf(file: UploadFile = File(...), start: int = 0, end: int = 0):
    if file.filename.split(".")[-1] != "pdf":
        raise HTTPException(
            status_code=400, detail="Tipo de archivo invalido, solo se permiten archivos PDF.")

    reader = PdfReader(file.file)
    writer = PdfWriter()
    for i in range(start-1, end):
        writer.add_page(reader.pages[i])

    with open("pdf_dividido.pdf", "wb") as buffer:
        writer.write(buffer)

    return FileResponse("pdf_dividido.pdf", media_type="application/pdf", filename="pdf_dividido.pdf")
