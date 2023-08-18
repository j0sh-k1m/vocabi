import "./App.css";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import { CssBaseline } from "@mui/material";
import { createContext, useMemo, useState } from "react";
import { getDesignTokens } from "./themes/themes";

const loggedIn = true;

export const ColorModeContext = createContext({ toggleColorMode: () => {} });

// Application
function App() {
  return <>{loggedIn ? <HomePage></HomePage> : <LoginPage></LoginPage>}</>;
}

// Component to handle themes 
const ToggleColorMode = () => {
  // store color mode state
  const [mode, setMode] = useState<"light" | "dark">("light");

  // toggle the color mode
  const colorMode = useMemo(
    () => ({
      toggleColorMode: () => {
        setMode((prevMode) => (prevMode === "light" ? "dark" : "light"));
      },
    }),
    []
  );

  // Create theme
  const theme = useMemo(() => createTheme(getDesignTokens(mode)), [mode]);

  return (
    <ColorModeContext.Provider value={colorMode}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <App />
      </ThemeProvider>
    </ColorModeContext.Provider>
  );
};

export default ToggleColorMode;
