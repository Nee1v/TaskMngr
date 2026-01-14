import React, { useState, useEffect, useCallback } from "react";

export default function TaskManager() {
  const [todoTasks, setTodoTasks] = useState([]);
  const [completedTasks, setCompletedTasks] = useState([]);
  const [undoStack, setUndoStack] = useState([]);
  const [goal, setGoal] = useState("Bread");
  const goals = ["Bread", "Pizza", "Cake"];

  // 1. Fetch logic
  const fetchTasks = useCallback(async () => {
    const todoRes = await fetch(`http://127.0.0.1:8000/tasks/todo?goal=${goal}`);
    const todos = await todoRes.json();
    setTodoTasks(todos);

    const completedRes = await fetch(`http://127.0.0.1:8000/tasks/completed?goal=${goal}`);
    const completed = await completedRes.json();
    setCompletedTasks(completed);
  }, [goal]);

  // 2. Goal-switch reset logic
  useEffect(() => {
    fetchTasks();
    setUndoStack([]);

    return () => {
      fetch(`http://127.0.0.1:8000/tasks/reset/${goal}`, { method: "POST" });
    };
  }, [goal, fetchTasks]);

  // 3. Manual reset function
  const resetCurrentGoal = async () => {
    if (!window.confirm(`Reset all progress for the ${goal} goal?`)) return;

    await fetch(`http://127.0.0.1:8000/tasks/reset/${goal}`, {
      method: "POST",
    });

    await fetchTasks();
    setUndoStack([]);
  };

  // 4. Action functions
  const completeTask = async (task) => {
    await fetch(`http://127.0.0.1:8000/tasks/${task.id}/complete`, {
      method: "POST",
    });
    await fetchTasks();
    setUndoStack([...undoStack, task]);
  };

  const undoTask = async () => {
    if (undoStack.length === 0) return;
    const lastTask = undoStack[undoStack.length - 1];

    await fetch(`http://127.0.0.1:8000/tasks/${lastTask.id}/undo`, {
      method: "POST",
    });
    await fetchTasks();
    setUndoStack(undoStack.slice(0, -1));
  };

  // 5. The UI Return
  return (
    <div style={{ padding: "20px" }}>
      <h1>Quest Tracker</h1>

      <div style={{ 
        marginBottom: "20px", 
        display: "flex", 
        alignItems: "center", 
        gap: "20px" 
      }}>
        <label>
          Current Quest:{" "}
          <select value={goal} onChange={(e) => setGoal(e.target.value)}>
            {goals.map((g) => (
              <option key={g} value={g}>{g}</option>
            ))}
          </select>
        </label>

        <button 
          onClick={resetCurrentGoal}
          style={{
            backgroundColor: "#ff4d4d",
            color: "white",
            border: "none",
            padding: "6px 15px",
            borderRadius: "4px",
            cursor: "pointer",
            fontWeight: "bold"
          }}
        >
          Reset Current Goal
        </button>
      </div>

      <div style={{ display: "flex", gap: "50px" }}>
        <div style={{ flex: 1 }}>
          <h2>Available Objectives</h2>
          {todoTasks.length === 0 && <p>Quest Complete!</p>}
          <ul>
            {todoTasks.map((task) => (
              <li
                key={task.id}
                style={{ padding: "10px", border: "1px solid #ccc", marginBottom: "5px", cursor: "pointer" }}
                onClick={() => completeTask(task)}
              >
                {task.title}
              </li>
            ))}
          </ul>
        </div>

        <div style={{ flex: 1 }}>
          <h2>Finished Objectives</h2>
          <button 
            onClick={undoTask} 
            disabled={undoStack.length === 0} 
            style={{ marginBottom: "10px" }}
          >
            Undo Action
          </button>
          <ul>
            {completedTasks.map((task) => (
              <li 
                key={task.id} 
                style={{ padding: "10px", border: "1px solid #ccc", marginBottom: "5px", backgroundColor: "#e0ffe0" }}
              >
                {task.title}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}