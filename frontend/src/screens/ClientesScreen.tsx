import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { FiPlus, FiSearch, FiUser, FiEdit2, FiTrash2, FiArrowLeft, FiRefreshCw } from 'react-icons/fi';
import { api } from '../services/api';
import './ClientesScreen.css';

interface Cliente {
  id_cliente: string;
  nome_completo: string;
  nome_exibicao?: string;
  pronomes?: string;
  identidade_genero?: string;
  autodescricao?: string;
  sexo_equacao: string;
  data_nascimento: string;
  telefone?: string;
  email?: string;
  status: string;
}

export const ClientesScreen: React.FC = () => {
  const navigate = useNavigate();
  const [clientes, setClientes] = useState<Cliente[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [error, setError] = useState<string | null>(null);

  const loadClientes = async () => {
    try {
      setLoading(true);
      setError(null);
      // GET /api/v1/clientes
      const response = await api.get('/clientes');
      console.log('Clientes carregados:', response.data);
      setClientes(response.data);
    } catch (error: any) {
      console.error('Erro ao carregar clientes:', error);
      setError(error.response?.data?.detail || 'Erro ao carregar lista de clientes');
      setClientes([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadClientes();
  }, []);

  const filteredClientes = clientes.filter(cliente =>
    cliente.nome_completo.toLowerCase().includes(searchTerm.toLowerCase()) ||
    cliente.nome_exibicao?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    cliente.email?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    cliente.id_cliente.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const getInitials = (nome: string) => {
    return nome.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
  };

  const formatDate = (date: string) => {
    return new Date(date).toLocaleDateString('pt-BR');
  };

  const handleDelete = async (id: string, nome: string) => {
    if (window.confirm(`Deseja realmente excluir ${nome}?`)) {
      try {
        // DELETE /api/v1/clientes/{id}
        await api.delete(`/clientes/${id}`);
        loadClientes();
      } catch (error: any) {
        console.error('Erro ao excluir cliente:', error);
        alert(error.response?.data?.detail || 'Erro ao excluir cliente');
      }
    }
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="spinner"></div>
        <p>Carregando clientes...</p>
      </div>
    );
  }

  return (
    <div className="clientes-container">
      <header className="clientes-header">
        <button className="back-button" onClick={() => navigate('/')}>
          <FiArrowLeft size={24} />
        </button>
        <h1 className="header-title">Clientes</h1>
        <button className="btn-primary" onClick={() => navigate('/clientes/novo')}>
          <FiPlus size={20} />
          Novo Cliente
        </button>
      </header>

      {error && (
        <div className="error-banner">
          <p>{error}</p>
          <button onClick={loadClientes} className="retry-button">
            <FiRefreshCw size={16} /> Tentar novamente
          </button>
        </div>
      )}

      <div className="clientes-search">
        <div className="search-box">
          <FiSearch size={20} className="search-icon" />
          <input
            type="text"
            placeholder="Buscar cliente por ID, nome ou email..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
      </div>

      <div className="clientes-list">
        {filteredClientes.length === 0 ? (
          <div className="empty-state">
            <FiUser size={48} />
            <h3>Nenhum cliente encontrado</h3>
            <p>{searchTerm ? 'Tente buscar com outro termo' : 'Comece cadastrando seu primeiro cliente'}</p>
            <button className="btn-primary" onClick={() => navigate('/clientes/novo')}>
              <FiPlus size={20} />
              Cadastrar Cliente
            </button>
          </div>
        ) : (
          filteredClientes.map((cliente) => (
            <div key={cliente.id_cliente} className="cliente-card">
              <div className="cliente-avatar">
                <span>{getInitials(cliente.nome_exibicao || cliente.nome_completo)}</span>
              </div>
              <div className="cliente-info">
                <h3>{cliente.nome_exibicao || cliente.nome_completo}</h3>
                <p className="cliente-id">ID: {cliente.id_cliente}</p>
                {cliente.email && <p className="cliente-email">{cliente.email}</p>}
                {cliente.telefone && <p className="cliente-telefone">{cliente.telefone}</p>}
                <p className="cliente-data">
                  Nascimento: {formatDate(cliente.data_nascimento)} • Status: {cliente.status}
                </p>
              </div>
              <div className="cliente-actions">
                <button 
                  className="btn-icon"
                  onClick={() => navigate(`/clientes/${cliente.id_cliente}/editar`)}
                  title="Editar"
                >
                  <FiEdit2 size={18} />
                </button>
                <button 
                  className="btn-icon btn-danger"
                  onClick={() => handleDelete(cliente.id_cliente, cliente.nome_exibicao || cliente.nome_completo)}
                  title="Excluir"
                >
                  <FiTrash2 size={18} />
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};