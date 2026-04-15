import { Plus } from 'lucide-react';
import { useState } from 'react';
import { KanbanBoard } from './features/kanban/components/KanbanBoard';
import { useKanbanStore } from './features/kanban/store/useKanbanStore';
import { Priority } from './features/kanban/types';

function App() {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [priority, setPriority] = useState<Priority>('medium');
  const addTask = useKanbanStore((state) => state.addTask);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;
    
    addTask({
      title,
      description,
      priority,
      columnId: 'todo', // adds to the first column by default
    });

    setTitle('');
    setDescription('');
    setPriority('medium');
    setIsModalOpen(false);
  };

  return (
    <div className="min-h-screen bg-boardBg text-white selection:bg-indigo-500/30">
      <header className="px-8 py-6 mb-2 border-b border-gray-800 bg-boardBg/80 backdrop-blur-md sticky top-0 z-20 flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent">
            Workspace Kanban
          </h1>
          <p className="text-gray-400 text-sm mt-1">Gerencie suas tarefas com eficiência</p>
        </div>
        <button 
          onClick={() => setIsModalOpen(true)}
          className="bg-indigo-600 hover:bg-indigo-500 text-white px-4 py-2.5 rounded-lg flex items-center gap-2 font-medium transition-all shadow-lg shadow-indigo-600/20 active:scale-95"
        >
          <Plus size={20} />
          Nova Tarefa
        </button>
      </header>
      
      <main className="px-6 py-4">
        <KanbanBoard />
      </main>

      {/* Modal Simplificadíssimo para criação */}
      {isModalOpen && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4 transition-opacity">
          <div className="bg-cardBg w-full max-w-md rounded-2xl shadow-2xl border border-gray-700 overflow-hidden animate-in fade-in zoom-in-95 duration-200">
            <div className="px-6 py-4 border-b border-gray-800 bg-columnBg/50 flex justify-between items-center">
              <h2 className="text-xl font-semibold">Criar Nova Tarefa</h2>
              <button 
                onClick={() => setIsModalOpen(false)}
                className="text-gray-400 hover:text-white transition-colors"
                type="button"
              >
                ✕
              </button>
            </div>
            
            <form onSubmit={handleSubmit} className="p-6 flex flex-col gap-5">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-1.5">Título da Tarefa *</label>
                <input 
                  autoFocus
                  type="text" 
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  className="w-full bg-columnBg border border-gray-700 rounded-lg px-4 py-2.5 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
                  placeholder="Ex: Refatorar API de login"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-1.5">Descrição</label>
                <textarea 
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  className="w-full bg-columnBg border border-gray-700 rounded-lg px-4 py-2.5 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all min-h-[100px] resize-y"
                  placeholder="Adicione mais detalhes (opcional)"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-1.5">Prioridade</label>
                <div className="flex gap-3">
                  {(['low', 'medium', 'high'] as const).map((p) => (
                    <button
                      key={p}
                      type="button"
                      onClick={() => setPriority(p)}
                      className={`flex-1 py-2 rounded-lg text-sm font-medium border transition-all ${
                        priority === p 
                          ? p === 'low' ? 'bg-blue-500/20 text-blue-400 border-blue-500' :
                            p === 'medium' ? 'bg-yellow-500/20 text-yellow-400 border-yellow-500' :
                            'bg-red-500/20 text-red-400 border-red-500'
                          : 'bg-columnBg border-gray-700 text-gray-400 hover:border-gray-500'
                      }`}
                    >
                      {p === 'low' ? 'Baixa' : p === 'medium' ? 'Média' : 'Alta'}
                    </button>
                  ))}
                </div>
              </div>

              <div className="mt-4 flex gap-3">
                <button 
                  type="button"
                  onClick={() => setIsModalOpen(false)}
                  className="flex-1 px-4 py-2.5 rounded-lg font-medium bg-transparent border border-gray-700 text-gray-300 hover:bg-gray-800 transition-colors"
                >
                  Cancelar
                </button>
                <button 
                  type="submit"
                  disabled={!title.trim()}
                  className="flex-1 px-4 py-2.5 rounded-lg font-medium bg-indigo-600 text-white hover:bg-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors shadow-lg shadow-indigo-600/20"
                >
                  Criar Tarefa
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
