import React, { useState, useEffect, useCallback } from "react";

export default function TaskManager() {
  const [todoTasks, setTodoTasks] = useState([]);
  const [completedTasks, setCompletedTasks] = useState([]);
  const [undoStack, setUndoStack] = useState([]);
  const [goal, setGoal] = useState("Bread");
  const [activeInfo, setActiveInfo] = useState(null); // For the pretty popup
  
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

  // 2. Goal-switch and Initial Load
  useEffect(() => {
    fetchTasks();
    setUndoStack([]);

    return () => {
      fetch(`http://127.0.0.1:8000/tasks/reset/${goal}`, { method: "POST" });
    };
  }, [goal, fetchTasks]);

  // 3. Click-Away Listener for Popups
  useEffect(() => {
    const handleOutsideClick = (event) => {
      // If the user clicks something that isn't the info button or the popup, close it
      if (activeInfo && !event.target.closest('.info-container')) {
        setActiveInfo(null);
      }
    };

    window.addEventListener("mousedown", handleOutsideClick);
    return () => window.removeEventListener("mousedown", handleOutsideClick);
  }, [activeInfo]);

  // 4. Manual Reset function
  const resetCurrentGoal = async () => {
    if (!window.confirm(`Reset all progress for the ${goal} goal?`)) return;
    await fetch(`http://127.0.0.1:8000/tasks/reset/${goal}`, { method: "POST" });
    await fetchTasks();
    setUndoStack([]);
  };

  // 5. Action functions
  const completeTask = async (task) => {
    await fetch(`http://127.0.0.1:8000/tasks/${task.id}/complete`, { method: "POST" });
    await fetchTasks();
    setUndoStack([...undoStack, task]);
  };

  const undoTask = async () => {
    if (undoStack.length === 0) return;
    const lastTask = undoStack[undoStack.length - 1];
    await fetch(`http://127.0.0.1:8000/tasks/${lastTask.id}/undo`, { method: "POST" });
    await fetchTasks();
    setUndoStack(undoStack.slice(0, -1));
  };

  return (
    <div style={{ padding: "20px", fontFamily: "'Segoe UI', Roboto, sans-serif", color: "#333" }}>
      <h1>Quest Tracker</h1>

      {/* Header UI */}
      <div style={{ 
        marginBottom: "20px", 
        display: "flex", 
        alignItems: "center", 
        gap: "20px",
        position: "sticky",
        top: 0,
        backgroundColor: "white",
        zIndex: 100,
        padding: "10px 0"
      }}>
        <label style={{ fontWeight: "bold" }}>
          Current Quest:{" "}
          <select 
            value={goal} 
            onChange={(e) => setGoal(e.target.value)}
            style={{ padding: "5px", borderRadius: "4px" }}
          >
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
            padding: "8px 16px", 
            borderRadius: "4px", 
            cursor: "pointer", 
            fontWeight: "bold" 
          }}
        >
          Reset Current Goal
        </button>
      </div>

      {/* Main Container */}
      <div style={{ display: "flex", gap: "30px", height: "75vh" }}>
        
        {/* TODO Column */}
        <div style={{ 
          flex: 1, 
          display: "flex", 
          flexDirection: "column", 
          border: "1px solid #ddd", 
          borderRadius: "12px", 
          padding: "20px", 
          backgroundColor: "#fcfcfc" 
        }}>
          <h2 style={{ borderBottom: "2px solid #007bff", paddingBottom: "10px" }}>Available Objectives</h2>
          <div style={{ overflowY: "auto", flex: 1, paddingRight: "10px" }}>
            {todoTasks.length === 0 && <p>Quest Complete!</p>}
            <ul style={{ listStyle: "none", padding: 0 }}>
              {todoTasks.map((task) => (
                <li
                  key={task.id}
                  style={{ 
                    padding: "12px", 
                    border: "1px solid #eee", 
                    marginBottom: "10px", 
                    borderRadius: "8px", 
                    backgroundColor: "#fff", 
                    display: "flex", 
                    justifyContent: "space-between", 
                    alignItems: "center",
                    position: "relative"
                  }}
                >
                  <span onClick={() => completeTask(task)} style={{ cursor: "pointer", flex: 1 }}>
                    {task.title}
                  </span>
                  
                  {/* Info Container for Popup Logic */}
                  <div className="info-container" style={{ position: "relative", display: "flex", alignItems: "center" }}>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        setActiveInfo(activeInfo?.id === task.id ? null : task);
                      }}
                      style={{ 
                        background: activeInfo?.id === task.id ? "#007bff" : "none", 
                        border: "1px solid #007bff", 
                        color: activeInfo?.id === task.id ? "#fff" : "#007bff", 
                        borderRadius: "50%", width: "24px", height: "24px", cursor: "pointer",
                        fontWeight: "bold"
                      }}
                    >
                      i
                    </button>

                    {activeInfo?.id === task.id && (
                      <div style={{
                        position: "absolute",
                        top: "30px",
                        right: "0",
                        zIndex: 1000,
                        width: "260px",
                        backgroundColor: "#2c3e50",
                        color: "#ecf0f1",
                        padding: "15px",
                        borderRadius: "8px",
                        boxShadow: "0px 8px 24px rgba(0,0,0,0.3)",
                        fontSize: "14px"
                      }}>
                        <div style={{ fontWeight: "bold", marginBottom: "8px", color: "#3498db", borderBottom: "1px solid #5d6d7e" }}>
                          Description
                        </div>
                        {task.description || "No details available."}
                      </div>
                    )}
                  </div>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Completed Column */}
        <div style={{ 
          flex: 1, 
          display: "flex", 
          flexDirection: "column", 
          border: "1px solid #c3e6cb", 
          borderRadius: "12px", 
          padding: "20px", 
          backgroundColor: "#f8fff9" 
        }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "10px" }}>
            <h2 style={{ margin: 0 }}>Finished Objectives</h2>
            <button onClick={undoTask} disabled={undoStack.length === 0}>Undo</button>
          </div>
          <div style={{ overflowY: "auto", flex: 1, paddingRight: "10px" }}>
            <ul style={{ listStyle: "none", padding: 0 }}>
              {completedTasks.map((task) => (
                <li 
                  key={task.id} 
                  style={{ 
                    padding: "12px", border: "1px solid #d4edda", marginBottom: "8px", 
                    borderRadius: "8px", backgroundColor: "#eaffea", color: "#155724",
                    textDecoration: "line-through"
                  }}
                >
                  {task.title}
                </li>
              ))}
            </ul>
          </div>
        </div>

      </div>
    </div>
  );
}