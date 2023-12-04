import React from 'react';
import './Card.css'; 

const CourseCard = ({ num, course }) => {
  return (
    <div className='course-card'>
        <div className='course-number'>
        {num + 1}. CSCE {course.course_name}
        </div>
        <div className='course-details'>
        {course.description}
        <div className='course-difficulty'>Difficulty: {course.difficulty}</div>
        <div className='course-relevance'>Relevance: {course.relevance.toFixed(2)}</div>
        </div>
  </div>
  );
};

export default CourseCard;
