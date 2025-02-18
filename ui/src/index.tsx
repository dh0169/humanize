import React from 'react';
import ReactDOM from 'react-dom/client';
import './styles/index.css';
import App from './App';

let rootElement = document.getElementById('root');

if(!rootElement) {
  rootElement = document.createElement('div');
  rootElement.id = "root";
} 

const root = ReactDOM.createRoot(rootElement);
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);