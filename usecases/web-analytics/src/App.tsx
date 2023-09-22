import Box from "@mui/material/Box";
import { ThemeProvider } from "@mui/material/styles";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { DozerProvider } from "@dozerjs/dozer-react";
import { NavBar } from "./components/NavBar";
import { darkTheme } from "./components/Theme";
import { Home } from './routes/Home';
import { Config } from "./routes/Config";
import { Schema } from "./routes/Schema";
import { Performance } from "./components/Performance";
import { PageView } from "./components/PageView";

function App() {
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
              <Box sx={{ flex: '3', minWidth: 0 }}>
                <DozerProvider value={{
                  serverAddress: 'http://127.0.0.1:62998',
                }}>
                  <Box sx={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                    <Performance />
                    <PageView />
                  </Box>
                </DozerProvider>
              </Box>
            </Box>
          </Box>
        </Box>
      </BrowserRouter>
    </ThemeProvider>
  );
}

export default App;
