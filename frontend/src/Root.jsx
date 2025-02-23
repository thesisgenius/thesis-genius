import React, { useState } from "react";
import { AuthProvider } from "./context/AuthContext";
import App from "./App";

const Root = () => {
    const [refreshCount, setRefreshCount] = useState(0);

    // Function to increment the refresh count, forcing reinitialization of the App component
    const incrementRefreshCount = () => setRefreshCount((prevCount) => prevCount + 1);

    return (
        <AuthProvider refreshApp={incrementRefreshCount}>
            <App key={refreshCount} />
        </AuthProvider>
    );
};

export default Root;
