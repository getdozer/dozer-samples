import Box from "@mui/material/Box";
import { ThemeProvider } from "@mui/material/styles";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { NavBar } from "./components/NavBar";
import { darkTheme } from "./components/Theme";
import { Home } from './routes/Home';
import { Config } from "./routes/Config";
import { Schema } from "./routes/Schema";

function App() {
  return (
    <ThemeProvider theme={darkTheme}>
      <BrowserRouter>
        <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
          <NavBar />
          <Box sx={{flex: '1', minHeight: '0'}}>
            <Box sx={{ height: '100%', display: 'flex' }}>
              <Box sx={{ flex: '1' }}>
                <Routes>
                  <Route index element={<Home />} />
                  <Route element={<Config />} path={"/config"} />
                  <Route element={<Schema />} path={"/schema"} />
                </Routes>
              </Box>
              <Box sx={{ flex: '1' }}>

              </Box>
            </Box>
          </Box>
        </Box>
      </BrowserRouter>
    </ThemeProvider>
  );
}

export default App;
