import React, { useState } from "react";
import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom";
import Inicio from "../src/componentes/Inicio/Inicio";
import PagePrincipal from "../src/componentes/Pageprincipal/Pageprincipal";

const App = () => {
    const [token, setToken] = useState(localStorage.getItem("token"));

    const handleLogout = () => {
        setToken(null);
        localStorage.removeItem("token"); // Eliminar el token al cerrar sesión
    };

    return (
        <Router>
            <Routes>
                {/* Ruta de Inicio de Sesión */}
                <Route
                    path="/"
                    element={
                        token ? <Navigate to="/principal" replace /> : <Inicio setToken={setToken} />
                    }
                />

                {/* Ruta de Página Principal */}
                <Route
                    path="/principal"
                    element={
                        token ? (
                            <PagePrincipal handleLogout={handleLogout} />
                        ) : (
                            <Navigate to="/" replace />
                        )
                    }
                />

                {/* Ruta no encontrada */}
                <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
        </Router>
    );
};

export default App;
