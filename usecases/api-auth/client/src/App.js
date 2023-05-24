import './App.css';
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Login from "./components/login";
import Orders from "./components/orders";
import Temperature from "./components/temperature";
import Dashboard from "./components/admin/dashboard";
import Movies from "./components/public/movies";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src="https://getdozer.io/img/logo.svg" className="App-logo" alt="logo" />
        <BrowserRouter>
          <Routes>
            <Route element={<Login />} path={"/admin"} />
            <Route index element={<Movies />} path={"/"} />
            <Route element={<Dashboard />} path={"/admin/dashboard"} />
          </Routes>
        </BrowserRouter>
      </header>
    </div>
  );
}

export default App;
