import { Button, InputAdornment, TextField, useTheme } from "@mui/material";
import { Box, Typography } from "@mui/material";
import { getDesignTokens } from "../../themes/themes";
import { CodeOutlined } from "@mui/icons-material";
import { ChangeEvent, useState } from "react";
import axios from "axios";
import { Link } from "react-router-dom";

const EmailVerificationPage = () => {
  const theme = useTheme();
  const { palette } = getDesignTokens(theme.palette.mode);

  const tempEmail = "test@example.com";

  const [code, setCode] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [message, setMessage] = useState("Please Verify Your Email");

  const handleCodeInput = (event: ChangeEvent<HTMLInputElement>) => {
    const codeInput = event.target.value;
    setCode(codeInput);
  };

  // Instead of putting code as url param, make it a post request and post the code to the backend
  const handleSubmitCode = () => {
    if (!code) {
      return;
    }
    const data = {
      token: code,
    };
    axios
      .post(`http://127.0.0.1:8080/auth/email-verification`, data, {
        headers: { "Content-Type": "application/json" },
      })
      .then((response) => {
        setMessage("Email Successfully Verified");
        setErrorMessage("");
      })
      .catch((error) => {
        setErrorMessage(error.response.data.message);
      });
  };

  return (
    <>
      <Box sx={{ boxShadow: 3, padding: "40px", borderRadius: "10px" }}>
        <Typography variant="h3" sx={{ color: palette.niceBlue }}>
          {message}
        </Typography>
        <Typography variant="h6" sx={{ mt: 3 }}>
          Verification code was to{" "}
          <Typography variant="body1" sx={{ mt: 2, color: palette.niceBlue }}>
            {tempEmail}
          </Typography>
        </Typography>
        <TextField
          label="Vericiation Code"
          placeholder="Enter code here"
          fullWidth
          margin="normal"
          variant="standard"
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <CodeOutlined />
              </InputAdornment>
            ),
          }}
          onChange={handleCodeInput}
        />
        {message === "Please Verify Your Email" && (
          <Button onClick={handleSubmitCode}>Verify</Button>
        )}
        {errorMessage && (
          <Typography variant="body2" sx={{ color: "red" }}>
            {errorMessage}
          </Typography>
        )}
        {message === "Email Successfully Verified" && (
          <Link to={"/auth/login"}>
            <Button
              sx={{ mt: 1 }}
              variant="contained"
              color="primary"
              size="large"
            >
              Login
            </Button>
          </Link>
        )}
      </Box>
    </>
  );
};

export default EmailVerificationPage;
