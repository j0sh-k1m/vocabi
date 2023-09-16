import { LockPersonOutlined } from "@mui/icons-material";
import {
  Grid,
  Box,
  Typography,
  TextField,
  InputAdornment,
  Container,
  CircularProgress,
  Button,
  useTheme,
} from "@mui/material";
import axios from "axios";
import { ChangeEvent, useState } from "react";
import { useSelector } from "react-redux";
import { Link, useNavigate } from "react-router-dom";
import { AuthState } from "../../../store/store";
import { getDesignTokens } from "../../../themes/themes";

const CreateNewPasswordPage = () => {
  const theme = useTheme();
  const { palette } = getDesignTokens(theme.palette.mode);

  const navigate = useNavigate(); 

  const email = useSelector((state: AuthState) => state.resetPasswordEmail);

  const [newPassword, setNewPassword] = useState<string>("");
  const [confirmNewPassword, setConfirmNewPassword] = useState<string>("");
  const [verificationToken, setVerificationToken] = useState<string>("");

  const [newPasswordError, setNewPasswordError] = useState<string>("");
  const [confirmNewPasswordError, setConfirmNewPasswordError] =
    useState<string>("");

  const [isLoading, setIsLoading] = useState<boolean>(false);

  const [resetSuccess, setResetSuccess] = useState<boolean>(false);

  const validatePassword = (password: string) => {
    if (password === "") return false;
    const passwordRegex =
      /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
    return passwordRegex.test(password);
  };

  const handleNewPasswordChange = (event: ChangeEvent<HTMLInputElement>) => {
    const passwordInput = event.target.value;
    setNewPassword(passwordInput);

    if (!validatePassword(passwordInput)) {
      setNewPasswordError("Invalid Password");
    } else {
      setNewPasswordError("");
    }
  };

  const handleConfirmNewPasswordChange = (
    event: ChangeEvent<HTMLInputElement>
  ) => {
    const passwordInput = event.target.value;
    setConfirmNewPassword(passwordInput);

    if (passwordInput !== newPassword) {
      setConfirmNewPasswordError("Passwords do not match");
    } else {
      setConfirmNewPasswordError("");
    }
  };

  const handleResetPasswordSubmission = () => {
    if (!newPassword || !confirmNewPassword || !verificationToken) {
      return;
    }

    setIsLoading(true);

    axios({
      method: "post",
      url: "http://127.0.0.1:8080/auth/password/create-new",
      data: {
        email: email,
        password: newPassword,
        confirm_password: confirmNewPassword,
        verification_token: verificationToken,
      },
      headers: { "Content-Type": "application/json" },
    })
      .then((response) => {
        console.log(response);
        setResetSuccess(true);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  return (
    <>
      {!resetSuccess && (
        <Grid
          container
          justifyContent="center"
          alignItems="center"
          height="90vh"
        >
          <form onSubmit={handleResetPasswordSubmission}>
            <Box
              boxShadow={2}
              p={3}
              width={{ width: "400px" }} // Responsive width
              bgcolor="white"
              borderRadius={4}
              sx={{
                minHeight: "40vh",
                padding: "40px",
                display: "flex",
                flexDirection: "column",
              }}
            >
              <Typography
                variant="h4"
                gutterBottom
                fontWeight={"bold"}
                sx={{ textAlign: "center" }}
              >
                Reset Password
              </Typography>
              <TextField
                label="New Password"
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
                onChange={handleNewPasswordChange}
                error={!!newPasswordError}
                helperText={newPasswordError}
              />
              <TextField
                label="Confirm New Password"
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
                onChange={handleConfirmNewPasswordChange}
                error={!!confirmNewPasswordError}
                helperText={confirmNewPasswordError}
              />
              <TextField
                label="Verification Code"
                fullWidth
                margin="normal"
                variant="standard"
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <LockPersonOutlined />
                    </InputAdornment>
                  ),
                }}
                onChange={(e) => setVerificationToken(e.target.value)}
              />
              {isLoading ? (
                <Container
                  sx={{
                    display: "flex",
                    justifyContent: "center",
                    alignItems: "center",
                    mt: 4,
                  }}
                >
                  <CircularProgress />
                </Container>
              ) : (
                <Button
                  variant="contained"
                  fullWidth
                  color="primary"
                  sx={{ mt: 2, borderRadius: "10px" }}
                  type="submit"
                  onClick={handleResetPasswordSubmission}
                >
                  Reset Password
                </Button>
              )}

              <Box sx={{ mt: "auto", alignSelf: "flex-end-center" }}>
                <Typography variant="body2" sx={{ mt: 1 }}>
                  Remember your password?{" "}
                  <Link to={"/auth/login"} style={{ color: palette.niceBlue }}>
                    Login
                  </Link>
                </Typography>
              </Box>
            </Box>
          </form>
        </Grid>
      )}

      <Grid container justifyContent="center" alignItems="center" height="90vh">
        {resetSuccess && (
          <Box
            boxShadow={2}
            p={3}
            width={{ width: "400px" }} // Responsive width
            bgcolor="white"
            borderRadius={4}
            sx={{
              minHeight: "30vh",
              padding: "40px",
              display: "flex",
              flexDirection: "column",
            }}
          >
            <Typography
              variant="h4"
              gutterBottom
              fontWeight={"bold"}
              sx={{ textAlign: "center" }}
            >
              Password Successfully Reset
            </Typography>
            <Button sx={{ mt: 4 }} onClick={() => navigate('/auth/login')}>Login</Button>
          </Box>
        )}
      </Grid>
    </>
  );
};

export default CreateNewPasswordPage;
