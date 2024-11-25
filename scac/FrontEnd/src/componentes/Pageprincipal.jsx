import React, { useState } from "react";

function PagePrincipal() {
  const [file1, setFile1] = useState(null);
  const [file2, setFile2] = useState(null);

  const handleFile1Change = (e) => {
    setFile1(e.target.files[0]);
  };

  const handleFile2Change = (e) => {
    setFile2(e.target.files[0]);
  };

  const handleSubmit = async () => {

    if (!file1 || !file2) {
      alert("Por favor, selecciona ambos archivos.");
      return;
   

    }

    const formData = new FormData();
    formData.append("file1", file1);
    formData.append("file2", file2);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/process-files/", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        const contentType = response.headers.get("Content-Type");
        if (contentType === "application/json") {
          const result = await response.json();
          console.log("Resultado:", result);
        } else {
          const blob = await response.blob();
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement("a");
          a.href = url;
          a.download = "resultado.xlsx";
          a.click();
          console.log("Archivo descargado exitosamente.");
        }
      } else {
        console.error("Error en el servidor:", await response.text());
      }
    } catch (error) {
      console.error("Error al procesar los archivos:", error);
    }
    

  };

  return (
    <div>
      <h1>Subir Archivos</h1>
      <input type="file" onChange={handleFile1Change} />
      <input type="file" onChange={handleFile2Change} />
      <button onClick={handleSubmit}>Descargar</button>
    </div>
  );
}

export default PagePrincipal;
