'use client';
import { useState, useEffect } from 'react';
import axios from 'axios';

interface Employee {
  id: string;
  username: string;
  employee_id: string;
  is_active: boolean;
}

interface Project {
  id: string;
  name: string;
}

interface Task {
  id: string;
  name: string;
  project_id: string;
}

interface TimeEntry {
  id: string;
  task_id: string;
  task_name: string;
  project_name: string;
  start_time: string;
  end_time: string | null;
  duration_seconds: number | null;
  is_active: boolean;
}

export default function Home() {
  const [token, setToken] = useState<string>('');
  const [username, setUsername] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [tasks, setTasks] = useState<Task[]>([]);
  const [selectedTask, setSelectedTask] = useState<string>('');
  const [message, setMessage] = useState<string>('');
  const [error, setError] = useState<string>('');
  const [isTracking, setIsTracking] = useState<boolean>(false);
  const [timeEntryId, setTimeEntryId] = useState<string>('');
  const [elapsedTime, setElapsedTime] = useState<number>(0);
  const [startTime, setStartTime] = useState<Date | null>(null);

  const login = async () => {
    try {
      const response = await axios.post<{ access: string; refresh: string }>(
        'http://localhost:8000/api/login/',
        { username, password }
      );
      setToken(response.data.access);
      localStorage.setItem('refreshToken', response.data.refresh);
      setMessage('Login successful');
      setError('');
      loadTasks(response.data.access);
    } catch (err) {
      setError('Login failed');
      setMessage('');
    }
  };

  const loadTasks = async (authToken: string) => {
    try {
      const response = await axios.get<Task[]>('http://localhost:8000/api/tasks/', {
        headers: { Authorization: `Bearer ${authToken}` },
      });
      setTasks(response.data);
      setError('');
    } catch (err) {
      setError('Failed to load tasks');
    }
  };

  const startTracking = async () => {
    if (!selectedTask) {
      setError('Select a task');
      return;
    }
    try {
      const response = await axios.post(
        'http://localhost:8000/api/time-entries/start_tracking/',
        { task_id: selectedTask },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setIsTracking(true);
      setTimeEntryId(response.data.id);
      setStartTime(new Date(response.data.start_time));
      setMessage('Tracking started');
      setError('');
    } catch (err) {
      setError('Failed to start tracking');
      setMessage('');
    }
  };

  const stopTracking = async () => {
    try {
      const response = await axios.post(
        'http://localhost:8000/api/time-entries/stop_tracking/',
        {},
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setIsTracking(false);
      setTimeEntryId('');
      setStartTime(null);
      setMessage('Tracking stopped');
      setError('');
    } catch (err) {
      setError('Failed to stop tracking');
      setMessage('');
    }
  };

  useEffect(() => {
    if (token) {
      loadTasks(token);
      const interval = setInterval(() => {
        axios
          .get<TimeEntry>('http://localhost:8000/api/time-entries/active/', {
            headers: { Authorization: `Bearer ${token}` },
          })
          .then((response) => {
            if (response.data.id) {
              setIsTracking(true);
              setTimeEntryId(response.data.id);
              setSelectedTask(response.data.task_id);
              setStartTime(new Date(response.data.start_time));
            } else {
              setIsTracking(false);
              setTimeEntryId('');
              setStartTime(null);
            }
          })
          .catch(() => {});
      }, 30000);
      return () => clearInterval(interval);
    }
  }, [token]);

  useEffect(() => {
    if (isTracking && startTime) {
      const interval = setInterval(() => {
        setElapsedTime(Math.floor((new Date().getTime() - startTime.getTime()) / 1000));
      }, 1000);
      return () => clearInterval(interval);
    } else {
      setElapsedTime(0);
    }
  }, [isTracking, startTime]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-8 rounded shadow-md w-96">
        <h1 className="text-2xl font-bold mb-4">Time Tracker</h1>
<div className="bg-blue-500 text-white p-4">Test Tailwind</div>        {!token ? (
          <>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Username"
              className="w-full p-2 mb-4 border rounded"
            />
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Password"
              className="w-full p-2 mb-4 border rounded"
            />
            <button
              onClick={login}
              className="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600"
            >
              Login
            </button>
          </>
        ) : (
          <>
            <select
              value={selectedTask}
              onChange={(e) => setSelectedTask(e.target.value)}
              className="w-full p-2 mb-4 border rounded"
              disabled={isTracking}
            >
              <option value="">Select a task</option>
              {tasks.map((task) => (
                <option key={task.id} value={task.id}>
                  {task.name} ({task.project_id})
                </option>
              ))}
            </select>
            <button
              onClick={startTracking}
              disabled={isTracking}
              className="w-full bg-green-500 text-white p-2 rounded hover:bg-green-600 disabled:bg-gray-400"
            >
              Start Tracking
            </button>
            <button
              onClick={stopTracking}
              disabled={!isTracking}
              className="w-full bg-red-500 text-white p-2 rounded hover:bg-red-600 disabled:bg-gray-400 mt-2"
            >
              Stop Tracking
            </button>
            <button
              onClick={() => setToken('')}
              className="w-full bg-gray-500 text-white p-2 rounded hover:bg-gray-600 mt-2"
            >
              Logout
            </button>
            {isTracking && (
              <p className="mt-4 text-blue-500">
                Time Elapsed: {Math.floor(elapsedTime / 60)}m {elapsedTime % 60}s
              </p>
            )}
          </>
        )}
        {message && <p className="mt-4 text-green-500">{message}</p>}
        {error && <p className="mt-4 text-red-500">{error}</p>}
      </div>
    </div>
  );
}
