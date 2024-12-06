import React, { useRef } from "react";
import update from '../../assets/img/upload.png';
import "../Pageprincipal/Pageprincipal.css";


function Pantallados({ file1, setFile1, fileInputRef, handleRemoveFile1, handleScreenChange }) {
    return (
        <div className="processingScreen">
            <div className="titulosca">
                <h1 className="titusca">Bienvenido al Sistema de Certificación de Aprendices</h1>
            </div>
            <div className="mensajedebienvenida">
                <h2 className="tituloinstru">Modulo de Archivo Verificación de Instructor</h2>
                <div className="spanbienve">
                    <span className="spanbienvenida">
                        ¡Bienvenido! Este asistente te guiará en el proceso de certificación de Aprendices.
                    </span>
                    <span className="spanbienvenida">
                    Sube, carga o arrastra el archivo proporcionado por el instructor.
                  </span>
                    <span>Este archivo debe estar en formato .xlsx o .xls (excel).</span>
                    <span className="spanbienvenida">
                        Recomendaciones: asegúrate de que el archivo contenga celdas llenas y no tenga errores de formato.
                    </span>
                </div>
                <div className="listado">
                <h3>¿Qué puedes hacer aquí?</h3>
                <ul>
                    <li>Cargar archivos .XLSX o .XLS verificación instructor</li>
                    <li>Validar información de aprendices</li>
                    <li>Generar reportes de validación</li>
                    <li>Descargar resultados</li>
                </ul>
            </div>
            </div>
            
            <div className="contenedorcircle">
                <div className="circle" id="uno">1</div>
                <div className="circle">2</div>
                <div className="circle">3</div>
                <div className="line"></div>
            </div>

            <div className="contenedordearchivos">
                <h1 className="titulocontenedorarch">Ingresa aqui el archivo descargado de el instructor</h1>
                <div
                    className="custom-div"
                    onClick={() => fileInputRef.current.click()}
                    onDrop={(e) => {
                        e.preventDefault();
                        const file = e.dataTransfer.files[0];
                        if (file) {
                            setFile1(file);
                        }
                    }}
                    onDragOver={(e) => e.preventDefault()}
                >
                    <p className="titulocontenedorarch">Arrastra el archivo o haz clic aquí</p>
                    <img src={update} alt="Logoupdate" className="imgupdate" />
                    <input
                        id="file1"
                        type="file"
                        className="hidden-input"
                        accept=".xlsx , .xls"
                        ref={fileInputRef}
                        onChange={(e) => setFile1(e.target.files[0])}
                    />
                </div>
            </div>
            {file1 && (
                <div className="archivonombre">
                    <span className="spanicono">
                        <i className="bi bi-check-square-fill icono-archi"></i> Archivo cargado correctamente
                    </span>
                    <div className="campoarchivo">
                        <span className="file-name">
                            <i className="bi bi-file-earmark-excel icono-archidos"></i>
                            {file1.name}
                        </span>
                        <button className="delete-button" onClick={handleRemoveFile1}>x</button>
                    </div>
                </div>
            )}
            {file1 && (
                <div className="buttonorganizado">
                    <button className="botonescontinuar" onClick={() => handleScreenChange("sofia")}>
                        CONTINUAR
                    </button>
                </div>
            )}
        </div>
    );
}

export default Pantallados;
