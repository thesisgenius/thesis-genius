export function Button({ children, className = '', ...props }) {
    return (
        <button
            className={`px-4 py-2 rounded-lg bg-blue-500 text-white hover:bg-blue-600 focus:ring-2 focus:ring-blue-300 focus:outline-none ${className}`}
            {...props}
        >
            {children}
        </button>
    );
}