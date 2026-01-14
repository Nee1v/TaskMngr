import React, { useState, useEffect } from "react";

export default function TaskManager() {
  const [todoTasks, setTodoTasks] = useState([]);
  const [completedTasks, setCompletedTasks] = useState([]);
  const [undoStack, setUndoStack] = useState([]);
  const [goal, setGoal] = useState("Bread"); // Default goal
  const goals = ["Bread", "Pizza", "Cake"]; // Add more goals as needed

  // Fetch tasks whenever goal changes
  useEffect(() => {
    fetchTasks();
  }, [goal]);

  const fetchTasks = async () => {
    // Fetch TODO tasks
    const todoRes = await fetch(
      `http://127.0.0.1:8000/tasks/todo?goal=${goal}`
    );
    const todos = await todoRes.json();
    setTodoTasks(todos);

    // Fetch Completed tasks
    const completedRes = await fetch(
      `http://127.0.0.1:8000/tasks/completed?goal=${goal}`
    );
    const completed = await completedRes.json();
    setCompletedTasks(completed);

    // Reset undo stack when switching goals
    setUndoStack([]);
  };

  const completeTask = async (task) => {
    // Update backend
    await fetch(`http://127.0.0.1:8000/tasks/${task.id}/complete`, {
      method: "POST",
    });

    // Update frontend
    setTodoTasks(todoTasks.filter((t) => t.id !== task.id));
    setCompletedTasks([...completedTasks, task]);
    setUndoStack([...undoStack, task]);
  };

  const undoTask = async () => {
    if (undoStack.length === 0) return;
    const lastTask = undoStack[undoStack.length - 1];

    await fetch(`http://127.0.0.1:8000/tasks/${lastTask.id}/undo`, {
      method: "POST",
    });

    setCompletedTasks(completedTasks.filter((t) => t.id !== lastTask.id));
    setTodoTasks([...todoTasks, lastTask]);
    setUndoStack(undoStack.slice(0, -1));
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Task Manager</h1>

      {/* Goal selection */}
      <div style={{ marginBottom: "20px" }}>
        <label>
          Select Goal:{" "}
          <select value={goal} onChange={(e) => setGoal(e.target.value)}>
            {goals.map((g) => (
              <option key={g} value={g}>
                {g}
              </option>
            ))}
          </select>
        </label>
      </div>

      {/* Columns */}
      <div style={{ display: "flex", gap: "50px" }}>
        {/* TODO column */}
        <div style={{ flex: 1 }}>
          <h2>TODO</h2>
          {todoTasks.length === 0 && <p>No tasks to do!</p>}
          <ul>
            {todoTasks.map((task) => (
              <li
                key={task.id}
                style={{
                  padding: "10px",
                  border: "1px solid #ccc",
                  marginBottom: "5px",
                  cursor: "pointer",
                }}
                onClick={() => completeTask(task)}
                title={task.description}
              >
                {task.title}
              </li>
            ))}
          </ul>
        </div>

        {/* Completed column */}
        <div style={{ flex: 1 }}>
          <h2>Completed</h2>
          <button
            onClick={undoTask}
            disabled={undoStack.length === 0}
            style={{ marginBottom: "10px" }}
          >
            Undo
          </button>
          {completedTasks.length === 0 && <p>No completed tasks yet.</p>}
          <ul>
            {completedTasks.map((task) => (
              <li
                key={task.id}
                style={{
                  padding: "10px",
                  border: "1px solid #ccc",
                  marginBottom: "5px",
                  backgroundColor: "#e0ffe0",
                }}
                title={task.description}
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