import { Droppable } from '@hello-pangea/dnd';
import { Column, Task } from '../types';
import { KanbanTask } from './KanbanTask';

interface Props {
  column: Column;
  tasks: Task[];
}

export function KanbanColumn({ column, tasks }: Props) {
  return (
    <div className="flex flex-col bg-columnBg w-[340px] rounded-2xl shrink-0 h-full max-h-full overflow-hidden border border-gray-800 shadow-lg">
      <div className="p-4 border-b border-gray-800 flex items-center justify-between bg-columnBg/50 backdrop-blur-sm z-10 sticky top-0">
        <h2 className="font-semibold text-gray-100 flex items-center gap-2">
          {column.title}
          <span className="bg-gray-800 text-gray-400 text-xs px-2.5 py-1 rounded-full font-mono">
            {tasks.length}
          </span>
        </h2>
      </div>

      <Droppable droppableId={column.id} type="TASK">
        {(provided, snapshot) => (
          <div
            ref={provided.innerRef}
            {...provided.droppableProps}
            className={`flex-1 overflow-y-auto overflow-x-hidden p-4 min-h-[150px] transition-colors duration-200 custom-scrollbar ${
              snapshot.isDraggingOver ? 'bg-indigo-900/10' : ''
            }`}
          >
            {tasks.map((task, index) => (
              <KanbanTask key={task.id} task={task} index={index} />
            ))}
            {provided.placeholder}
          </div>
        )}
      </Droppable>
    </div>
  );
}
