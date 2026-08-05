import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { HomeScreen } from './screens/HomeScreen';
import { ClientesScreen } from './screens/ClientesScreen';
import { AnamneseScreen } from './screens/AnamneseScreen';
import { AnamneseDetailScreen } from './screens/AnamneseDetailScreen';
import './App.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomeScreen />} />
        <Route path="/clientes" element={<ClientesScreen />} />
        <Route path="/clientes/novo" element={<div>Novo Cliente (em breve)</div>} />
        <Route path="/clientes/:id/editar" element={<div>Editar Cliente (em breve)</div>} />
        <Route path="/anamnese" element={<AnamneseScreen />} />
        <Route path="/anamnese/nova" element={<div>Nova Anamnese (em breve)</div>} />
        <Route path="/anamnese/:id" element={<AnamneseDetailScreen />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}

export default App;