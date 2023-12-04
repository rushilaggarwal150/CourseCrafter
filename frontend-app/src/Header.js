// Header.js
import React from 'react';
import './Header.css';
import { Button } from './Button';

const Header = () => {

  const handleRefreshClick = () => {
    window.location.reload(true);
  }; 

  return (
    <div className="header">
      <h1>CourseCrafter.</h1>
      <div className='navBarBtn'>
        <Button buttonStyle="btn--outline" buttonSize="btn--medium" onClick={handleRefreshClick}>Start Over</Button>
      </div>
    </div>
  );
};

export default Header;
