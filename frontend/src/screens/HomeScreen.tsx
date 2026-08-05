import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  FiUsers, 
  FiClipboard, 
  FiCalendar, 
  FiClock, 
  FiPlusCircle, 
  FiUserPlus, 
  FiBell,
  FiChevronRight,
  FiHome,
  FiSettings,
  FiRefreshCw
} from 'react-icons/fi';
import { api } from '../services/api';

interface DashboardStats {
  totalClientes: number;
  totalAnamneses: number;
  anamnesesHoje: number;
  anamnesesPendentes: number;
}

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
  email?: string;
}

export const HomeScreen: React.FC = () => {
  const navigate = useNavigate();
  const [stats, setStats] = useState<DashboardStats>({
    totalClientes: 0,
    totalAnamneses: 0,
    anamnesesHoje: 0,
    anamnesesPendentes: 0,
  });
  const [recentAnamneses, setRecentAnamneses] = useState<Anamnese[]>([]);
  const [clientes, setClientes] = useState<Cliente[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadDashboard = async () => {
    try {
      setLoading(true);
      setError(null);

      // Buscar estatísticas
      const statsResponse = await api.get('/anamneses/dashboard/stats');
      setStats(statsResponse.data);

      // Buscar anamneses recentes (últimas 5)
      const anamnesesResponse = await api.get('/anamneses?limit=5');
      setRecentAnamneses(anamnesesResponse.data);

      // Buscar clientes para mostrar nomes
      const clientesResponse = await api.get('/clientes?limit=100');
      setClientes(clientesResponse.data);

    } catch (error) {
      console.error('Erro ao carregar dashboard:', error);
      setError('Erro ao carregar dados do dashboard');
      
      // Dados mockados para fallback
      setStats({
        totalClientes: 0,
        totalAnamneses: 0,
        anamnesesHoje: 0,
        anamnesesPendentes: 0,
      });
      setRecentAnamneses([]);
      setClientes([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDashboard();
  }, []);

  const getClienteNome = (idCliente: string) => {
    const cliente = clientes.find(c => c.id_cliente === idCliente);
    return cliente?.nome_exibicao || cliente?.nome_completo || idCliente;
  };

  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleDateString('pt-BR');
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Carregando dashboard...</p>
      </div>
    );
  }

  return (
    <div className="home-container">
      {/* Header */}
      <header className="header">
        <div>
          <h1 className="greeting">Olá, Dr. Silva 👋</h1>
          <p className="date">{new Date().toLocaleDateString('pt-BR', {
            day: '2-digit',
            month: 'long',
            year: 'numeric'
          })}</p>
        </div>
        <button className="notification-button">
          <FiBell size={24} />
          <span className="notification-badge">3</span>
        </button>
      </header>

      {error && (
        <div className="error-banner">
          <p>{error}</p>
          <button onClick={loadDashboard} className="retry-button">
            <FiRefreshCw size={16} /> Tentar novamente
          </button>
        </div>
      )}

      {/* Stats Cards */}
      <div className="stats-grid">
        <div className="stat-card blue" onClick={() => navigate('/clientes')} style={{cursor: 'pointer'}}>
          <FiUsers size={24} />
          <span className="stat-number">{stats.totalClientes}</span>
          <span className="stat-label">Clientes</span>
        </div>
        <div className="stat-card green" onClick={() => navigate('/anamnese')} style={{cursor: 'pointer'}}>
          <FiClipboard size={24} />
          <span className="stat-number">{stats.totalAnamneses}</span>
          <span className="stat-label">Total Anamneses</span>
        </div>
      </div>

      <div className="stats-grid">
        <div className="stat-card orange">
          <FiCalendar size={24} />
          <span className="stat-number">{stats.anamnesesHoje}</span>
          <span className="stat-label">Hoje</span>
        </div>
        <div className="stat-card red">
          <FiClock size={24} />
          <span className="stat-number">{stats.anamnesesPendentes}</span>
          <span className="stat-label">Pendentes</span>
        </div>
      </div>

      {/* Quick Actions */}
      <h2 className="section-title">Ações Rápidas</h2>
      <div className="quick-actions">
        <button className="action-button" onClick={() => navigate('/anamnese/nova')}>
          <div className="action-icon blue-bg">
            <FiPlusCircle size={28} />
          </div>
          <span className="action-text">Nova Anamnese</span>
        </button>

        <button className="action-button" onClick={() => navigate('/clientes/novo')}>
          <div className="action-icon green-bg">
            <FiUserPlus size={28} />
          </div>
          <span className="action-text">Novo Cliente</span>
        </button>
      </div>

      {/* Recent Activities */}
      <h2 className="section-title">Últimas Anamneses</h2>
      <div className="activity-list">
        {recentAnamneses.length > 0 ? (
          recentAnamneses.map((item) => (
            <div 
              key={item.id_anamnese} 
              className="activity-item"
              onClick={() => navigate(`/anamnese/${item.id_anamnese}`)}
              style={{cursor: 'pointer'}}
            >
              <div className="activity-icon">
                <FiClipboard size={20} />
              </div>
              <div className="activity-content">
                <p className="activity-title">{getClienteNome(item.id_cliente)}</p>
                <p className="activity-subtitle">
                  Anamnese • {formatDate(item.data_anamnese)}
                  {item.observacoes_gerais && ' • Com observações'}
                </p>
              </div>
              <FiChevronRight size={20} className="activity-arrow" />
            </div>
          ))
        ) : (
          <div className="empty-state">
            <FiClipboard size={48} />
            <p>Nenhuma anamnese recente</p>
          </div>
        )}
      </div>

      {/* Bottom Navigation */}
      <nav className="bottom-nav">
        <button className="nav-item active">
          <FiHome size={24} />
          <span>Início</span>
        </button>
        <button className="nav-item" onClick={() => navigate('/clientes')}>
          <FiUsers size={24} />
          <span>Clientes</span>
        </button>
        <button className="nav-item" onClick={() => navigate('/anamnese')}>
          <FiClipboard size={24} />
          <span>Anamnese</span>
        </button>
        <button className="nav-item">
          <FiSettings size={24} />
          <span>Config</span>
        </button>
      </nav>
    </div>
  );
};