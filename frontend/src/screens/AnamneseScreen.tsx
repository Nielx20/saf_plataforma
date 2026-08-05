import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { FiPlus, FiSearch, FiClipboard, FiUser, FiCalendar, FiArrowLeft, FiRefreshCw } from 'react-icons/fi';
import { api } from '../services/api';

interface Anamnese {
  id_anamnese: number;
  id_cliente: string;
  data_anamnese: string;
  pratica_atividade_fisica: boolean;
  historico_lesoes?: string;
  medicamentos_uso_continuo?: string;
  restricoes_medicas?: string;
  observacoes_gerais?: string;
}

interface Cliente {
  id_cliente: string;
  nome_completo: string;
  nome_exibicao?: string;
}

export const AnamneseScreen: React.FC = () => {
  const navigate = useNavigate();
  const [anamneses, setAnamneses] = useState<Anamnese[]>([]);
  const [clientes, setClientes] = useState<Cliente[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [error, setError] = useState<string | null>(null);

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Buscar anamneses: GET /api/v1/anamneses
      const anamnesesRes = await api.get('/anamneses');
      console.log('Anamneses carregadas:', anamnesesRes.data);
      
      // Buscar clientes: GET /api/v1/clientes
      const clientesRes = await api.get('/clientes');
      console.log('Clientes carregados:', clientesRes.data);
      
      setAnamneses(anamnesesRes.data);
      setClientes(clientesRes.data);
    } catch (error: any) {
      console.error('Erro ao carregar dados:', error);
      setError(error.response?.data?.detail || 'Erro ao carregar anamneses');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const getClienteNome = (idCliente: string) => {
    const cliente = clientes.find(c => c.id_cliente === idCliente);
    return cliente?.nome_exibicao || cliente?.nome_completo || idCliente;
  };

  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleDateString('pt-BR');
  };

  const filteredAnamneses = anamneses.filter(a => 
    getClienteNome(a.id_cliente).toLowerCase().includes(searchTerm.toLowerCase()) ||
    a.id_cliente.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) {
    return (
      <div className="loading-container">
        <div className="spinner"></div>
        <p>Carregando anamneses...</p>
      </div>
    );
  }

  return (
    <div className="anamnese-container">
      <header className="anamnese-header">
        <button className="back-button" onClick={() => navigate('/')}>
          <FiArrowLeft size={24} />
        </button>
        <h1 className="header-title">Anamneses</h1>
        <button className="btn-primary" onClick={() => navigate('/anamnese/nova')}>
          <FiPlus size={20} />
          Nova Anamnese
        </button>
      </header>

      {error && (
        <div className="error-banner">
          <p>{error}</p>
          <button onClick={loadData} className="retry-button">
            <FiRefreshCw size={16} /> Tentar novamente
          </button>
        </div>
      )}

      <div className="anamnese-search">
        <div className="search-box">
          <FiSearch size={20} className="search-icon" />
          <input
            type="text"
            placeholder="Buscar por cliente..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
      </div>

      <div className="anamnese-list">
        {filteredAnamneses.length === 0 ? (
          <div className="empty-state">
            <FiClipboard size={48} />
            <h3>Nenhuma anamnese encontrada</h3>
            <p>Comece criando uma nova anamnese</p>
            <button className="btn-primary" onClick={() => navigate('/anamnese/nova')}>
              <FiPlus size={20} />
              Nova Anamnese
            </button>
          </div>
        ) : (
          filteredAnamneses.map((anamnese) => (
            <div 
              key={anamnese.id_anamnese} 
              className="anamnese-card"
              onClick={() => navigate(`/anamnese/${anamnese.id_anamnese}`)}
            >
              <div className="anamnese-info">
                <div className="anamnese-cliente">
                  <FiUser size={18} />
                  <h3>{getClienteNome(anamnese.id_cliente)}</h3>
                </div>
                <div className="anamnese-meta">
                  <span className="anamnese-date">
                    <FiCalendar size={14} />
                    {formatDate(anamnese.data_anamnese)}
                  </span>
                  <span className={`anamnese-status ${anamnese.observacoes_gerais ? 'completed' : 'pending'}`}>
                    {anamnese.observacoes_gerais ? '✓ Completa' : '⏳ Pendente'}
                  </span>
                </div>
                {anamnese.observacoes_gerais && (
                  <p className="anamnese-obs">{anamnese.observacoes_gerais.substring(0, 100)}...</p>
                )}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};