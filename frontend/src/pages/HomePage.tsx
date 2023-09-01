import { Typography, Button, useTheme, Box } from "@mui/material";
import { Link } from "react-router-dom";
import { getDesignTokens } from "../themes/themes";

const HomePage = () => {
  const theme = useTheme();
  const { palette } = getDesignTokens(theme.palette.mode);
  return (
    <>
      <Box sx={{ boxShadow: 3, borderRadius: "10px" }}>
        <Typography
          variant="h1"
          style={{
            padding: "15px",
            backgroundColor: palette.niceBlue,
            color: "white",
            borderRadius: "10px",
          }}
        >
          Vocabi
        </Typography>
      </Box>
      <Link to={"/auth/login"}>
        <Button size="large" style={{ margin: "10px" }}>
          Get Started
        </Button>
      </Link>
      {/* <Link to={"/signup"}>
        <Button size="large" style={{ margin: "10px" }}>
          Sign Up
        </Button>
      </Link> */}
    </>
  );
};

export default HomePage;
