import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Tab from '@mui/material/Tab';
import Tabs from '@mui/material/Tabs';
import Toolbar from '@mui/material/Toolbar';
import * as React from 'react';
import { Link, useLocation } from 'react-router-dom';

export function NavBar() {
  const routes = [
    {
      label: 'Home',
      path: '/',
    },
    {
      label: 'Config',
      path: '/config',
    },
    {
      label: 'Schema',
      path: '/schema',
    },
  ];
  const location = useLocation();
  const index = routes.findIndex((route) => route.path === location.pathname);

  const [active, setActive] = React.useState<number>(index);


  return (
    <AppBar position="static">
      <Toolbar sx={{ gap: '2rem' }}>
        <img src="/logo.svg" alt="Dozer" width={137} height={40} />
        <Box sx={{ flexGrow: 1, display: 'flex' }}>
          <Tabs value={active} onChange={(_, val) => setActive(val)} sx={{

          }}>
            <Tab component={Link} label="Home" to="/" />
            <Tab component={Link} label="Config" to="/config" />
            <Tab component={Link} label="Schema" to="/schema" />
          </Tabs>
        </Box>
      </Toolbar>
    </AppBar>
  );
}
