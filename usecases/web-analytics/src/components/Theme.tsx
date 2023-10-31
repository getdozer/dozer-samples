
import {
  ThemeOptions,
  createTheme,
  SimplePaletteColorOptions,
} from "@mui/material/styles";


const darkThemeOptions : ThemeOptions = {
  typography: {
      allVariants: {
          fontSize: '14px'
      },
      fontSize: 14,
      fontFamily: [
          '-apple-system',
          'BlinkMacSystemFont',
          '"Segoe UI"',
          'Roboto',
          '"Helvetica Neue"',
          'Arial',
          'sans-serif',
          '"Apple Color Emoji"',
          '"Segoe UI Emoji"',
          '"Segoe UI Symbol"',
      ].join(','),
      h1 : {
          fontSize: '40px',
          fontWeight: 700,
      },
      h2: {
          fontSize: '36px',
          fontWeight: 700,
      },
      h3: {
          fontSize: '24px',
          fontWeight: 700,
      },
      h4: {
          fontSize: '20px',
          fontWeight: 700,
      },
      h5: {
          fontSize: '18px',
          fontWeight: 500,
      },
      h6: {
          fontSize: '12px',
          fontWeight: 700,
          color: 'hsl(210, 12%, 40%)'
      },
      button: {
          fontWeight: 600,
          textTransform: 'uppercase',
          fontSize: '14px'
      }
  },
  palette: {
    mode: "dark",
    primary: {
      main: "#A73D82",
      light: "#A63880",
      dark: "#871861",
    },
    secondary: {
      main: "#5865F2",
    },
    success: {
      main: "#31C632",
    },
    error: {
      main: "#FF6666",
    },
    text: {
      primary: "#FFFFFF",
      secondary: "hsl(210, 12%, 45%)",
      disabled: "hsl(210, 12%, 22%)",
    },
    background: {
      default: "#10151A",
      paper: "#1B232C",
    },
    grey: {
      "50": "hsl(213, 26%, 26%)",
      "100": "hsl(213, 26%, 24%)",
      "200": "hsl(213, 26%, 22%)",
      "300": "hsl(213, 26%, 20%)",
      "400": "hsl(213, 26%, 18%)",
      "500": "hsl(213, 26%, 16%)",
      "600": "hsl(213, 26%, 14%)",
      "700": "hsl(213, 26%, 12%)",
      "800": "hsl(213, 26%, 10%)",
      "900": "hsl(213, 26%, 8%)",
      "A100": "hsl(210, 12%, 30%)",
      "A200": "hsl(210, 12%, 40%)",
      "A400": "hsl(210, 12%, 50%)",
      "A700": "hsl(210, 12%, 60%)"
    }
  }
};

darkThemeOptions.components = {
  MuiButton: {
      styleOverrides : {
          root : {
              borderRadius: "30px",
              padding: '5px 20px 5px 20px',
          }
      }
  },
  MuiTab : {
      styleOverrides : {
          root : {
              fontSize: '14px',
              textTransform: 'none',
              color: darkThemeOptions.palette?.grey?.A200,
              fontWeight: 500
          }
      }
  },
  MuiSelect : {
      styleOverrides : {
          root : {
              background: darkThemeOptions.palette?.background?.paper
          }
      }
  },
  MuiTooltip : {
      styleOverrides : {
          tooltip : {
              backgroundColor: darkThemeOptions.palette?.grey?.[300],
              fontSize: '12px'
          }
      }
  },

  MuiDivider : {
      styleOverrides : {
          root : {
              border: '0px',
              height: '1px',
              background: darkThemeOptions.palette?.grey?.[700],
              filter: `drop-shadow(0px -1px 0px ${darkThemeOptions.palette?.grey?.[400]})`
          }
      }
  },

  MuiPaginationItem : {
      styleOverrides : {
          root : {
              backgroundColor: darkThemeOptions.palette?.background?.paper,
              color: darkThemeOptions.palette?.grey?.A200,
              '&:hover': {
                  backgroundColor: darkThemeOptions.palette?.grey?.[400]
              },
              '&.Mui-selected': {
                  backgroundColor: (darkThemeOptions.palette?.primary as SimplePaletteColorOptions).main,
                  color: darkThemeOptions.palette?.text?.primary,
                  '&:hover' : {
                      backgroundColor: (darkThemeOptions.palette?.primary as SimplePaletteColorOptions).main,
                      color: darkThemeOptions.palette?.text?.primary
                  }
              }
          }
      }
  },
};


export const darkTheme = createTheme(darkThemeOptions);


