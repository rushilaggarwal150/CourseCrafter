// CourseCarousel.js
import React, { useState } from 'https://cdn.skypack.dev/react';
import { TiChevronLeftOutline, TiChevronRightOutline } from 'https://cdn.skypack.dev/react-icons/ti';
import CourseCard from './Card';

const MAX_VISIBILITY = 3;

const CourseCarousel = ({ courses }) => {
  const [active, setActive] = useState(2);
  const count = courses.length;

  return (
    <div className='carousel'>
      {active > 0 && (
        <button className='nav left' onClick={() => setActive(i => i - 1)}>
          <TiChevronLeftOutline />
        </button>
      )}
      {courses.map((course, i) => (
        <div
          key={i}
          className='card-container'
          style={{
            '--active': i === active ? 1 : 0,
            '--offset': (active - i) / 3,
            '--direction': Math.sign(active - i),
            '--abs-offset': Math.abs(active - i) / 3,
            'pointer-events': active === i ? 'auto' : 'none',
            'opacity': Math.abs(active - i) >= MAX_VISIBILITY ? '0' : '1',
            'display': Math.abs(active - i) > MAX_VISIBILITY ? 'none' : 'block',
          }}
        >
          <CourseCard course={course} />
        </div>
      ))}
      {active < count - 1 && (
        <button className='nav right' onClick={() => setActive(i => i + 1)}>
          <TiChevronRightOutline />
        </button>
      )}
    </div>
  );
};

export default CourseCarousel;
