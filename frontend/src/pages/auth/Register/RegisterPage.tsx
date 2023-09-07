import { useTheme } from "@mui/material";
import {
  AccountBoxOutlined,
  AlternateEmailOutlined,
  LockPersonOutlined,
} from "@mui/icons-material";
import {
  Typography,
  Box,
  Button,
  Grid,
  TextField,
  InputAdornment,
} from "@mui/material";
import { ChangeEvent, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { getDesignTokens } from "../../../themes/themes";
import axios from "axios";

const RegisterPage = () => {
  const navigate = useNavigate(); 
  const theme = useTheme();
  const { palette } = getDesignTokens(theme.palette.mode);

  const [signUpError, setSignUpError] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const [emailError, setEmailError] = useState("");
  const [passwordError, setPasswordError] = useState("");
  const [confirmPasswordError, setConfirmPasswordError] = useState("");

  const validateEmail = (email: string) => {
    if (email === "") return false;
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return emailRegex.test(email);
  };

  const validatePassword = (password: string) => {
    if (password === "") return false;
    const passwordRegex =
      /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
    return passwordRegex.test(password);
  };

  const validateConfirmPassword = (confirmPassword: string) => {
    return password === confirmPassword;
  };

  const handleFirstNameChange = (event: ChangeEvent<HTMLInputElement>) => {
    const firstNameInput = event.target.value;
    setFirstName(firstNameInput);
  };

  const handleLastNameChange = (event: ChangeEvent<HTMLInputElement>) => {
    const lastNameInput = event.target.value;
    setLastName(lastNameInput);
  };

  const handleEmailChange = (event: ChangeEvent<HTMLInputElement>) => {
    const emailInput = event.target.value;
    setEmail(emailInput);

    if (!validateEmail(emailInput)) {
      setEmailError("Invalid Email");
    } else {
      setEmailError("");
    }
  };

  const handlePasswordChange = (event: ChangeEvent<HTMLInputElement>) => {
    const passwordInput = event.target.value;
    setPassword(passwordInput);

    if (!validatePassword(passwordInput)) {
      setPasswordError("Invalid Password");
    } else {
      setPasswordError("");
    }
  };

  const handleConfirmPassword = (event: ChangeEvent<HTMLInputElement>) => {
    const confirmPasswordInput = event.target.value;
    setConfirmPassword(confirmPasswordInput);

    if (!validateConfirmPassword(confirmPasswordInput)) {
      setConfirmPasswordError("Passwords do not match");
    } else {
      setConfirmPasswordError("");
    }
  };

  const handleSignUpSubmission = () => {
    if (
      !(
        validateEmail(email) &&
        validatePassword(password) &&
        validateConfirmPassword(confirmPassword) &&
        firstName &&
        lastName
      )
    ) {
      return;
    }

    const data = {
      first_name: firstName,
      last_name: lastName,
      email: email,
      password: password,
    };

    axios
      .post("http://127.0.0.1:8080/auth/register", data, {
        headers: { "Content-Type": "application/json" },
      })
      .then((response) => {
        navigate("/auth/email-verification")
        console.log(response);
      })
      .catch((error) => {
        setSignUpError(error.response.data.message);
      });
  };

  return (
    <>
      <Grid container justifyContent="center" alignItems="center" height="90vh">
        <Box
          boxShadow={2}
          p={3}
          width={"450px"} // Responsive width
          bgcolor="white"
          borderRadius={4}
          sx={{
            minHeight: "40vh",
            minWidth: "17vw",
            padding: "40px",
            display: "flex",
            flexDirection: "column",
            textAlign: "center"
          }} // Taller box
        >
          <Typography variant="h4" gutterBottom fontWeight={"bold"}>
            Sign Up
          </Typography>
          <TextField
            label="First Name"
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
            onChange={handleFirstNameChange}
            error={!firstName}
          />
          <TextField
            label="Last Name"
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
            onChange={handleLastNameChange}
            error={!lastName}
          />
          <TextField
            label="Email"
            fullWidth
            margin="normal"
            variant="standard"
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <AlternateEmailOutlined />
                </InputAdornment>
              ),
            }}
            onChange={handleEmailChange}
            error={!!emailError}
            helperText={emailError}
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
            error={!!passwordError}
            helperText={passwordError}
          />
          <TextField
            label="Confirm Password"
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
            onChange={handleConfirmPassword}
            error={!!confirmPasswordError}
            helperText={confirmPasswordError}
          />
          <Box>
            {signUpError && (
              <Typography variant="body2" sx={{ color: "red" }}>
                {signUpError}
              </Typography>
            )}
          </Box>
          <Box>
            <Typography variant="body2" fontWeight={"bold"}>
              Password requirements:
            </Typography>
            <Typography variant="body2">At least 8 characters</Typography>
            <Typography variant="body2">1 uppercase letter</Typography>
            <Typography variant="body2">1 lowercase letter</Typography>
            <Typography variant="body2">1 digit</Typography>
            <Typography variant="body2">1 special character</Typography>
          </Box>
          <Button
            variant="contained"
            fullWidth
            color="primary"
            sx={{ mt: 2, borderRadius: "10px" }}
            onClick={handleSignUpSubmission}
          >
            Sign Up
          </Button>
          <Box sx={{ mt: "auto", alignSelf: "flex-end-center" }}>
            <Typography variant="body2" sx={{ mt: 2 }}>
              Already have an account?{" "}
              <Link to={"/auth/login"} style={{ color: palette.niceBlue }}>
                Login
              </Link>
            </Typography>
          </Box>
        </Box>
      </Grid>
    </>
  );
};

export default RegisterPage;
