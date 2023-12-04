import React, { useState, useEffect, useRef } from 'react';
import Header from './Header';
import TypingForm from './Form';
import Plot from 'react-plotly.js';
import './Graph.css';
import Loading from './Loading';
import Footer from './Footer';
import CourseCard from './Card';

const App = () => {
  const [data, setData] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [formSubmitted, setFormSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);
  const [showScrollButton, setShowScrollButton] = useState(false);

  const textContainerRef = useRef();

  const fetchData = async () => {
    try {
      setLoading(true);

      const response = await fetch('http://127.0.0.1:5000/process_user_input', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_input: inputValue }),
      });

      if (response.ok) {
        const result = await response.json();
        setData(result);
      } else {
        console.error('Failed to fetch data:', response.status);
      }
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (value) => {
    setInputValue(value);
  };

  const handleFormSubmit = () => {
    setFormSubmitted(true);
  };

  useEffect(() => {
    if (formSubmitted) {
      fetchData();
      setFormSubmitted(false);
    }
  }, [formSubmitted]);

  useEffect(() => {
    const handleScroll = () => {
      const textContainer = textContainerRef.current;
      var isAboveTextContainer = false;
      if(textContainer){
        isAboveTextContainer = window.scrollY < (textContainer.offsetTop || Infinity);
      }
      
      setShowScrollButton(isAboveTextContainer);
    };

    window.addEventListener('scroll', handleScroll);

    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, []);

  const scrollToTextContainer = () => {
    const textContainerTop = textContainerRef.current.offsetTop;
    window.scrollTo({ top: textContainerTop, behavior: 'smooth' });
  };

  const sortedData = [...data].sort((a, b) => b.relevance - a.relevance);
  const top5RelevantCourses = sortedData.slice(0, 5);

  const plotData = {
    x: data.map((entry) => entry.difficulty),
    y: data.map((entry) => entry.relevance.toFixed(2)),
    mode: 'markers',
    type: 'scatter',
    marker: { size: 10, color: '#2C2C54' },
    text: data.map((entry) => `CSCE ${entry.course_number} - ${entry.course_name}`),
  };

  const graphLayout = {
    title: 'Suggested Courses',
    showlegend: false,
    xaxis: {
      title: {
        text: 'Difficulty',
        font: {
          size: 18,
          color: '#7f7f7f',
        },
      },
    },
    yaxis: {
      title: {
        text: 'Relevance',
        font: {
          size: 18,
          color: '#7f7f7f',
        },
      },
    },
  };

  return (
    <div className="App">
      {/* <header className="App-header"> */}
        <Header />
        <TypingForm onInputChange={handleInputChange} onSubmit={handleFormSubmit} />
        <div className='graph-container'>
          {loading ? (
            <Loading />
          ) : (
            <Plot
              data={[plotData]}
              layout={graphLayout}
            />
          )}
          {top5RelevantCourses.length > 1 && (
            <div className='text-container' ref={textContainerRef}>
              <h2>Most relevant courses</h2>
              {top5RelevantCourses.map((entry, index) => (
                <CourseCard num={index} course={entry} />
              ))}
            </div>
          )}
        </div>
        {showScrollButton && (
          <button className='scroll-button' onClick={scrollToTextContainer}>
            &#x2193;
          </button>
        )}
      <Footer />
    
    </div>
  );
};

export default App;
