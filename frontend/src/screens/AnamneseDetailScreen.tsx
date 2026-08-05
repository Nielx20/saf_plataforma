import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { FiArrowLeft, FiUser, FiCalendar, FiRefreshCw } from 'react-icons/fi';
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
  pronomes?: string;
  identidade_genero?: string;
  sexo_equacao: string;
  data_nascimento: string;
  telefone?: string;
  email?: string;
}

export const AnamneseDetailScreen: React.FC = () => {
  const navigate = useNavigate();
  const { id } = useParams<{ id: string }>();
  const [anamnese, setAnamnese] = useState<Anamnese | null>(null);
  const [cliente, setCliente] = useState<Cliente | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadData();
  }, [id]);

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Buscar anamnese: GET /api/v1/anamneses/{id}
      const anamneseRes = await api.get(`/anamneses/${id}`);
      console.log('Anamnese carregada:', anamneseRes.data);
      setAnamnese(anamneseRes.data);

      // Buscar cliente: GET /api/v1/clientes/{id_cliente}
      const clienteRes = await api.get(`/clientes/${anamneseRes.data.id_cliente}`);
      console.log('Cliente carregado:', clienteRes.data);
      setCliente(clienteRes.data);

    } catch (error: any) {
      console.error('Erro ao carregar detalhes:', error);
      setError(error.response?.data?.detail || 'Erro ao carregar detalhes da anamnese');
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: 'long',
      year: 'numeric'
    });
  };

  const formatDisplayDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    });
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="spinner"></div>
        <p>Carregando detalhes...</p>
      </div>
    );
  }

  if (error || !anamnese || !cliente) {
    return (
      <div className="error-container">
        <p>{error || 'Anamnese não encontrada'}</p>
        <button onClick={() => navigate('/anamnese')} className="btn-primary">
          Voltar para Anamneses
        </button>
      </div>
    );
  }

  return (
    <div className="anamnese-detail-container">
      <header className="detail-header">
        <button className="back-button" onClick={() => navigate('/anamnese')}>
          <FiArrowLeft size={24} />
        </button>
        <h1 className="header-title">Detalhes da Anamnese</h1>
        <div style={{ width: 40 }} />
      </header>

      <div className="detail-content">
        {/* Informações do Cliente */}
        <div className="detail-card">
          <div className="detail-client">
            <div className="client-avatar">
              <span>{cliente.nome_exibicao?.substring(0, 2).toUpperCase() || cliente.nome_completo.substring(0, 2).toUpperCase()}</span>
            </div>
            <div className="client-info">
              <h3>{cliente.nome_exibicao || cliente.nome_completo}</h3>
              <p className="client-detail">
                <FiUser size={14} /> ID: {cliente.id_cliente}
              </p>
              <p className="client-detail">
                <FiCalendar size={14} /> Nascimento: {formatDate(cliente.data_nascimento)}
              </p>
              {cliente.email && <p className="client-detail">📧 {cliente.email}</p>}
              {cliente.telefone && <p className="client-detail">📱 {cliente.telefone}</p>}
            </div>
          </div>
        </div>

        {/* Informações da Anamnese */}
        <div className="detail-info-grid">
          <div className="info-item">
            <label>Data da Anamnese</label>
            <p>{formatDisplayDate(anamnese.data_anamnese)}</p>
          </div>
          <div className="info-item">
            <label>Pratica Atividade Física</label>
            <p>{anamnese.pratica_atividade_fisica ? '✅ Sim' : '❌ Não'}</p>
          </div>
        </div>

        {anamnese.historico_lesoes && (
          <div className="detail-section">
            <h3>Histórico de Lesões</h3>
            <div className="detail-box">
              <p>{anamnese.historico_lesoes}</p>
            </div>
          </div>
        )}

        {anamnese.medicamentos_uso_continuo && (
          <div className="detail-section">
            <h3>Medicamentos em Uso Contínuo</h3>
            <div className="detail-box">
              <p>{anamnese.medicamentos_uso_continuo}</p>
            </div>
          </div>
        )}

        {anamnese.restricoes_medicas && (
          <div className="detail-section">
            <h3>Restrições Médicas</h3>
            <div className="detail-box">
              <p>{anamnese.restricoes_medicas}</p>
            </div>
          </div>
        )}

        {anamnese.observacoes_gerais && (
          <div className="detail-section">
            <h3>Observações Gerais</h3>
            <div className="detail-box">
              <p>{anamnese.observacoes_gerais}</p>
            </div>
          </div>
        )}

        <button 
          className="btn-primary full-width"
          onClick={() => navigate('/anamnese')}
          style={{ marginTop: 20 }}
        >
          Voltar para Lista
        </button>
      </div>
    </div>
  );
};