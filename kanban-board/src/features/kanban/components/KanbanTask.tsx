import { Draggable } from '@hello-pangea/dnd';
import { Task } from '../types';
import { useKanbanStore } from '../store/useKanbanStore';
import { Trash2 } from 'lucide-react';

interface Props {
  task: Task;
  index: number;
}

export function KanbanTask({ task, index }: Props) {
  const deleteTask = useKanbanStore((state) => state.deleteTask);

  const priorityColors = {
    low: 'bg-blue-500/20 text-blue-400 border-blue-500/30',
    medium: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30',
    high: 'bg-red-500/20 text-red-400 border-red-500/30',
  };

  return (
    <Draggable draggableId={task.id} index={index}>
      {(provided, snapshot) => (
        <div
          ref={provided.innerRef}
          {...provided.draggableProps}
          {...provided.dragHandleProps}
          className={`group bg-cardBg p-4 rounded-xl border border-gray-700/50 hover:border-gray-500 shadow-sm transition-all duration-200 mb-3 select-none flex flex-col gap-2 ${
            snapshot.isDragging ? 'shadow-xl scale-[1.02] rotate-1 z-50 ring-2 ring-indigo-500/50' : ''
          }`}
          style={provided.draggableProps.style}
        >
          <div className="flex justify-between items-start">
            <h3 className="font-medium text-gray-100 text-base">{task.title}</h3>
            <button
              onClick={() => deleteTask(task.id)}
              className="text-gray-500 hover:text-red-400 opacity-0 group-hover:opacity-100 transition-opacity"
              type="button"
            >
              <Trash2 size={16} />
            </button>
          </div>
          
          {task.description && (
            <p className="text-gray-400 text-sm line-clamp-2 leading-relaxed">
              {task.description}
            </p>
          )}

          <div className="flex items-center gap-2 mt-1">
            <span className={`text-xs px-2.5 py-1 rounded-md border font-medium ${priorityColors[task.priority]}`}>
              {task.priority === 'low' ? 'Baixa' : task.priority === 'medium' ? 'Média' : 'Alta'}
            </span>
            <span className="text-xs text-gray-500 ml-auto font-mono">
              {new Date(task.createdAt).toLocaleDateString('pt-BR', { day: '2-digit', month: 'short' })}
            </span>
          </div>
        </div>
      )}
    </Draggable>
  );
}
