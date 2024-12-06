import React, { useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import sena from '../../assets/img/logosena.png';
import Pantallados from "../Segundapantalla/Pantallados";
import Pantallatres from "../Tercerapantalla/Pantallatres";
import Pantallajuicio from "../PantallaJuicios/Pantallajuicios";
import Pantallaresult from "../Pantallaresultado/Pantallaresultado";

import "./Pageprincipal.css";

function PagePrincipal({ handleLogout }) {
  const navigate = useNavigate();

  // Declarar los estados file1 y file2
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
          <Pantallados
            file1={file1}
            setFile1={setFile1}
            fileInputRef={fileInputRef}
            handleRemoveFile1={handleRemoveFile1}
            handleScreenChange={handleScreenChange}
          />
        )}
        
        {currentScreen === "sofia" && (
          <Pantallatres
            file2={file2}
            setFile2={setFile2}
            fileInputRef={fileInputRef}
            handleRemoveFile2={handleRemoveFile2}
            handleScreenChange={handleScreenChange}
          />
        )}

        {currentScreen === "juicios" && (
          <Pantallajuicio
            handleScreenChange={handleScreenChange}
          />
        )}

        {currentScreen === "resultados" && (
          <Pantallaresult
            file1={file1}
            file2={file2}
            handleScreenChange={handleScreenChange}
          />
        )}
      </div>
    </div>
  );
}

export default PagePrincipal;
