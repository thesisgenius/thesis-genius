import React, { useState } from 'react';

const Box5Text = () => {
    const [value, setValue] = useState('');
  
    const handleChange = (e) => {
      setValue(e.target.value);
    };
  
    return (

    <div id="Page5">
        <h2>Dedication:</h2>
        <div class="box">
            <div id="Dedication">Dedication</div>
            <div id="Ded-to">This dissertation is dedicated to</div>
            <textarea id="textarea51" value={value} onChange={handleChange} 
                style={{
                minHeight: '100px',
                resize: 'vertical', // Allows resizing vertically
                }}
                placeholder="my therapist / mom / dog / editor / hamster / favorite analyst / favorite deity. This page is optional. You can say whatever you want, it’s your dissertation. Just keep it clean.">
            </textarea>
        </div>
    </div>

    );
};

export default Box5Text;