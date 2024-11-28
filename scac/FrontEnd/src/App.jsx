import React, { useState } from "react";
import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom";
import Inicio from "../src/componentes/Inicio/Inicio";
import PagePrincipal from "../src/componentes/Pageprincipal/Pageprincipal";

const App = () => {
    const [token, setToken] = useState(localStorage.getItem("token"));

    // Lógica para manejar el cierre de sesión
    const handleLogout = () => {
        setToken(null);
        localStorage.removeItem("token"); // Eliminar el token al cerrar sesión
    };

    return (
        <Router>
            <Routes>
                {/* Ruta de Inicio de Sesión */}
                <Route
                    path="/login"
                    element={
                        token ? (
                            <Navigate to="/principal" replace /> // Si ya hay un token, redirige al principal
                        ) : (
                            <Inicio setToken={setToken} /> // Muestra el componente de login
                        )
                    }
                />

                {/* Ruta de Página Principal */}
                <Route
                    path="/principal"
                    element={
                        token ? (
                            <PagePrincipal handleLogout={handleLogout} /> // Si hay token, muestra la página principal
                        ) : (
                            <Navigate to="/login" replace /> // Si no hay token, redirige al login
                        )
                    }
                />

                {/* Ruta no encontrada */}
                <Route path="*" element={<Navigate to="/login" replace />} />
            </Routes>
        </Router>
    );
};

export default App;
