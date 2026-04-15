import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { KanbanState } from '../types';
import { v4 as uuidv4 } from 'uuid';

export const useKanbanStore = create<KanbanState>()(
  persist(
    (set) => ({
      columns: [
        { id: 'todo', title: 'A Fazer' },
        { id: 'doing', title: 'Em Progresso' },
        { id: 'done', title: 'Concluído' },
      ],
      tasks: [],

      addTask: (taskData) => set((state) => ({
        tasks: [...state.tasks, { ...taskData, id: uuidv4(), createdAt: Date.now() }]
      })),

      moveTask: (taskId, newColumnId, newIndex) => set((state) => {
        const newTasks = [...state.tasks];
        const taskIndex = newTasks.findIndex(t => t.id === taskId);
        if (taskIndex === -1) return state;

        const [movedTask] = newTasks.splice(taskIndex, 1);
        movedTask.columnId = newColumnId;
        newTasks.splice(newIndex, 0, movedTask);
        
        return { tasks: newTasks };
      }),

      deleteTask: (taskId) => set((state) => ({
        tasks: state.tasks.filter(t => t.id !== taskId)
      })),

      reorderColumns: (startIndex, endIndex) => set((state) => {
        const newColumns = [...state.columns];
        const [removed] = newColumns.splice(startIndex, 1);
        newColumns.splice(endIndex, 0, removed);
        return { columns: newColumns };
      }),
    }),
    { name: 'kanban-storage' }
  )
);
