import React, { useState, useEffect } from "react";

const FadingBanner = () => {
    const messages = [
        "This will be the first key point about the selected section!",
        "This will be the second key point about the selected section!",
        "This will be the third key point about the selected section!",
    ];

    const [currentMessageIndex, setCurrentMessageIndex] = useState(0);

    useEffect(() => {
        const interval = setInterval(() => {
            setCurrentMessageIndex((prevIndex) => (prevIndex + 1) % messages.length);
        }, 3000); // Change message every 3 seconds

        return () => clearInterval(interval);
    }, [messages.length]);

    return (
        <div className="fading-banner">
            <p key={currentMessageIndex} className="fade">
                {messages[currentMessageIndex]}
            </p>
        </div>
    );
};

export default FadingBanner;