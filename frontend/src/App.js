import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [todos, setTodos] = useState([]);

  useEffect(() => {
    fetch('http://localhost:5001/todos')
      .then(response => response.json())
      .then(data => setTodos(data))
      .catch(error => console.error('Error:', error));
  }, []);

  return (
    <div className="App">
      <h1>My Todos</h1>
      <ul>
        {todos.map(todo => (
          <li key={todo.id}>
            {todo.task} - {todo.completed ? '✅' : '❌'}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
