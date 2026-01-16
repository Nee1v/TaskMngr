import React, { useState, useEffect, useCallback } from "react";

export default function TaskManager() {
  const [todoTasks, setTodoTasks] = useState([]);
  const [completedTasks, setCompletedTasks] = useState([]);
  const [undoStack, setUndoStack] = useState([]);
  const [goal, setGoal] = useState("Origins");
  const [activeInfo, setActiveInfo] = useState(null);
  const [showResetConfirm, setShowResetConfirm] = useState(false);
  
  const goals = ["Origins", "Pizza", "Cake"];

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
    setShowResetConfirm(false); // Close reset popup if user switches goals
    setActiveInfo(null); // Close any open info popups

    return () => {
      fetch(`http://127.0.0.1:8000/tasks/reset/${goal}`, { method: "POST" });
    };
  }, [goal, fetchTasks]);

  // 3. Global Click-Away Listener for all Popups
  useEffect(() => {
    const handleOutsideClick = (event) => {
      if (activeInfo && !event.target.closest('.info-container')) {
        setActiveInfo(null);
      }
      if (showResetConfirm && !event.target.closest('.reset-container')) {
        setShowResetConfirm(false);
      }
    };

    window.addEventListener("mousedown", handleOutsideClick);
    return () => window.removeEventListener("mousedown", handleOutsideClick);
  }, [activeInfo, showResetConfirm]);

  // 4. Manual Reset functions
  const handleResetClick = () => {
    setShowResetConfirm(true);
  };

  const confirmReset = async () => {
    await fetch(`http://127.0.0.1:8000/tasks/reset/${goal}`, { method: "POST" });
    await fetchTasks();
    setUndoStack([]);
    setShowResetConfirm(false);
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
    <div style={{ 
      minHeight: "100vh", 
      backgroundColor: "#0a0a0a", 
      color: "#e0e0e0",          
      padding: "20px", 
      fontFamily: "'Segoe UI', Roboto, sans-serif" 
    }}>
      <h1 style={{ color: "#ff8c00", textTransform: "uppercase", letterSpacing: "2px" }}>
        BO3 Zombies EE Tool
      </h1>

      {/* Header UI */}
      <div style={{ 
        marginBottom: "20px", 
        display: "flex", 
        alignItems: "center", 
        gap: "20px",
        position: "sticky",
        top: 0,
        backgroundColor: "#0a0a0a", // Matches background
        zIndex: 100,
        padding: "10px 0",
        borderBottom: "1px solid #333"
      }}>
        <label style={{ fontWeight: "bold", color: "#ff8c00" }}>
          Current Quest:{" "}
          <select 
            value={goal} 
            onChange={(e) => setGoal(e.target.value)}
            style={{ 
              padding: "8px", 
              borderRadius: "4px", 
              backgroundColor: "#1a1a1a", 
              color: "#fff", 
              border: "1px solid #ff8c00" 
            }}
          >
            {goals.map((g) => (
              <option key={g} value={g}>{g}</option>
            ))}
          </select>
        </label>

        {/* Reset Container */}
        <div className="reset-container" style={{ position: "relative" }}>
          <button 
            onClick={handleResetClick}
            style={{ 
              backgroundColor: "transparent", 
              color: "#ff4d4d", 
              border: "2px solid #ff4d4d", 
              padding: "8px 18px", 
              borderRadius: "4px", 
              cursor: "pointer", 
              fontWeight: "bold",
              textTransform: "uppercase"
            }}
          >
            Reset EE
          </button>

          {showResetConfirm && (
            <div style={{
              position: "absolute",
              top: "50px",
              left: "0",
              zIndex: 1000,
              width: "250px",
              backgroundColor: "#1a1a1a",
              color: "#ecf0f1",
              padding: "15px",
              borderRadius: "8px",
              border: "1px solid #ff4d4d",
              boxShadow: "0px 0px 15px rgba(255, 77, 77, 0.4)",
              textAlign: "center"
            }}>
              <div style={{ marginBottom: "12px", fontWeight: "bold" }}>
                Restart the {goal} quest?
              </div>
              <div style={{ display: "flex", gap: "10px", justifyContent: "center" }}>
                <button 
                  onClick={confirmReset}
                  style={{ backgroundColor: "#ff4d4d", color: "white", border: "none", padding: "8px 14px", borderRadius: "4px", cursor: "pointer" }}
                >
                  Confirm
                </button>
                <button 
                  onClick={() => setShowResetConfirm(false)}
                  style={{ backgroundColor: "#333", color: "white", border: "none", padding: "8px 14px", borderRadius: "4px", cursor: "pointer" }}
                >
                  Back
                </button>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Main Container */}
      <div style={{ display: "flex", gap: "30px", height: "75vh" }}>
        
        {/* TODO Column */}
        <div style={{ 
          flex: 1, 
          display: "flex", 
          flexDirection: "column", 
          border: "1px solid #444", 
          borderRadius: "8px", 
          padding: "0px 20px 20px 20px", 
          backgroundColor: "#111" 
        }}>
          <h2 style={{ borderBottom: "2px solid #ff8c00", paddingBottom: "10px", color: "#ff8c00" }}>Available Steps</h2>
          <div style={{ overflowY: "auto", flex: 1, paddingRight: "10px" }}>
            <ul style={{ listStyle: "none", padding: 0 }}>
              {todoTasks.map((task) => (
                <li
                  key={task.id}
                  style={{ 
                    padding: "12px",  //
                    border: "1px solid #222", 
                    marginBottom: "10px", 
                    borderRadius: "4px", 
                    backgroundColor: "#1a1a1a", 
                    display: "flex", 
                    justifyContent: "space-between", 
                    alignItems: "center",
                    position: "relative"
                  }}
                >
                  <span onClick={() => completeTask(task)} style={{ cursor: "pointer", flex: 1, color: "#e0e0e0" }}>
                    {task.title}
                  </span>
                  
                  <div className="info-container" style={{ position: "relative", display: "flex", alignItems: "center" }}>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        setActiveInfo(activeInfo?.id === task.id ? null : task);
                      }}
                      style={{ 
                        background: "none", 
                        border: "1px solid #ff8c00", 
                        color: "#ff8c00", 
                        borderRadius: "50%", 
                        width: "24px", height: "24px", cursor: "pointer"
                      }}
                    >
                      i
                    </button>

                    {activeInfo?.id === task.id && (
                      <div style={{ 
                        position: "absolute", top: "35px", right: "0", zIndex: 1000, width: "280px", 
                        backgroundColor: "#1a1a1a", color: "#ccc", padding: "18px", borderRadius: "8px", 
                        border: "1px solid #ff8c00", boxShadow: "0px 0px 20px rgba(255, 140, 0, 0.2)"
                      }}>
                        <div style={{ fontWeight: "bold", marginBottom: "8px", color: "#ff8c00", borderBottom: "1px solid #333" }}>
                          Description
                        </div>
                        {task.description}
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
          border: "1px solid #444", 
          borderRadius: "8px", 
          padding: "20px", 
          backgroundColor: "#111" 
        }}>
          {/* Header Container - Fixed alignment to match TODO */}
          <div style={{ 
            display: "flex", 
            justifyContent: "space-between", 
            alignItems: "center", 
            marginBottom: "15px", 
            borderBottom: "2px solid #ff8c00", // Matches the Available orange bar
            paddingBottom: "10px" 
          }}>
            <h2 style={{ 
              margin: 0,              // Explicitly removed top margin for perfect alignment
              color: "#ff8c00",       // Bright orange to match Available header 
              letterSpacing: "1px",
              fontSize: "1.5rem"      // Matches the standard H2 size of the left column
            }}>
              Finished Steps
            </h2>
            <button 
              onClick={undoTask} 
              disabled={undoStack.length === 0}
              style={{ 
                background: "none", 
                border: "1px solid #ff8c00", 
                color: "#ff8c00", 
                cursor: undoStack.length === 0 ? "default" : "pointer",
                padding: "4px 12px",
                fontSize: "12px",
                borderRadius: "4px",
                opacity: undoStack.length === 0 ? 0.2 : 0.8,
                textTransform: "uppercase"
              }}
            >
              UNDO
            </button>
          </div>
          
          {/* List Area */}
          <div style={{ overflowY: "auto", flex: 1, paddingRight: "10px" }}>
            <ul style={{ listStyle: "none", padding: 0 }}>
              {completedTasks.map((task) => (
                <li 
                  key={task.id} 
                  style={{ 
                    padding: "12px", 
                    border: "1px solid #222", 
                    marginBottom: "10px", 
                    borderRadius: "4px", 
                    backgroundColor: "#ff8c00", 
                    color: "#1a1a1a",           // Orange text as requested
                    fontSize: "16px",
                    fontWeight: "500",
                    display: "flex",
                    alignItems: "center",
                    gap: "10px",
                    opacity: 0.6               // Dimmed slightly so you can tell it's done
                  }}
                >
                  {/* Dim Checkmark */}
                  <span style={{ color: "#1a1a1a", fontSize: "18px", opacity: 1.0 }}>✓</span>
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