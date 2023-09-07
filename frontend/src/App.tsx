import "./App.css";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import { CssBaseline } from "@mui/material";
import { createContext, useMemo, useState } from "react";
import { getDesignTokens } from "./themes/themes";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

import HomePage from "./pages/Home/HomePage";
import LoginPage from "./pages/auth/Login/LoginPage";
import ModulesPage from "./pages/user/Modules/ModulesPage";
import StatsPage from "./pages/user/Stats/StatsPage";
import WordListPage from "./pages/user/Words/WordsPage";
import RegisterPage from "./pages/auth/Register/RegisterPage";
import ResetPasswordPage from "./pages/auth/ResetPassword/ResetPasswordPage";
import EmailVerificationPage from "./pages/auth/EmailVerification/EmailVerificationPage";
import NotFoundPage from "./pages/error/NotFoundPage";
import { useSelector } from "react-redux";
import { authState } from "./store/store";
import { Navigate } from "react-router-dom";
import CreateWordPage from "./pages/user/CreateWord/CreateWordPage";

export const ColorModeContext = createContext({ toggleColorMode: () => {} });

// Application
function App() {
  const isAuth = useSelector((state: authState) => state.token);
  return (
    <>

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
          <Route
            path="/word-list/:user_id/create-word"
            element={isAuth ? <CreateWordPage /> : <Navigate to={"/"} />}
          >
          </Route>
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
