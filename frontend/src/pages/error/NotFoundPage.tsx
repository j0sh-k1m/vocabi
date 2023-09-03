import { Box, Button, Typography } from "@mui/material";
import { Link } from "react-router-dom";

const NotFoundPage = () => {
  const user_id = "1";
  return (
    <>
      <Box sx={{ padding: "20px", boxShadow: 3, borderRadius: "20px" }}>
        <Typography variant="h1" fontSize="150px">
          404
        </Typography>
        <Typography variant="h1" fontSize="75px">
          Page Not Found
        </Typography>
        <Box sx={{ mt: 2 }}>
          <Link to={`/user-modules/${user_id}`}>
            <Button size="large">Go Back Home</Button>
          </Link>
        </Box>
      </Box>
    </>
  );
};

export default NotFoundPage;
