import React, { useState } from 'react';
import './Form.css';
import { Button } from './Button';

const TypingForm = ({ onInputChange, onSubmit }) => {
  const [inputValue, setInputValue] = useState('');

  const handleInputChangeLocal = (event) => {
    const value = event.target.value;
    setInputValue(value);
    onInputChange(value); // Notify the parent component about the input change
  };

  const handleSubmit = () => {
    // You can perform any actions needed on form submission
    // For example, you can call the onSubmit prop passed from the parent component
    onSubmit();
  };

  return (
    <div className='form-div'>
      <h2>What are you interested in?</h2>
      <form>
        <textarea
          value={inputValue}
          onChange={handleInputChangeLocal}
          placeholder="Start typing..."
        />
      </form>
      <Button buttonSize={"btn--large"} onClick={handleSubmit}>Submit</Button>
    </div>
  );
};

export default TypingForm;
