export type Priority = 'low' | 'medium' | 'high';

export interface Task {
  id: string;
  title: string;
  description?: string;
  priority: Priority;
  columnId: string;
  createdAt: number;
}

export interface Column {
  id: string;
  title: string;
}

export interface KanbanState {
  tasks: Task[];
  columns: Column[];
  moveTask: (taskId: string, newColumnId: string, newIndex: number) => void;
  addTask: (task: Omit<Task, 'id' | 'createdAt'>) => void;
  deleteTask: (taskId: string) => void;
  reorderColumns: (startIndex: number, endIndex: number) => void;
}
