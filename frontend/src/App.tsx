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
import { AuthState } from "./store/store";
import { Navigate } from "react-router-dom";
import CreateWordPage from "./pages/user/CreateWord/CreateWordPage";
import ExecuteModulePage from "./pages/user/ExecuteModule/ExecuteModulePage";
import CreateNewPasswordPage from "./pages/auth/CreateNewPassword/CreateNewPasswordPage";

export const ColorModeContext = createContext({ toggleColorMode: () => {} });

// Application
function App() {
  const isAuth = useSelector((state: AuthState) => state.token);
  return (
    <>
      <Router>
        <Routes>
          {/* Starting Page */}
          <Route path="/" element={<HomePage />} />

          {/* Login Page */}
          <Route path="/auth/login" element={<LoginPage />} />

          {/* Register Page */}
          <Route path="/auth/register" element={<RegisterPage />} />

          {/* Email Verification Page */}
          <Route
            path="/auth/email-verification"
            element={<EmailVerificationPage />}
          />

          {/* Reset Password Page */}
          <Route path="/auth/password/reset" element={<ResetPasswordPage />} />

          {/* Create New Password */}
          <Route
            path="/auth/password/create-new"
            element={<CreateNewPasswordPage />}
          />

          {/* User Modules Page */}
          <Route
            path="/user-modules/:user_id"
            element={isAuth ? <ModulesPage /> : <Navigate to={"/"} />}
          />

          {/* Execute Module Page */}
          <Route
            path="/user-modules/:user_id/modules"
            element={isAuth ? <ExecuteModulePage /> : <Navigate to={"/"} />}
          />

          {/* User Stats Page */}
          <Route
            path="/stat/:user_id"
            element={isAuth ? <StatsPage /> : <Navigate to={"/"} />}
          />

          {/* User Word List Page */}
          <Route
            path="/word-list/:user_id"
            element={isAuth ? <WordListPage /> : <Navigate to={"/"} />}
          />

          {/* Create Word Page */}
          <Route
            path="/word-list/:user_id/create-word"
            element={isAuth ? <CreateWordPage /> : <Navigate to={"/"} />}
          ></Route>

          {/* Url Not Found Page */}
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
