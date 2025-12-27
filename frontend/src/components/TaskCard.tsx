
'use client';

import { FaCheck, FaPencilAlt, FaTrash } from 'react-icons/fa';

interface Task {
  id: number;
  title: string;
  description: string;
  completed: boolean;
}

interface TaskCardProps {
  task: Task;
  onUpdate: (id: number, data: Partial<Task>) => void;
  onDelete: (id: number) => void;
  onEdit: (task: Task) => void;
}

export default function TaskCard({ task, onUpdate, onDelete, onEdit }: TaskCardProps) {
  const cardClasses = `
    bg-gray-800/50 backdrop-blur-lg rounded-xl shadow-lg p-5 text-white 
    transform hover:-translate-y-1 transition-all duration-300
    border border-transparent
    ${!task.completed ? 'hover:shadow-purple-500/30' : 'hover:shadow-green-500/20'}
  `;

  return (
    <div className={cardClasses}>
      <div className="flex justify-between items-start">
        <div className="flex-grow">
          <h3 className="text-xl font-bold">{task.title}</h3>
          <p className="mt-2 text-gray-400 text-sm">
            {task.description ? task.description : <span className="text-gray-500">No description provided</span>}
          </p>
        </div>
        <span
          className={`ml-4 px-2.5 py-1 text-xs font-bold rounded-full ${
            task.completed ? 'bg-green-500/20 text-green-300' : 'bg-purple-500/20 text-purple-300'
          }`}
        >
          {task.completed ? 'COMPLETED' : 'PENDING'}
        </span>
      </div>
      <div className="mt-4 flex justify-end items-center space-x-3">
        {!task.completed && (
          <button
            onClick={() => onUpdate(task.id, { completed: true })}
            className="p-2 rounded-full text-gray-400 hover:bg-green-500/20 hover:text-green-300 transition-colors"
            aria-label="Complete Task"
          >
            <FaCheck />
          </button>
        )}
        <button
            onClick={() => onEdit(task)}
            className="p-2 rounded-full text-gray-400 hover:bg-blue-500/20 hover:text-blue-300 transition-colors"
            aria-label="Edit Task"
        >
            <FaPencilAlt />
        </button>
        <button
          onClick={() => onDelete(task.id)}
          className="p-2 rounded-full text-gray-400 hover:bg-red-500/20 hover:text-red-300 transition-colors"
          aria-label="Delete Task"
        >
          <FaTrash />
        </button>
      </div>
    </div>
  );
}
