import { DozerProvider } from "@dozerjs/dozer-react";
import { Performance } from "../components/Performance";
import { PageView } from "../components/PageView";
import { Box, CircularProgress } from "@mui/material";
import { useTimeout } from "ahooks";
import { useState } from "react";

export function Monitor () {
  const [ loading, setLoading ] = useState(true);
  useTimeout(() => {
    setLoading(false);
  }, 1000)

  if (loading) {
    return (
      <Box sx={{ display: 'flex', height: '100%', justifyContent: 'center', alignItems: 'center' }}>
        <CircularProgress />
      </Box>
    )
  }
  return (
    <DozerProvider value={{
      serverAddress: 'http://127.0.0.1:62998',
    }}>
      <Box sx={{ display: 'flex', flexDirection: 'column', gap: '1rem', overflow: 'overlay' }}>
        <Performance />
        <PageView />
      </Box>
    </DozerProvider>
  )
}
