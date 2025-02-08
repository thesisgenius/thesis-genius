import React, { useState } from 'react';

const Box6Text = () => {
    const [value, setValue] = useState('');
  
    const handleChange = (e) => {
      setValue(e.target.value);
    };
  
    return (

    <div id="Page6">
        <h2>Acknowledgements:</h2>
        <div class="box">
                <div id="Acknowledgements">Acknowledgements</div>
                <textarea id="textarea61" value={value} onChange={handleChange} 
                    style={{
                    minHeight: '100px',
                    resize: 'vertical', // Allows resizing both horizontally and vertically
                    }}
                    placeholder="This page is also optional, and you can format it any way you want. Since this is the appropriate place to thank anyone who helped you, inspired you, and/or put up with you throughout the dissertation process, think carefully about who you might like to explicitly appreciate.">
                </textarea>
        </div>
    </div>

    );
};

export default Box6Text;