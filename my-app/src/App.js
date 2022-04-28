import logo from './logo.svg';
import './App.css';

import { useState, useEffect } from 'react';

const WS_URL = "ws://localhost:8080/websocket";



function App() {
  const [websocket, _] = useState(new WebSocket(WS_URL));
  const [total, setTotal] = useState(null);
  const [horizontal_labels, setLabels] = useState([]);

  useEffect(() => {
    websocket.onmessage = (event) => {
      const payload = JSON.parse(event.data);
      const payload_json = JSON.parse(payload);

      if (!horizontal_labels.includes(payload_json["PRODUCT_NAME"])){
          horizontal_labels.push(payload_json["PRODUCT_NAME"])
          setLabels(horizontal_labels);
      }
      console.log(horizontal_labels);
      console.log(payload_json);
    };

  }, [websocket]);

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <h2>{total || "...waiting..."}</h2>
      </header>
    </div>
  );
}
export default App;
