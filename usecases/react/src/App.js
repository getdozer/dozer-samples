import './App.css';
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Airports from "./components/airports";
import { AirportsWrapper } from "./components/airportsWrapper";
import { DozerProvider } from "@dozerjs/dozer-react";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src="/logo.svg" className="App-logo" alt="logo" />
        <DozerProvider value={{
          serverAddress: 'http://localhost:62998',
        }}>
          <BrowserRouter>
            <Routes>
              <Route index element={<Airports />} />
              <Route element={<AirportsWrapper />} path={"/airports"} />
            </Routes>
          </BrowserRouter>
        </DozerProvider>
      </header>
    </div>
  );
}

export default App;
