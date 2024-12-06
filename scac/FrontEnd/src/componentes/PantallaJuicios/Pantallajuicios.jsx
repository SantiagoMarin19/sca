import React from "react";
import update from '../../assets/img/upload.png';
import logosofia from "../../assets/img/logosofiacopia.png"

function Pantallajuicio ({handleScreenChange}) {
    return (
        <div className="processingScreen">
            <div className="titulosca">
                <h1 className="titusca">Modulo Archivo de Carga de Juicios de <img src={logosofia} alt="LogoSofia" className="LogoSofia" /></h1>
            </div>
            <div className="mensajedebienvenida">
                <h2 className="tituloinstru">Modulo Archivo Juicios  </h2>
                <div className="spanbienve">
                    <span className="spanbienvenida">
                        !Ya casi estamos ¡ Ahora estamos en el tercer paso y ultimo
                    </span>
                    <span>Sube, carga o arrastra el archivo descargado de Juicios</span>
                    <span className="spanbienvenida">
                        Este archivo debe contener los estudiantes con sus juicios aprobados y no aprobados en su debido formato.
                    </span>
                    <span className="spanbienvenida">
                        El archivo debe estar en formato .xlsx o .xls (Excel).
                    </span>
                    <span className="spanbienvenida">
                        Recomendaciones: Asegurate de que el archivo JUICIO contenga la misma FICHA de cada de los archivos subidos anteriormente .
                    </span>
                </div>
                <div className="listado">
                    <h3>¿Qué puedes hacer aquí?</h3>
                    <ul>
                        <li>Cargar archivos .XLSX o .XLS verificación SofiaPlus</li>
                        <li>Validar información de aprendices</li>
                        <li>Generar reportes de validación</li>
                        <li>Descargar resultados</li>
                    </ul>
                </div>
            </div>
            <div className="contenedorcircle">
                <div className="circle">1</div>
                <div className="circle" id="dos">2</div>
                <div className="circle">3</div>
                <div className="line"></div>
            </div>

            <div className="contenedordearchivos">
                <h1 className="titulocontenedorarch">Ingresa aqui el archivo descargado de SofiaPlus</h1>


                
            </div>
            <div className="buttonorganizado">
                    <button className="botonescontinuar" onClick={() => handleScreenChange("resultados")}>Siguiente</button>
                    <button className="botonescontinuar" onClick={() => handleScreenChange("sofia")}>Volver</button>
                </div>
        </div>
            );
};

export default Pantallajuicio;
