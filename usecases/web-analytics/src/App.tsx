import Box from "@mui/material/Box";
import { ThemeProvider } from "@mui/material/styles";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { NavBar } from "./components/NavBar";
import { darkTheme } from "./components/Theme";
import { usePerformance } from "./hooks/usePerformance";
import { Config } from "./routes/Config";
import { Home } from './routes/Home';
import { Monitor } from "./routes/Monitor";
import { Schema } from "./routes/Schema";


function App() {
  usePerformance();
  return (
    <ThemeProvider theme={darkTheme}>
      <BrowserRouter>
        <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
          <NavBar />
          <Box sx={{flex: '1', minHeight: '0'}}>
            <Box sx={{ height: '100%', display: 'flex', gap: '1rem', padding: '1rem', boxSizing: 'border-box' }}>
              <Box sx={{ flex: '2', minWidth: 0 }}>
                <Routes>
                  <Route index element={<Home />} />
                  <Route element={<Config />} path={"/config"} />
                  <Route element={<Schema />} path={"/schema"} />
                </Routes>
              </Box>
              <Box sx={{ flex: '3', minWidth: 0, height: '100%', overflow: 'overlay' }}>
                <Monitor />
              </Box>
            </Box>
          </Box>
        </Box>
      </BrowserRouter>
    </ThemeProvider>
  );
}

export default App;
