
'use client';

import { useState, useEffect } from 'react';

interface Task {
  id: number;
  title: string;
  description: string;
  completed: boolean;
}

interface EditTaskModalProps {
  task: Task | null;
  onClose: () => void;
  onSave: (id: number, data: { title: string; description: string }) => void;
}

export default function EditTaskModal({ task, onClose, onSave }: EditTaskModalProps) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');

  useEffect(() => {
    if (task) {
      setTitle(task.title);
      setDescription(task.description);
    }
  }, [task]);

  if (!task) return null;

  const handleSave = () => {
    onSave(task.id, { title, description });
  };

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
      <div className="w-full max-w-lg p-8 space-y-6 bg-white/10 backdrop-blur-xl rounded-2xl shadow-2xl">
        <h2 className="text-3xl font-bold text-white">Edit Task</h2>
        <div className="space-y-4">
          <div>
            <label htmlFor="title" className="text-sm font-medium text-gray-300">
              Title
            </label>
            <input
              id="title"
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="w-full px-3 py-2 mt-1 text-white bg-white/20 rounded-lg border border-transparent focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>
          <div>
            <label htmlFor="description" className="text-sm font-medium text-gray-300">
              Description
            </label>
            <textarea
              id="description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full px-3 py-2 mt-1 text-white bg-white/20 rounded-lg border border-transparent focus:outline-none focus:ring-2 focus:ring-indigo-500"
              rows={4}
            />
          </div>
        </div>
        <div className="flex justify-end space-x-4">
          <button
            onClick={onClose}
            className="px-4 py-2 font-semibold text-gray-300 bg-white/10 rounded-lg hover:bg-white/20"
          >
            Cancel
          </button>
          <button
            onClick={handleSave}
            className="px-4 py-2 font-semibold text-white bg-gradient-to-r from-indigo-600 to-violet-600 rounded-lg shadow-lg hover:from-indigo-700 hover:to-violet-700"
          >
            Save
          </button>
        </div>
      </div>
    </div>
  );
}
