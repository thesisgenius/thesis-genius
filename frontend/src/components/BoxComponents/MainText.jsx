import React, { useState } from 'react';

const MainText = () => {
    const [value, setValue] = useState('');
  
    const handleChange = (e) => {
      setValue(e.target.value);
    };
  
    return (

    <div className="Body">
        <h2>Body:</h2>
        <div class="box">
                <div class="Title-placeholder">Level 1 Title</div>
                <textarea class="textarea-body" value={value} onChange={handleChange} 
                    style={{
                    minHeight: '100px',
                    resize: 'vertical', // Allows resizing both horizontally and vertically
                    }}
                    placeholder="Type main text here...">
                </textarea>
        </div>
    </div>

    );
};

export default MainText;