
'use client';

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
  return (
    <div className="bg-white/10 backdrop-blur-md rounded-xl shadow-lg p-6 text-white transform hover:-translate-y-1 transition-transform duration-300">
      <div className="flex justify-between items-start">
        <div>
          <h3 className="text-xl font-bold">{task.title}</h3>
          <p className="mt-2 text-gray-300">{task.description}</p>
        </div>
        <span
          className={`px-2 py-1 text-xs font-semibold rounded-full ${
            task.completed ? 'bg-green-500/70' : 'bg-yellow-500/70'
          }`}
        >
          {task.completed ? 'Done' : 'Pending'}
        </span>
      </div>
      <div className="mt-4 flex justify-end space-x-2">
        {!task.completed && (
          <button
            onClick={() => onUpdate(task.id, { completed: true })}
            className="px-3 py-1 text-sm text-white bg-green-500/70 rounded-full hover:bg-green-600/70"
          >
            ✅ Complete
          </button>
        )}
        <button
            onClick={() => onEdit(task)}
            className="px-3 py-1 text-sm text-white bg-blue-500/70 rounded-full hover:bg-blue-600/70"
        >
            ✏️ Edit
        </button>
        <button
          onClick={() => onDelete(task.id)}
          className="px-3 py-1 text-sm text-white bg-red-500/70 rounded-full hover:bg-red-600/70"
        >
          🗑️ Delete
        </button>
      </div>
    </div>
  );
}
