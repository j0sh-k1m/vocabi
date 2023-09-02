import "./App.css";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import { CssBaseline } from "@mui/material";
import { createContext, useMemo, useState } from "react";
import { getDesignTokens } from "./themes/themes";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

import HomePage from "./pages/HomePage";
import LoginPage from "./pages/auth/LoginPage";
import ModulesPage from "./pages/users/ModulesPage";
import StatsPage from "./pages/users/StatsPage";
import WordListPage from "./pages/users/WordListPage";
import RegisterPage from "./pages/auth/RegisterPage";
import ResetPasswordPage from "./pages/auth/ResetPasswordPage";
import EmailVerificationPage from "./pages/auth/EmailVerificationPage";

const loggedIn = true;

export const ColorModeContext = createContext({ toggleColorMode: () => {} });

// Implement the login page 

// Application
function App() {
  return <>
  {/* { loggedIn ? <HomePage></HomePage> : <LoginPage></LoginPage>} */}

    <Router>
      {/* <HomePage></HomePage> */}
      <Routes>
        <Route path="/" Component={HomePage}/>
        <Route path="/user-modules/:user_id" Component={ModulesPage} />
        <Route path="/stat/:user_id" Component={StatsPage} />
        <Route path="/word-list/:user_id" Component={WordListPage} />
        <Route path="/auth/login" Component={LoginPage}/>
        <Route path="/auth/register" Component={RegisterPage} />
        <Route path="/auth/password/reset" Component={ResetPasswordPage} />
        <Route path="/auth/email-verification" Component={EmailVerificationPage} /> 
      </Routes>
    </Router>

    </>;
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
