import React, { useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import sena from '../../assets/img/logosena.png';
import "./Pageprincipal.css";

function PagePrincipal({ handleLogout }) {
  const navigate = useNavigate();
  const [circle, setCircle] = useState(null);

  const [file1, setFile1] = useState(null);
  const [file2, setFile2] = useState(null);
  const [currentScreen, setCurrentScreen] = useState("upload"); // Estado para manejar pantallas

  const handleFile1Change = (e) => {
    setFile1(e.target.files[0]);
  };

  const handleFile2Change = (e) => {
    setFile2(e.target.files[0]);
  };
  const fileInputRef = useRef(null); // Referencia al input de archivo

  const handleSubmit = async () => {
    if (!file1 || !file2) {
      alert("Por favor, selecciona ambos archivos.");
      return;
    }

    // Aquí no se cambia automáticamente la pantalla, solo se envían los datos al servidor
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
          const blob = await response.blob(); // Descargar el archivo
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement("a");
          a.href = url;
          a.download = "resultado.xlsx"; // Nombre del archivo descargado
          a.click();
          window.URL.revokeObjectURL(url); // Limpia el objeto de URL
        }
      } else {
        console.error("Error en el servidor:", await response.text());
      }
    } catch (error) {
      console.error("Error al procesar los archivos:", error);
    }
  };



  // Primera vista de inicio landingPage 

  return (
    <div className="Contenedorprincipal">
      <div className="columnaizquierda">
        <div className="letrascolumna">
          <img src={sena} alt="LogoSena" className="imgsena" />
          <div className="Enlances">
            <span>Complementaria</span>
            <span>Titulada</span>
          </div>
          <button onClick={handleLogout}>Cerrar sesión</button>
        </div>
      </div>

      <div className="contenedormitad">
        {currentScreen === "upload" && (
          <>
            <div className="processingScreen">
              <div className="titulosca">
                <h1 className="titusca">Sistema de Certificacion de Aprendices </h1>
              </div>
              <div className="mensajedebienvenida">
                <h2>INSTRUCTOR</h2>
                <span>
                  Este asistente te guiará en el proceso de validación de tus
                  archivos de Sofía Plus.
                </span>
                <div className="listado">
                  <h3>¿Qué puedes hacer aquí?</h3>
                  <ul>
                    <li>Cargar archivos .XLSX de Sofía Plus</li>
                    <li>Validar información de aprendices</li>
                    <li>Generar reportes de validación</li>
                    <li>Descargar resultados</li>
                  </ul>
                  <span>*Nota: Los archivos deben estar en formato .XLSX.</span>
                </div>
              </div>
              <div
                className="custom-div"
                onClick={() => fileInputRef.current.click()} // Simula clic en el input
                onDrop={(e) => {
                  e.preventDefault();
                  const file = e.dataTransfer.files[0];
                  if (file) {
                    setFile1(file); // O setFile2 según corresponda
                  }
                }}
                onDragOver={(e) => e.preventDefault()}
              >
                <p className="upload-title, cursor-pointer">Arrastra un archivo o haz clic aquí</p>
                <input
                  id="file1"
                  type="file"
                  className="hidden-input"
                  accept=".xlsx , .xls"
                  ref={fileInputRef} // Asocia la referencia al input
                  onChange={(e) => setFile1(e.target.files[0])} // O setFile2 según corresponda
                />
              </div>
              {file1 && (
                <div className="archivonombre">
                  <p className="file-name">Archivo cargado: {file1.name}</p>
                </div>
              )}
              <div className="buttonorganizado">
                <button className="botonescontinuar" onClick={() => setCurrentScreen("processing")}>CONTINUAR</button>
              </div>

            </div>
          </>
        )}




        {/* // Segunda vista luego de subir el primer archivo */}

        {currentScreen === "processing" && (
          <div className="processingScreen">
            <div className="titulosca">
              <h1 className="titusca">Sistema de Certificacion de Aprendices</h1>
            </div>
            <div className="mensajedebienvenida">
              <h2>SOFIA</h2>
              <span>
                Este asistente te guiará en el proceso de validación de tus
                archivos de Sofía Plus.
              </span>
              <div className="listado">
                <h3>¿Qué puedes hacer aquí?</h3>
                <ul>
                  <li>Cargar archivos .XLSX de Sofía Plus</li>
                  <li>Validar información de aprendices</li>
                  <li>Generar reportes de validación</li>
                  <li>Descargar resultados</li>
                </ul>
                <span>*Nota: Los archivos deben estar en formato .XLSX.</span>
              </div>

            </div>
            <div
              className="custom-div"
              onClick={() => fileInputRef.current.click()} // Simula clic en el input
              onDrop={(e) => {
                e.preventDefault();
                const file = e.dataTransfer.files[0];
                if (file) {
                  setFile2(file);
                }
              }}
              onDragOver={(e) => e.preventDefault()}
            >
              <label htmlFor="file2" className="upload-label , cursor-pointer">
                <p className="upload-title">Arrastra un archivo o haz clic aquí</p>
                <input
                  id="file2"
                  type="file"
                  className="hidden-input"
                  accept=".xlsx , .xls"
                  ref={fileInputRef}
                  onChange={(e) => setFile2(e.target.files[0])}
                />
              </label>
            </div>
            {file2 && (
              <div className="archivonombre">
                <p className="file-name">Archivo cargado: {file2.name}</p>
                <button>X</button>
              </div>
            )}

            <div className="buttonorganizado">
              <button className="botonescontinuar" onClick={() => setCurrentScreen("result")}>Siguiente</button>
              <button className="botonescontinuar" onClick={() => setCurrentScreen("upload")}>Volver</button>
            </div>

          </div>
        )}


        {/* //Tercera vista para el resultado */}

        {currentScreen === "result" && (
          <div className="resultScreen">
            <h2>¡Procesamiento completado!</h2>
            <p>Los resultados están listos para ser descargados.</p>
            <button className="botonescontinuar" onClick={handleSubmit}>
              <i className="fas fa-check-circle"></i> Descargar
            </button>

            <button className="botonescontinuar" onClick={() => setCurrentScreen("upload")}>Volver al inicio</button>
          </div>
        )}
      </div>
    </div>
  );
}

export default PagePrincipal;
