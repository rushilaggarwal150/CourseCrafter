import React from 'react';
import './Loading.css'; 

const Loading = () => {
  return (
    <div className='loading'>
      <div className='loading-text'> 
        Loading<span className='dot-1'>.</span><span className='dot-2'>.</span><span className='dot-3'>.</span>
      </div>
    </div>
  );
};

export default Loading; // Exporting the Loading component for use in other modules