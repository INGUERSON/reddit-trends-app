import { DragDropContext, DropResult } from '@hello-pangea/dnd';
import { useKanbanStore } from '../store/useKanbanStore';
import { KanbanColumn } from './KanbanColumn';

export function KanbanBoard() {
  const columns = useKanbanStore((state) => state.columns);
  const tasks = useKanbanStore((state) => state.tasks);
  const moveTask = useKanbanStore((state) => state.moveTask);

  const onDragEnd = (result: DropResult) => {
    const { destination, source, draggableId } = result;

    if (!destination) return;

    if (
      destination.droppableId === source.droppableId &&
      destination.index === source.index
    ) {
      return;
    }

    moveTask(draggableId, destination.droppableId, destination.index);
  };

  return (
    <DragDropContext onDragEnd={onDragEnd}>
      <div className="flex gap-6 h-[calc(100vh-140px)] overflow-x-auto overflow-y-hidden pb-4 px-2 items-start custom-scrollbar">
        {columns.map((col) => {
          const columnTasks = tasks.filter((t) => t.columnId === col.id);

          return <KanbanColumn key={col.id} column={col} tasks={columnTasks} />;
        })}
      </div>
    </DragDropContext>
  );
}
