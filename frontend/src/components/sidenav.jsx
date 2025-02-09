import React, { useState } from 'react';
import '../styles/sidenav.css';
import AllPages from '../pages/AllPages';

const SideNav = () => {
  const [isOpen, setIsOpen] = useState(false);
  const sideNavWidth = '250px'; // Width of the side nav

  const toggleNav = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div>

      <button className="openbtn" onClick={toggleNav}> &#9776;</button>

      {/* Side Navigation */}
        <div className={`sidenav ${isOpen ? 'open' : ''}`} style={{ width: sideNavWidth }}>

            <h2>Pages</h2>

            <a href="#Page1">Title</a>
            <a href="#Page2">Copywrite</a>
            <a href="#Page3">Signature</a>
            <a href="#Page4">Abstract</a>
            <a href="#Page5">Dedication</a>
            <a href="#Page6">Ackknowledgements</a>


        </div>


      {/* Main Content Area */}
        <div className="content" style={{ marginLeft: isOpen ? sideNavWidth : '0' }}>

        <AllPages />

        </div>
    </div>
  );
};

export default SideNav;
