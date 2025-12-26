'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { getTasks, addTask, updateTask, deleteTask } from '@/lib/api';
import TaskCard from '@/components/TaskCard';
import EditTaskModal from '@/components/EditTaskModal';

interface Task {
  id: number;
  title: string;
  description: string;
  completed: boolean;
}

export default function DashboardPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [error, setError] = useState('');
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      router.push('/login');
    } else {
      fetchTasks();
    }
  }, [router]);

  const fetchTasks = async () => {
    try {
      const response = await getTasks();
      setTasks(response.data);
    } catch (err) {
      setError('Failed to fetch tasks.');
    }
  };

  const handleAddTask = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await addTask({ title, description });
      setTitle('');
      setDescription('');
      fetchTasks();
    } catch (err) {
      setError('Failed to add task.');
    }
  };

  const handleUpdateTask = async (id: number, data: Partial<Task>) => {
    try {
      await updateTask(id, data);
      fetchTasks();
      setEditingTask(null);
    } catch (err) {
      setError('Failed to update task.');
    }
  };

  const handleDeleteTask = async (id: number) => {
    try {
      await deleteTask(id);
      fetchTasks();
    } catch (err) {
      setError('Failed to delete task.');
    }
  };

  const handleEditClick = (task: Task) => {
    setEditingTask(task);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    router.push('/login');
  };

  return (
    <div className="min-h-screen p-8">
      <header className="flex justify-between items-center mb-8">
        <h1 className="text-4xl font-bold text-white">My Tasks</h1>
        <button
          onClick={handleLogout}
          className="px-4 py-2 font-semibold text-white bg-red-500/70 rounded-lg shadow-lg hover:bg-red-600/70"
        >
          Logout
        </button>
      </header>

      <div className="mb-8 p-6 bg-white/10 backdrop-blur-md rounded-xl shadow-lg">
        <h2 className="text-2xl font-bold text-white mb-4">Add a New Task</h2>
        <form onSubmit={handleAddTask} className="space-y-4">
          <input
            type="text"
            placeholder="Task Title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
            className="w-full px-3 py-2 text-white bg-white/20 rounded-lg border border-transparent focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
          <textarea
            placeholder="Task Description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            required
            className="w-full px-3 py-2 text-white bg-white/20 rounded-lg border border-transparent focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
          <button
            type="submit"
            className="w-full px-4 py-2 font-semibold text-white bg-gradient-to-r from-indigo-600 to-violet-600 rounded-lg shadow-lg hover:from-indigo-700 hover:to-violet-700"
          >
            Add Task
          </button>
        </form>
        {error && <p className="mt-4 text-sm text-red-400">{error}</p>}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {tasks.map((task) => (
          <TaskCard
            key={task.id}
            task={task}
            onUpdate={(id, data) => handleUpdateTask(id, data)}
            onDelete={handleDeleteTask}
            onEdit={handleEditClick}
          />
        ))}
      </div>
      <EditTaskModal
        task={editingTask}
        onClose={() => setEditingTask(null)}
        onSave={handleUpdateTask}
      />
    </div>
  );
}