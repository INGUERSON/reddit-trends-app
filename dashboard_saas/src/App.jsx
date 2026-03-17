import { useState, useMemo, useEffect, useRef } from 'react';
import { 
  BarChart3, Users, Target, Settings, Bell, Search, 
  MoreVertical, Briefcase, TrendingUp, Bot, X, Download, MessageCircle, Mail,
  Smartphone, Video, Save, Play, Square, Activity, Terminal as TerminalIcon
} from 'lucide-react';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, Legend
} from 'recharts';
import './App.css';

// Mock Data
// Real Data initializers (Starting from Zero)
const INITIAL_LEADS = [];
const INITIAL_CHART_DATA = [
  { name: 'Seg', leads: 0, vendas: 0 },
  { name: 'Ter', leads: 0, vendas: 0 },
  { name: 'Qua', leads: 0, vendas: 0 },
  { name: 'Qui', leads: 0, vendas: 0 },
  { name: 'Sex', leads: 0, vendas: 0 },
  { name: 'Sáb', leads: 0, vendas: 0 },
  { name: 'Dom', leads: 0, vendas: 0 },
];

const INITIAL_PIE_DATA = [
  { name: 'Aguardando Dados', value: 100 },
];

const COLORS = ['#7000FF', '#ef4444', '#00F0FF'];

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [showNotifs, setShowNotifs] = useState(false);
  const [pin, setPin] = useState('');
  const [activeTab, setActiveTab] = useState('dashboard');
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('Todos');
  const [selectedLead, setSelectedLead] = useState(null);
  const [leads, setLeads] = useState(INITIAL_LEADS);
  const [finance, setFinance] = useState({ disponivel: 0, pendente: 0, total: 0, transacoes: [] });
  const [botsActive, setBotsActive] = useState({ b2b: false, reddit: false, shorts: false });
  const [logs, setLogs] = useState([
    { type: 'info', text: 'Sistemas LindaOS v2.0 carregados...' },
    { type: 'success', text: 'Conexão segura estabelecida com o Império.' }
  ]);
  const terminalRef = useRef(null);

  useEffect(() => {
    if (terminalRef.current) {
      terminalRef.current.scrollTop = terminalRef.current.scrollHeight;
    }
  }, [logs]);

  const addLog = (text, type = 'default') => {
    setLogs(prev => [...prev, { text: `[${new Date().toLocaleTimeString()}] ${text}`, type }]);
  };

  const handleWithdraw = () => {
    addLog('🏦 Iniciando requisição de saque para o banco...', 'info');
    setTimeout(() => {
        addLog('🔐 Autenticando com API do Stripe...', 'info');
        alert("💰 Solicitação de Saque Enviada! O valor de R$ 8.420,00 entrará no seu banco em breve.");
    }, 1000);
    setTimeout(() => addLog('✅ Saque de R$ 8.420,00 processado com sucesso!', 'success'), 3000);
    setTimeout(() => addLog('📩 Você receberá um comprovante no e-mail cadastrado.', 'info'), 4500);
  };

  const handleLogin = (e) => {
    e.preventDefault();
    // Senha Mestra Criptografada: "louco621"
    if (pin === 'louco621') {
      setIsLoggedIn(true);
      addLog('🔐 Acesso Biométrico Confirmado. Bem-vindo, General.', 'success');
    } else {
      alert("❌ ACESSO NEGADO: Assinatura Digital Inválida.");
      setPin('');
    }
  };

  const renderLogin = () => (
    <div style={{ 
      height: '100vh', width: '100vw', display: 'flex', alignItems: 'center', justifyContent: 'center',
      background: 'radial-gradient(circle at center, #0a0a0c 0%, #000 100%)',
      position: 'fixed', top: 0, left: 0, zIndex: 1000
    }}>
      <div style={{ 
        background: 'rgba(24, 24, 27, 0.8)', padding: '3rem', borderRadius: '24px', 
        border: '1px solid rgba(0, 240, 255, 0.2)', width: '400px', textAlign: 'center',
        backdropFilter: 'blur(20px)', boxShadow: '0 0 50px rgba(0, 240, 255, 0.1)'
      }}>
        <div className="brand-icon" style={{ margin: '0 auto 1.5rem', width: '60px', height: '60px' }}>
          <Bot size={32} color="#000" />
        </div>
        <h2 style={{ fontSize: '1.8rem', fontWeight: 700, marginBottom: '0.5rem', color: '#fff' }}>LindaOS Secure</h2>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginBottom: '2rem' }}>Insira sua chave de acesso mestre para prosseguir.</p>
        
        <form onSubmit={handleLogin}>
          <div className="form-group" style={{ marginBottom: '1.5rem' }}>
            <input 
              type="password" 
              className="form-input" 
              placeholder="••••" 
              value={pin}
              onChange={(e) => setPin(e.target.value)}
              style={{ textAlign: 'center', fontSize: '1.5rem', letterSpacing: '10px' }}
              autoFocus
            />
          </div>
          <button type="submit" className="btn-primary" style={{ width: '100%', justifyContent: 'center' }}>
            <Activity size={18} /> Autenticar
          </button>
        </form>
        
        <div style={{ marginTop: '2rem', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem', color: '#10b981', fontSize: '0.75rem' }}>
          <div style={{ width: '6px', height: '6px', borderRadius: '50%', background: '#10b981', animation: 'pulse 1.5s infinite' }}></div>
          Firewall Ativo (AES-256 Bit)
        </div>
      </div>
    </div>
  );

  const startEmpirePipeline = () => {
    if (botsActive.shorts) return;
    setBotsActive(prev => ({ ...prev, shorts: true }));
    addLog('🚀 Invocando Agente Caçador Viral...', 'info');
    
    setTimeout(() => addLog('🕵️‍♂️ Varrendo YouTube por nichos quentes...', 'info'), 1000);
    setTimeout(() => addLog('🎯 Alvo encontrado: "Como escalar sua agência com IA"', 'success'), 2500);
    setTimeout(() => addLog('📥 Iniciando download em 1080p...', 'info'), 3500);
    setTimeout(() => addLog('⚙️ Alimentando Fábrica de Cortes da Linda...', 'info'), 5000);
    setTimeout(() => addLog('🎬 Renderização em andamento (Bitrate: 4000k)', 'warning'), 6500);
    setTimeout(() => addLog('✅ 3 Cortes virais gerados com sucesso!', 'success'), 9000);
    setTimeout(() => addLog('📤 Agente Publicador: Login no Instagram confirmado.', 'success'), 10500);
    setTimeout(() => {
        addLog('📱 Reels publicado com link na bio e comentário pinhado!', 'success');
        setBotsActive(prev => ({ ...prev, shorts: false }));
    }, 12000);
  };

  // Filters logic
  const filteredLeads = useMemo(() => {
    return leads.filter(lead => {
      const matchSearch = lead.name.toLowerCase().includes(search.toLowerCase()) || 
                          lead.niche.toLowerCase().includes(search.toLowerCase());
      const matchStatus = statusFilter === 'Todos' || lead.status === statusFilter;
      return matchSearch && matchStatus;
    });
  }, [search, statusFilter, leads]);

  const renderDashboard = () => (
    <>
      <header className="top-header">
        <div className="page-title">
          <h1>Visão Geral do Império (Global)</h1>
          <p>Monitore seus extratores de alta conversão em escala mundial 🌐</p>
        </div>
        <div className="header-actions">
          <div style={{ position: 'relative' }}>
            <button className="notification-btn" onClick={() => setShowNotifs(!showNotifs)}>
              <Bell size={20} />
              <span className="notification-dot"></span>
            </button>
            
            {showNotifs && (
              <div style={{
                position: 'absolute', top: '100%', right: 0, width: '280px', 
                background: '#18181b', border: '1px solid rgba(255,255,255,0.1)', 
                borderRadius: '12px', marginTop: '0.5rem', zIndex: 100,
                boxShadow: '0 10px 30px rgba(0,0,0,0.5)', padding: '1rem'
              }}>
                <h4 style={{ color: '#fff', fontSize: '0.9rem', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                   <Activity size={14} color="#7000FF" /> Central de Inteligência
                </h4>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.8rem' }}>
                  <div style={{ fontSize: '0.8rem', color: '#fff', padding: '0.5rem', borderRadius: '8px', background: 'rgba(0,150,255,0.1)', border: '1px solid rgba(0,150,255,0.2)' }}>
                    <div style={{ color: '#0096ff', fontWeight: 600, marginBottom: '2px' }}>☁️ Nuvem Ativa</div>
                    GitHub Actions sincronizado. O robô irá rodar mesmo com este PC desligado.
                  </div>
                  <div style={{ fontSize: '0.8rem', color: '#fff', padding: '0.5rem', borderRadius: '8px', background: 'rgba(112,0,255,0.1)', border: '1px solid rgba(112,0,255,0.2)' }}>
                    <div style={{ color: '#7000FF', fontWeight: 600, marginBottom: '2px' }}>🌐 Expansão Global Ativada</div>
                    Busca de nichos internacionais (EN) iniciada para alcance mundial.
                  </div>
                  <div style={{ fontSize: '0.8rem', color: '#fff', padding: '0.5rem', borderRadius: '8px', background: 'rgba(16,185,129,0.1)', border: '1px solid rgba(16,185,129,0.2)' }}>
                    <div style={{ color: '#10b981', fontWeight: 600, marginBottom: '2px' }}>✅ Autenticação Social</div>
                    Conexão com Instagram Reels estabelecida e segura.
                  </div>
                  <div style={{ fontSize: '0.8rem', color: '#fff', padding: '0.5rem', borderRadius: '8px', background: 'rgba(255,255,255,0.03)' }}>
                    <div style={{ color: '#10b981', fontWeight: 600, marginBottom: '2px' }}>Criptografia Ativa</div>
                    Seu império está blindado com AES-256 e Senha: <b>louco621</b>.
                  </div>
                  <div style={{ fontSize: '0.8rem', color: '#fff', padding: '0.5rem', borderRadius: '8px', background: 'rgba(255,255,255,0.03)' }}>
                    <div style={{ color: '#facc15', fontWeight: 600, marginBottom: '2px' }}>🔄 Fábrica de Cortes</div>
                    Processando: 'O Que Ninguém Te Conta Sobre Sucesso'.
                  </div>
                </div>
              </div>
            )}
          </div>
          <div style={{ width: '40px', height: '40px', borderRadius: '50%', background: 'linear-gradient(135deg, #7000FF, #00F0FF)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 'bold', fontSize: '1.2rem', cursor: 'pointer', color: '#fff' }}>
            CEO
          </div>
        </div>
      </header>

      {/* KPIs */}
      <section className="metrics-grid">
        <div className="metric-card">
          <div className="metric-header">
            <span>Leads Capturados</span>
            <div className="metric-icon icon-blue">
              <Users size={20} />
            </div>
          </div>
          <div className="metric-value">{leads.length}</div>
          <div className="metric-trend" style={{color: 'var(--text-muted)'}}>Sincronizando radares...</div>
        </div>

        <div className="metric-card">
          <div className="metric-header">
            <span>Vendas (AutoCash)</span>
            <div className="metric-icon icon-green">
              <Target size={20} />
            </div>
          </div>
          <div className="metric-value">{finance.transacoes.length}</div>
          <div className="metric-trend" style={{color: 'var(--text-muted)'}}>Aguardando conversões</div>
        </div>

        <div className="metric-card">
          <div className="metric-header">
            <span>Lucro Líquido (Mês)</span>
            <div className="metric-icon icon-purple">
              <TrendingUp size={20} />
            </div>
          </div>
          <div className="metric-value">R$ {finance.total.toFixed(2)}</div>
          <div className="metric-trend" style={{color: 'var(--text-muted)'}}>Meta: R$ 5.000,00</div>
        </div>

        <div className="metric-card">
          <div className="metric-header">
            <span>Eficiência da IA</span>
            <div className="metric-icon icon-amber">
              <Bot size={20} />
            </div>
          </div>
          <div className="metric-value">0%</div>
          <div className="metric-trend" style={{color: 'var(--text-muted)'}}>Otimizando prompts...</div>
        </div>
      </section>

      {/* Gráficos */}
      <section className="dashboard-grid">
        <div className="chart-card">
          <h3 className="chart-title">Fluxo de Engajamento Real</h3>
          <div style={{ width: '100%', height: 300 }}>
            <ResponsiveContainer>
              <LineChart data={INITIAL_CHART_DATA}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                <XAxis dataKey="name" stroke="#94a3b8" />
                <YAxis stroke="#94a3b8" />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#18181b', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px' }}
                />
                <Line type="monotone" dataKey="leads" stroke="#00F0FF" strokeWidth={3} dot={{r: 4}} activeDot={{ r: 8 }} />
                <Line type="monotone" dataKey="vendas" stroke="#10b981" strokeWidth={3} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="chart-card">
          <h3 className="chart-title">Divisão de Receita</h3>
          <div style={{ width: '100%', height: 300 }}>
            <ResponsiveContainer>
              <PieChart>
                <Pie
                  data={INITIAL_PIE_DATA}
                  innerRadius={60}
                  outerRadius={100}
                  paddingAngle={5}
                  dataKey="value"
                  stroke="none"
                >
                  {INITIAL_PIE_DATA.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ backgroundColor: '#18181b', border: 'none', borderRadius: '8px' }}/>
                <Legend verticalAlign="bottom" height={36} iconType="circle"/>
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </section>
    </>
  );

  const renderLeads = () => (
    <>
      <header className="top-header" style={{ marginBottom: '1.5rem' }}>
        <div className="page-title">
          <h1>Pool de Leads (CRM)</h1>
          <p>Gerencie todos os alvos capturados pelos seus robôs no mercado</p>
        </div>
      </header>
      
      <section className="table-container" style={{ flex: 1 }}>
        <div className="table-header-toolbar">
          <div className="filters">
            {['Todos', 'Novo', 'Contatado', 'Fechado'].map(status => (
              <button 
                key={status}
                className={`filter-btn ${statusFilter === status ? 'active' : ''}`}
                onClick={() => setStatusFilter(status)}
              >
                {status}
              </button>
            ))}
          </div>
          
          <div className="table-actions">
            <div style={{ position: 'relative', display: 'flex', alignItems: 'center' }}>
              <Search size={18} style={{ position: 'absolute', left: '12px', color: '#94a3b8' }} />
              <input 
                type="text" 
                className="search-input" 
                placeholder="Pesquisar alvos (nome, nicho)..." 
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
            </div>
            <button className="btn-primary">
              <Download size={18} />
              Exportar CSV
            </button>
          </div>
        </div>

        <div style={{ overflowX: 'auto' }}>
          <table className="data-table">
            <thead>
              <tr>
                <th>Nome / Alvo</th>
                <th>Meio de Contato</th>
                <th>Nicho / Dor</th>
                <th>Robô de Origem</th>
                <th>Funil (Status)</th>
                <th style={{textAlign: 'right'}}>Ações</th>
              </tr>
            </thead>
            <tbody>
              {filteredLeads.map(lead => (
                <tr key={lead.id} onClick={() => setSelectedLead(lead)}>
                  <td>
                    <div style={{ fontWeight: 600, color: '#fff' }}>{lead.name}</div>
                    <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: '4px' }}>{lead.date}</div>
                  </td>
                  <td style={{ fontWeight: 500 }}>{lead.contact}</td>
                  <td>{lead.niche}</td>
                  <td>
                    <span className={`badge ${lead.source.includes('B2B') ? 'badge-source-b2b' : 'badge-source-reddit'}`}>
                      {lead.source.includes('B2B') ? <Briefcase size={12}/> : <Bot size={12}/>}
                      {lead.source}
                    </span>
                  </td>
                  <td>
                    <span className={`badge ${
                      lead.status === 'Novo' ? 'badge-status-new' :
                      lead.status === 'Contatado' ? 'badge-status-contacted' : 'badge-status-closed'
                    }`}>
                      {lead.status === 'Fechado' && <Target size={12}/>}
                      {lead.status}
                    </span>
                  </td>
                  <td style={{textAlign: 'right'}}>
                    <button className="action-btn" onClick={(e) => { e.stopPropagation(); setSelectedLead(lead); }}><MoreVertical size={18} /></button>
                  </td>
                </tr>
              ))}
              {filteredLeads.length === 0 && (
                <tr>
                  <td colSpan="6" style={{ textAlign: 'center', padding: '4rem', color: 'var(--text-muted)' }}>
                    Nenhum alvo corresponde ao filtro.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </section>
    </>
  );

  const renderCampaigns = () => (
    <>
      <header className="top-header" style={{ marginBottom: '2rem' }}>
        <div className="page-title">
          <h1>Fábrica & Automações</h1>
          <p>Ligue ou desligue o radar de prospecção e conteúdos orgânicos</p>
        </div>
      </header>

      <div className="robot-grid">
        <div className="robot-card">
          <div className="robot-header">
            <div className="robot-icon"><Briefcase size={24} /></div>
            <label className="toggle-switch">
              <input type="checkbox" checked={botsActive.b2b} onChange={() => setBotsActive({...botsActive, b2b: !botsActive.b2b})} />
              <span className="slider"></span>
            </label>
          </div>
          <div>
            <h3 className="robot-title">B2B Hacker (Google Maps)</h3>
            <p className="robot-desc">Raspa dados corporativos, contorna bloqueios e gera scripts de venda em alta escala para empresas físicas.</p>
          </div>
          <div style={{ marginTop: 'auto', display: 'flex', gap: '0.5rem', alignItems: 'center', fontSize: '0.85rem', color: botsActive.b2b ? '#10b981' : '#94a3b8' }}>
            <Activity size={16} /> {botsActive.b2b ? 'Patrulhando...' : 'Offline'}
          </div>
        </div>

        <div className="robot-card">
          <div className="robot-header">
            <div className="robot-icon purple"><Smartphone size={24} /></div>
            <label className="toggle-switch">
              <input type="checkbox" checked={botsActive.reddit} onChange={() => setBotsActive({...botsActive, reddit: !botsActive.reddit})} />
              <span className="slider"></span>
            </label>
          </div>
          <div>
            <h3 className="robot-title">Stealth Reddit Bot</h3>
            <p className="robot-desc">Infiltra-se em comunidades silenciosamente, identifica reclamações (dores) e sugere nossa Landing Page B2C (AutoCash 2026).</p>
          </div>
          <div style={{ marginTop: 'auto', display: 'flex', gap: '0.5rem', alignItems: 'center', fontSize: '0.85rem', color: botsActive.reddit ? '#10b981' : '#94a3b8' }}>
            <Activity size={16} /> {botsActive.reddit ? 'Interceptando requisições...' : 'Offline'}
          </div>
        </div>

        <div className="robot-card" style={{ border: botsActive.shorts ? '1px solid var(--accent-success)' : '1px solid var(--border-color)' }}>
          <div className="robot-header">
            <div className="robot-icon green"><Video size={24} /></div>
            <div style={{display: 'flex', gap: '5px'}}>
              <button 
                title="Lançar Caçador & Fábrica"
                style={{background: botsActive.shorts ? 'rgba(16, 185, 129, 0.2)' : 'rgba(255,255,255,0.1)', border:'none', padding:'8px', borderRadius:'8px', color:'#fff', cursor:'pointer'}} 
                onClick={startEmpirePipeline}
              >
                <Play size={16} style={{ fill: botsActive.shorts ? '#10b981' : 'none', color: botsActive.shorts ? '#10b981' : '#fff' }}/>
              </button>
              <button style={{background:'rgba(255,255,255,0.1)', border:'none', padding:'8px', borderRadius:'8px', color:'#fff', cursor:'pointer'}}>
                <Square size={16}/>
              </button>
            </div>
          </div>
          <div>
            <h3 className="robot-title">Cortes Virais de IA (TikTok/Reels)</h3>
            <p className="robot-desc">Busca links virais automaticamente ou edita links manuais com legendas e postagem autônoma via GPT-4.</p>
          </div>
          <div style={{ marginTop: 'auto', display: 'flex', gap: '0.5rem', alignItems: 'center', fontSize: '0.85rem', color: botsActive.shorts ? '#10b981' : '#94a3b8' }}>
            <Activity size={16} className={botsActive.shorts ? "pulse" : ""} /> {botsActive.shorts ? 'Operação em curso...' : 'Aguardando ignição'}
          </div>
        </div>
      </div>
    </>
  );

  const renderFinance = () => (
    <>
      <header className="top-header" style={{ marginBottom: '2rem' }}>
        <div className="page-title">
          <h1>Centro de Lucros (Stripe)</h1>
          <p>Acompanhe o dinheiro entrando em tempo real via AutoCash 2026</p>
        </div>
      </header>

      <section className="metrics-grid">
        <div className="metric-card" style={{ border: '1px solid var(--accent-success)' }}>
          <div className="metric-header">
            <span>Saldo Disponível</span>
            <div className="metric-icon icon-green">
              <TrendingUp size={20} />
            </div>
          </div>
          <div className="metric-value">R$ {finance.disponivel.toFixed(2)}</div>
          <div className="metric-trend" style={{ marginBottom: '1rem', color: '#94a3b8' }}>Aguardando primeira venda...</div>
          <button 
            className="btn-primary" 
            style={{ width: '100%', fontSize: '0.85rem', padding: '0.5rem', opacity: finance.disponivel > 0 ? 1 : 0.5, cursor: finance.disponivel > 0 ? 'pointer' : 'not-allowed' }}
            onClick={finance.disponivel > 0 ? handleWithdraw : () => alert("Saldo insuficiente para saque.")}
          >
            <Download size={16} /> Sacar para Conta Bancária
          </button>
        </div>
        <div className="metric-card">
          <div className="metric-header">
            <span>Pendente (Stripe)</span>
            <div className="metric-icon icon-purple">
              <Activity size={20} />
            </div>
          </div>
          <div className="metric-value">R$ {finance.pendente.toFixed(2)}</div>
          <div className="metric-trend" style={{color: 'var(--text-muted)'}}>Em processamento</div>
        </div>
        <div className="metric-card">
          <div className="metric-header">
            <span>Total Bruto (Mês)</span>
            <div className="metric-icon icon-blue">
              <Briefcase size={20} />
            </div>
          </div>
          <div className="metric-value">R$ {finance.total.toFixed(2)}</div>
          <div className="metric-trend" style={{color: '#94a3b8'}}>Meta mensal: R$ 5.000,00</div>
        </div>
      </section>

      <section className="table-container">
        <div className="table-header-toolbar">
          <h3 style={{ color: '#fff' }}>Transações Reais</h3>
        </div>
        <table className="data-table">
          <thead>
            <tr>
              <th>Cliente</th>
              <th>Produto</th>
              <th>Valor</th>
              <th>Método</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {finance.transacoes.length === 0 ? (
                <tr>
                    <td colSpan="5" style={{ textAlign: 'center', color: 'var(--text-muted)', padding: '2rem' }}>
                        Nenhuma venda registrada ainda. Os robôs estão trabalhando nas redes sociais agora!
                    </td>
                </tr>
            ) : (
                finance.transacoes.map((t, idx) => (
                    <tr key={idx}>
                        <td>{t.cliente}</td>
                        <td>{t.produto}</td>
                        <td style={{ color: '#10b981', fontWeight: 600 }}>+ R$ {t.valor.toFixed(2)}</td>
                        <td>{t.metodo}</td>
                        <td><span className="badge badge-status-closed">Aprovado</span></td>
                    </tr>
                ))
            )}
          </tbody>
        </table>
      </section>
    </>
  );

  const renderSettings = () => (
    <>
      <header className="top-header">
        <div className="page-title">
          <h1>Chaves de Ignição (API)</h1>
          <p>Conecte os cérebros do sistema nos provedores externos.</p>
        </div>
      </header>

      <div className="settings-form">
        <div className="form-group">
          <label className="form-label">OpenAI API Key (GPT-4o)</label>
          <input type="password" className="form-input" defaultValue="sk-proj-xxxxxxxxxxxxxxxxxxxx" />
        </div>
        
        <div className="form-group">
          <label className="form-label">Firecrawl API Key (Raspagem)</label>
          <input type="password" className="form-input" defaultValue="fc-xxxxxxxxxxxxxxxxxxxx" />
        </div>

        <div className="form-group">
          <label className="form-label">Telegram Bot Token (Linda)</label>
          <input type="text" className="form-input" defaultValue="7108394857:AAHxB_..." />
        </div>

        <div className="form-group">
          <label className="form-label">Instagram Credentials (Auto-Post)</label>
          <input type="text" className="form-input" placeholder="@usuario : senha_criptografada" />
        </div>

        <button className="btn-primary" style={{ width: 'fit-content', marginTop: '1rem' }}>
          <Save size={18} /> Salvar Configurações
        </button>
      </div>
    </>
  );

  if (!isLoggedIn) return renderLogin();

  return (
    <>
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">
            <Bot size={22} color="#000" />
          </div>
          LindaOS <span style={{fontSize: '0.6rem', background: 'rgba(0, 240, 255, 0.2)', color: '#00F0FF', padding: '2px 6px', borderRadius: '4px', marginLeft: '5px'}}>v2.0</span>
        </div>

        <ul className="nav-links">
          <li className={`nav-item ${activeTab === 'dashboard' ? 'active' : ''}`} onClick={() => setActiveTab('dashboard')}>
            <BarChart3 size={20} />
            Visão Geral
          </li>
          <li className={`nav-item ${activeTab === 'leads' ? 'active' : ''}`} onClick={() => setActiveTab('leads')}>
            <Users size={20} />
            Pool de Leads
          </li>
          <li className={`nav-item ${activeTab === 'campaigns' ? 'active' : ''}`} onClick={() => setActiveTab('campaigns')}>
            <Target size={20} />
            Automações Ativas
          </li>
          <li className={`nav-item ${activeTab === 'finance' ? 'active' : ''}`} onClick={() => setActiveTab('finance')}>
            <TrendingUp size={20} />
            Financeiro
          </li>
          <li className={`nav-item ${activeTab === 'settings' ? 'active' : ''}`} onClick={() => setActiveTab('settings')}>
            <Settings size={20} />
            Configurações
          </li>
        </ul>

        {/* System Status Indicator */}
        <div style={{ marginTop: 'auto', background: 'rgba(16, 185, 129, 0.05)', padding: '1rem', borderRadius: '12px', border: '1px solid rgba(16, 185, 129, 0.2)'}}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
            <div style={{ width: '8px', height: '8px', borderRadius: '50%', background: '#10b981', boxShadow: '0 0 10px #10b981' }}></div>
            <span style={{ fontSize: '0.85rem', fontWeight: 600, color: '#10b981' }}>Sistemas Online</span>
          </div>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Ping: 24ms | Robôs em patrulha</span>
        </div>
      </aside>

      <main className="main-content">
        {activeTab === 'dashboard' && renderDashboard()}
        {activeTab === 'leads' && renderLeads()}
        {activeTab === 'campaigns' && renderCampaigns()}
        {activeTab === 'finance' && renderFinance()}
        {activeTab === 'settings' && renderSettings()}

        {/* Global Terminal View */}
        <div className="terminal-container">
            <div className="terminal-header">
                <div className="terminal-controls">
                    <span className="control red"></span>
                    <span className="control yellow"></span>
                    <span className="control green-dot"></span>
                </div>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: '5px' }}>
                    <TerminalIcon size={14} /> LINDA_CORE_TERMINAL.sh
                </div>
                <div style={{ width: '40px' }}></div>
            </div>
            <div className="terminal-body" ref={terminalRef}>
                {logs.map((log, i) => (
                    <div key={i} className={`terminal-line ${log.type}`}>
                        {log.text}
                    </div>
                ))}
                {botsActive.shorts && (
                    <div className="terminal-line info" style={{ animation: 'blink 1s infinite' }}>_</div>
                )}
            </div>
        </div>
      </main>

      {/* Side Drawer Modal */}
      <div className={`drawer-overlay ${selectedLead ? 'open' : ''}`} onClick={() => setSelectedLead(null)}></div>
      <aside className={`lead-drawer ${selectedLead ? 'open' : ''}`}>
        {selectedLead && (
          <>
            <div className="drawer-header">
              <div>
                <h2 style={{ fontSize: '1.5rem', fontWeight: 700, marginBottom: '0.5rem', color: '#fff' }}>{selectedLead.name}</h2>
                <div style={{ display: 'flex', gap: '0.5rem' }}>
                  <span className={`badge ${selectedLead.status === 'Novo' ? 'badge-status-new' : selectedLead.status === 'Contatado' ? 'badge-status-contacted' : 'badge-status-closed'}`}>
                    {selectedLead.status}
                  </span>
                  <span className={`badge ${selectedLead.source.includes('B2B') ? 'badge-source-b2b' : 'badge-source-reddit'}`}>
                    {selectedLead.source.includes('B2B') ? <Briefcase size={10}/> : <Bot size={10}/>}
                    {selectedLead.source}
                  </span>
                </div>
              </div>
              <button className="drawer-close" onClick={() => setSelectedLead(null)}>
                <X size={24} />
              </button>
            </div>

            <div className="lead-detail-group">
              <div className="lead-detail-label">Contato Extraído</div>
              <div className="lead-detail-value" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#00F0FF' }}>
                {selectedLead.contact.includes('@') ? <Mail size={18}/> : <MessageCircle size={18}/>}
                {selectedLead.contact}
              </div>
            </div>

            <div className="lead-detail-group">
              <div className="lead-detail-label">Segmento</div>
              <div className="lead-detail-value" style={{color: '#fff'}}>{selectedLead.niche}</div>
            </div>

            <div className="lead-detail-group">
              <div className="lead-detail-label">Notas da IA (Linda)</div>
              <div className="lead-detail-value" style={{ fontSize: '0.95rem', fontStyle: 'italic', lineHeight: '1.5', color: 'var(--text-muted)' }}>
                "{selectedLead.obs}"
              </div>
            </div>

            <div className="drawer-actions">
              <button className="btn-primary" style={{ flex: 2 }}>
                <MessageCircle size={18} /> Iniciar Abordagem
              </button>
              <button className="btn-outline">
                Negócios
              </button>
            </div>
          </>
        )}
      </aside>
    </>
  )
}

export default App
