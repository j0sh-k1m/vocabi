import { Box, Typography, CircularProgress } from "@mui/material";

const LoadingPage = () => {
  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        minHeight: "80vh",
      }}
    >
      <CircularProgress color="primary" size={80} thickness={4} sx={{ mb: 2 }} />
      <Typography variant="h5" color="primary">
        Loading...
      </Typography>
    </Box>
  );
};

export default LoadingPage;
