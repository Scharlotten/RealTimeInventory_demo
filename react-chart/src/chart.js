import React from 'react';
import { Bar } from 'react-chartjs-2';
import faker from 'faker';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

import { useState, useEffect } from 'react';

const WS_URL = "ws://localhost:8080/websocket";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

export const options = {
  responsive: true,
  plugins: {
    legend: {
      position: 'top'
    },
    title: {
      display: true,
      text: 'Real time Inventory',
    },
  },
};

export function Chart() {

  const [websocket, _] = useState(new WebSocket(WS_URL));
  const [horizontal_labels, setLabels] = useState([]);
  const [data_points, setDataPoints] = useState({});
  const [barState, setBarState] = useState({
        labels: [],
        datasets: [
          {
            label: 'Products',
            data: [],
            backgroundColor: 'rgba(255, 99, 132, 0.7)',
          }
        ],
      });

  useEffect(() => {
    websocket.onmessage = (event) => {
      const payload = JSON.parse(event.data);
      const payload_json = JSON.parse(payload);
      const this_product = payload_json["PRODUCT_NAME"];
      const this_total = payload_json["MOVING_INVENTORY"];

      if (!horizontal_labels.includes(this_product)){
          horizontal_labels.push(this_product)
          setLabels(horizontal_labels);
      }
      data_points[this_product] = this_total
      console.log(`this_product = ${this_product}`)
      console.log(`this_total = ${this_total}`)
      setDataPoints(data_points);

      setBarState({
        labels: horizontal_labels,
        datasets: [
          {
            label: 'Products',
            data: horizontal_labels.map((f) => data_points[f]),
            backgroundColor: 'rgba(255, 99, 132, 0.7)',
          }
        ],
      });

      console.log(horizontal_labels);
      console.log(payload_json);

    };

  }, [websocket]);

  return <Bar options={options} data={barState} />;
}