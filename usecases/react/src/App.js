import './App.css';
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Airports from "./components/airports";
import { AirportsWrapper } from "./components/airportsWrapper";
import { DozerProvider } from "@dozerjs/dozer-react";
import { DOZER_APP_ID } from "./config";
import { AUTH_TOKEN } from "./config";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src="https://getdozer.io/img/logo.svg" className="App-logo" alt="logo" />
        <DozerProvider value={{
          serverAddress: 'https://data.dev.getdozer.io:443',
          authToken: AUTH_TOKEN,
          headers:
          {
            'X-Dozer-App-Id': DOZER_APP_ID
          }
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
