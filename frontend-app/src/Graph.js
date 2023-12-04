// Graph.js
import React from 'react';
import Plot from 'react-plotly.js';
import './Graph.css';

const layout = {
  title: 'Suggested Courses',
  showlegend: false,
  xaxis: {
    title: {
      text: 'Difficulty',
      font: {
        size: 18,
        color: '#7f7f7f'
      }
    },
  },
  yaxis: {
    title: {
      text: 'Relevance',
      font: {
        size: 18,
        color: '#7f7f7f'
      }
    }
  }
};

// Function to insert line breaks after every 10 words

const Graph = ({ incomingData }) => {
  var x = [],
    y = [],
    t = [],
    colors = [];

  for (var i = 0; i < incomingData.length; i++) {
    var row = incomingData[i];
    y.push(row.relevance);
    x.push(row.difficulty);
    t.push({ name: row.course_name, description: row.description });
    colors.push(row.difficulty > 3 ? '#2C2C54' : '#474787');
  }

  console.log(x)

  const graphData = [
    {
      x: x,
      y: y,
      mode: 'markers',
      type: 'scatter',
      marker: { size: 12, color: colors },
      text: t,
      hovertemplate:
        '<b>%{text.name}</b><br>' +
        '<br>Difficulty: %{x}<br>' +
        'Relevance: %{y}<br>' +
        'Description: %{text.description}<extra></extra>',
    },
  ];
  return (
    <div className='graph-container'>
      <Plot data={graphData} layout={layout} />
    </div>
  );
};

export default Graph;
