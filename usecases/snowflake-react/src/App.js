import './App.css';
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Customers from "./components/customers";
import Customer from "./components/customer";
import Orders from "./components/orders";
import { DozerProvider } from "@dozerjs/dozer-react";
import { DOZER_APP_ID } from "./config";
import { AUTH_TOKEN } from "./config";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <a href={"/"}><img src="https://getdozer.io/img/logo.svg" className="App-logo" alt="logo" /></a>
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
              <Route index element={<Customers />} />
              <Route element={<Orders />} path={"/orders"} />
              <Route element={<Customer />} path={"/customer/:key"} />
            </Routes>
          </BrowserRouter>
        </DozerProvider>
      </header>
    </div>
  );
}

export default App;
