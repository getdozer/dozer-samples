import './App.css';
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Login from "./components/login";
import Orders from "./components/orders";
import Temperature from "./components/temperature";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src="https://getdozer.io/img/logo.svg" className="App-logo" alt="logo" />
        <BrowserRouter>
          <Routes>
            <Route element={<Login />} path={"/login"} />
            <Route element={<Orders />} path={"/orders/:jwt"} />
            <Route index element={<Temperature />} path={"/"} />
          </Routes>
        </BrowserRouter>
      </header>
    </div>
  );
}

export default App;
