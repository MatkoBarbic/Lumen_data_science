import background from './images/croatia-satellite-map.jpg'
import './App.css';
import { Route, Router, Routes, BrowserRouter } from 'react-router-dom';
import { Switch } from 'react-router';
import Home from './components/Home';
import Guess from './components/Guess';

function App() {
  return (
    <>
      <img src={background} alt="Map of Croatia" className='background'></img>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />}></Route>
          <Route path="/guess" element={<Guess />}></Route>
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
