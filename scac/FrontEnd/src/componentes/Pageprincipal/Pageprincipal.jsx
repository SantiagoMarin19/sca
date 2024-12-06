import React, { useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import sena from '../../assets/img/logosena.png';
import logosofia from '../../assets/img/logosofiacopia.png';
import Pantallados from "../Segundapantalla/Pantallados";
import Pantallatres from "../Tercerapantalla/Pantallatres";

import "./Pageprincipal.css";

function PagePrincipal({ handleLogout }) {
  const navigate = useNavigate();
  const [file1, setFile1] = useState(null);
  const [file2, setFile2] = useState(null);
  const [currentScreen, setCurrentScreen] = useState("upload");
  const fileInputRef = useRef(null); 

  const handleFile1Change = (e) => setFile1(e.target.files[0]);
  const handleFile2Change = (e) => setFile2(e.target.files[0]);

  const handleRemoveFile1 = () => {
    setFile1(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  const handleRemoveFile2 = () => {
    setFile2(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  const handleScreenChange = (screen) => {
    setCurrentScreen(screen);
    window.scrollTo(0, 0);
  };

  const handleSubmit = async () => {
    if (!file1 || !file2) {
      alert("Por favor, selecciona ambos archivos.");
      return;
    };

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
          window.URL.revokeObjectURL(url);
        }
      } else {
        console.error("Error en el servidor:", await response.text());
      }
    } catch (error) {
      console.error("Error al procesar los archivos:", error);
    }
  };

  return (
    <div className="Contenedorprincipal">
      <div className="columnaizquierda">
        <div className="letrascolumna">
          <img src={sena} alt="LogoSena" className="imgsena" />
          <div className="Enlances">
            <span><i className="bi bi-motherboard-fill"></i> Complementaria</span>
            <span><i className="bi bi-mortarboard-fill"></i> Titulada</span>
          </div>
        </div>
        <div className="enlacesabajo">
          <span className="buttoncerrar" onClick={handleLogout}>
            <i className="bi bi-box-arrow-right"></i>Cerrar sesión
          </span>
          <span className="derechosreservados">Todos los derechos reservados CBI Palmira</span>
        </div>
      </div>

      <div className="contenedormitad">
        {currentScreen === "upload" && (
          <>
          
            {/* Pantalla2 Component */}
            <Pantallados
              file1={file1}
              setFile1={setFile1}
              fileInputRef={fileInputRef}
              handleRemoveFile1={handleRemoveFile1}
              handleScreenChange={handleScreenChange}
            />
          </>
        )}
        
        {currentScreen === "processing" && (
          <Pantallatres
            file2={file2}
            setFile2={setFile2}
            fileInputRef={fileInputRef}
            handleRemoveFile2={handleRemoveFile2}
            handleScreenChange={handleScreenChange}
          />
        )}

        {currentScreen === "result" && (
          <div className="resultScreen">
            <h2>¡Procesamiento completado!</h2>
            <p>Los resultados están listos para ser descargados.</p>
            <button className="botonescontinuar" onClick={handleSubmit}>
              <i className="fas fa-check-circle"></i> Descargar
            </button>
            <button className="botonescontinuar" onClick={() => handleScreenChange("upload")}>
              Volver al inicio
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export default PagePrincipal;
