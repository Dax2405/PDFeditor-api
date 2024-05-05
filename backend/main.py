from fastapi import FastAPI, UploadFile, HTTPException, File
from fastapi.responses import FileResponse
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from typing import List


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
    reader = PdfReader(file.file)
    writer = PdfWriter()
    for page in reader.pages:
        page.compress_content_streams()
        writer.add_page(page)

    output_pdf = "pdf_comprimido.pdf"
    with open(output_pdf, "wb") as f:
        writer.write(f)

    reader = PdfReader(output_pdf)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)

    writer.add_metadata(reader.metadata)

    with open(output_pdf, "wb") as fp:
        writer.write(fp)
    return FileResponse(output_pdf, media_type="application/pdf", filename=output_pdf)
