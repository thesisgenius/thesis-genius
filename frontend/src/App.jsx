import { Outlet, useLocation } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';

const App = () => {
    const location = useLocation();
    const showHeaderFooter = !location.pathname.includes('/app');

    return (
        <>
            {showHeaderFooter && <Header />}
            <Outlet />
            {showHeaderFooter && <Footer />}
        </>
    );
};

export default App;
