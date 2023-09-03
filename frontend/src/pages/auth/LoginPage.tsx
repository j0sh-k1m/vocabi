import { AccountBoxOutlined, LockPersonOutlined } from "@mui/icons-material";
import {
  Box,
  Button,
  Grid,
  InputAdornment,
  TextField,
  Typography,
} from "@mui/material";
import { ChangeEvent, useState } from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import { useTheme } from "@mui/material";
import { getDesignTokens } from "../../themes/themes";
import { authActions } from "../../store/store";
import { useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";

const LoginPage = () => {
  const theme = useTheme();
  const { palette } = getDesignTokens(theme.palette.mode);

  const dispatch = useDispatch(); 
  const navigate = useNavigate(); 

  const [loginError, setLoginError] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");

  const handleEmailChange = (event: ChangeEvent<HTMLInputElement>) => {
    const emailInput = event.target.value;
    setEmail(emailInput);
  };

  const handlePasswordChange = (event: ChangeEvent<HTMLInputElement>) => {
    const passwordInput = event.target.value;
    setPassword(passwordInput);
  };

  const handleLoginSubmission = () => {
    if (!(email && password)) {
      return 
    }

    const data = {
      email: email,
      password: password,
    };

    // Change this to api endpoint
    axios
      .post("http://127.0.0.1:8080/auth/login", data, {
        headers: { "Content-Type": "application/json" },
      })
      .then((response) => {
        console.log("API Response:", response.data);
        dispatch(authActions.setEmail({ email: response.data.user.email }))
        dispatch(authActions.setUserId({ user_id: response.data.user.user_id }))
        dispatch(authActions.setFirstName({ first_name: response.data.user.first_name }))
        dispatch(authActions.setLastName({ last_name: response.data.user.last_name }))
        dispatch(authActions.setToken({ token: response.data.token }))
        navigate(`/user-modules/${response.data.user.user_id}`)
      })
      .catch((error) => {
        setLoginError(error.response.data.message);
      });
  };

  return (
    <Grid container justifyContent="center" alignItems="center" height="90vh">
      <Box
        boxShadow={2}
        p={3}
        width={{ xs: "60%", sm: "80%", md: "100%", lg: "130%", xl: "150%" }} // Responsive width
        bgcolor="white"
        borderRadius={4}
        sx={{
          minHeight: "40vh",
          minWidth: "17vw",
          padding: "40px",
          display: "flex",
          flexDirection: "column",
        }} // Taller box
      >
        <Typography variant="h4" gutterBottom fontWeight={"bold"}>
          Login
        </Typography>
        <TextField
          label="Email"
          fullWidth
          margin="normal"
          variant="standard"
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <AccountBoxOutlined />
              </InputAdornment>
            ),
          }}
          onChange={handleEmailChange}
        />
        <TextField
          label="Password"
          fullWidth
          margin="normal"
          type="password"
          variant="standard"
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <LockPersonOutlined />
              </InputAdornment>
            ),
          }}
          onChange={handlePasswordChange}
        />
        <Button
          variant="contained"
          fullWidth
          color="primary"
          sx={{ mt: 2, borderRadius: "10px" }}
          onClick={handleLoginSubmission}
        >
          Login
        </Button>
        {loginError && (
          <Box>
            <Typography variant="body2" sx={{ mt: 2, color: "red" }}>
              {loginError}
            </Typography>
          </Box>
        )}
        <Box sx={{ mt: "auto", alignSelf: "flex-end-center" }}>
          <Typography variant="body2" sx={{ mt: 2 }}>
            Don't have an account?{" "}
            <Link to={"/auth/register"} style={{ color: palette.niceBlue }}>
              Sign Up
            </Link>
          </Typography>
          <Typography variant="body2" sx={{ mt: 1 }}>
            Forgot your password?{" "}
            <Link to={"/password/reset"} style={{ color: palette.niceBlue }}>
              Reset Password
            </Link>
          </Typography>
        </Box>
      </Box>
    </Grid>
  );
};

export default LoginPage;
