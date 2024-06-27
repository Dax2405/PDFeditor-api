"use client";

import React, { useState } from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import axios from "axios";

const SubirArchivo = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [error, setError] = useState("");

  const handleFileUpload = async (event: any) => {
    let files = event.target.files;

    // Check file size (each must be less than 30MB)
    for (let i = 0; i < files.length; i++) {
      if (files[i].size > 30 * 1024 * 1024) {
        setError(
          "Uno o más archivos son demasiado grandes. Cada uno debe ser menor de 30MB."
        );
        return;
      }
    }

    // Create a FormData object
    let formData = new FormData();
    for (let i = 0; i < files.length; i++) {
      formData.append("files", files[i]);
    }

    // Send the files to the backend
    const response = await axios.post(
      "http://127.0.0.1:8000/unir_pdfs/",
      formData,
      {
        responseType: "blob", // to handle pdf file
      }
    );

    // Create a new blob object
    const url = window.URL.createObjectURL(new Blob([response.data]));

    // Create a link, click it, and revoke it
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", "file.pdf"); // or any other extension
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="flex justify-center items-center h-screen">
      <Card>
        <CardHeader>
          <CardTitle>Unir PDFs</CardTitle>
          <CardDescription>Máximo 30 MB</CardDescription>
        </CardHeader>
        <CardContent>
          <input
            type="file"
            accept=".pdf"
            onChange={handleFileUpload}
            multiple
            className=""
          />
        </CardContent>
      </Card>
      {error && <p className="text-red-500">{error}</p>}
    </div>
  );
};

export default SubirArchivo;
