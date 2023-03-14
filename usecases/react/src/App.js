import './App.css';
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Airports from "./components/airports";
import { AirportsWrapper } from "./components/airportsWrapper";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src="https://getdozer.io/img/logo.svg" className="App-logo" alt="logo" />
        <BrowserRouter>
          <Routes>
            <Route index element={<Airports />} />
            <Route element={<AirportsWrapper />} path={"/airports"}/> />
          </Routes>
        </BrowserRouter>
      </header>
    </div>
  );
}

export default App;
