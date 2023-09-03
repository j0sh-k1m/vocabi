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
import NotFoundPage from "./pages/error/NotFoundPage";
import { useSelector } from "react-redux";
import { authState } from "./store/store";
import { Navigate } from "react-router-dom";

export const ColorModeContext = createContext({ toggleColorMode: () => {} });

// Application
function App() {
  const isAuth = useSelector((state: authState) => state.token);
  return (
    <>
      {/* { loggedIn ? <HomePage></HomePage> : <LoginPage></LoginPage>} */}

      <Router>
        {/* <HomePage></HomePage> */}
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route
            path="/user-modules/:user_id"
            element={isAuth ? <ModulesPage /> : <Navigate to={"/"} />}
          />
          <Route
            path="/stat/:user_id"
            element={isAuth ? <StatsPage /> : <Navigate to={"/"} />}
          />
          <Route
            path="/word-list/:user_id"
            element={isAuth ? <WordListPage /> : <Navigate to={"/"} />}
          />
          <Route path="/auth/login" element={<LoginPage />} />
          <Route path="/auth/register" element={<RegisterPage />} />
          <Route
            path="/auth/password/reset"
            element={isAuth ? <ResetPasswordPage /> : <Navigate to={"/"} />}
          />
          <Route
            path="/auth/email-verification"
            element={<EmailVerificationPage />}
          />
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </Router>
    </>
  );
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
