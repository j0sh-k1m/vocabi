import { LockPersonOutlined } from "@mui/icons-material";
import {
  Box,
  Button,
  CircularProgress,
  Container,
  Grid,
  InputAdornment,
  TextField,
  Typography,
  useTheme,
} from "@mui/material";
import axios from "axios";
import { FormEvent, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { getDesignTokens } from "../../../themes/themes";
import { useDispatch } from "react-redux";
import { authActions } from "../../../store/store";

const ResetPasswordPage = () => {
  const theme = useTheme();
  const { palette } = getDesignTokens(theme.palette.mode);

  const dispatch = useDispatch();

  const navigate = useNavigate();

  const [email, setEmail] = useState<string>("");

  const [isLoading, setIsLoading] = useState<boolean>(false);

  const handleSendResetVerification = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!email) {
      return;
    }

    setIsLoading(true);

    axios({
      method: "post",
      url: `http://127.0.0.1:8080/auth/password/reset`,
      data: { email: email },
      headers: { "Content-Type": "application/json" },
    })
      .then((response) => {
        console.log(response);
        dispatch(
          authActions.setResetPasswordEmail({
            resetPasswordEmail: response.data.email,
          })
        );
        navigate(`/auth/password/create-new`);
      })
      .catch((error) => {
        console.log(error);
      })
      .finally(() => {
        setIsLoading(false);
      });
  };

  return (
    <>
      {/* Create a get email component */}

      <Grid container justifyContent="center" alignItems="center" height="90vh">
        <form onSubmit={handleSendResetVerification}>
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
              Reset Password
            </Typography>

            <TextField
              label="Email"
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
              onChange={(e) => setEmail(e.target.value)}
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
                <CircularProgress sx={{}} />
              </Container>
            ) : (
              <Button
                variant="contained"
                fullWidth
                color="primary"
                type="submit"
                sx={{ mt: 2, borderRadius: "10px" }}
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
    </>
  );
};

export default ResetPasswordPage;
