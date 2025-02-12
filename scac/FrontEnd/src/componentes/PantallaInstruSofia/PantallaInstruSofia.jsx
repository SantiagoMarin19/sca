import React from "react";

function PantallaInstruSofia({ file1, file2, handleScreenChange }) {
    const handleSubmit = async () => {
        if (!file1 || !file2) {
            alert("Por favor, selecciona ambos archivos.");
            return;
        }

        const formData = new FormData();
        formData.append("file1", file1);
        formData.append("file2", file2);

        try {
            const response = await fetch("http://127.0.0.1:8000/api/process-comparacion/", {
                method: "POST",
                body: formData,
            });

            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement("a");
                a.href = url;
                a.download = "ComparacionResultado.xlsx";
                a.click();
                window.URL.revokeObjectURL(url);
            } else {
                console.error("Error en el servidor:", await response.text());
            }
        } catch (error) {
            console.error("Error al procesar los archivos:", error);
        }
    };

    return (
        <div className="resultScreen">
            <h2>Validacion de Datos de Aprendices</h2>
            <p>Esta validacion compara Numero de Documento , Tipo de Documento , Nombre de aprendiz </p>
            <p>Genera un archivo validando que los datos coincidan en su totalidad </p>
            <p>Al final del archivo encontraras una columna COINCIDENCIA </p>
            <button className="botonescontinuar" onClick={handleSubmit}>
                <i className="fas fa-check-circle"></i> Descargar Comparación
            </button>
            <button
                className="botonescontinuar"
                onClick={() => handleScreenChange("upload")}
            >
                <i className="fas fa-arrow-left"></i> Volver
            </button>
        </div>
    );
}

export default PantallaInstruSofia;