import './App.css';
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { DozerProvider } from '@dozerjs/dozer-react';
import Customers from "./components/customers";
import Customer from "./components/customer";
import Orders from "./components/orders";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <a href={"/"}><img src="/logo.svg" className="App-logo" alt="logo" /></a>
        <DozerProvider>
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
