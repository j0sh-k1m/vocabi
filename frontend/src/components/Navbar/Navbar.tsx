import { AppBar, Toolbar, Typography, IconButton } from "@mui/material";
import {
  Brightness4,
  Brightness7,
  DisplaySettings,
  InsertChart,
  School,
} from "@mui/icons-material";
import { Link } from "react-router-dom";
import { useContext } from "react";
import { ColorModeContext } from "../../App";
import { getDesignTokens } from "../../themes/themes";
import { useSelector } from "react-redux";
import { authState } from "../../store/store";
import { useTheme } from "@mui/material";

const Navbar = () => {
  const colorMode = useContext(ColorModeContext);
  const theme = useTheme();
  const { palette } = getDesignTokens(theme.palette.mode);

  const user_id = useSelector((state: authState) => state.user_id);

  return (
    <AppBar position="static" color="primary" sx={{ mb: 4 }}>
      <Toolbar sx={{ marginLeft: "25rem", marginRight: "25rem" }}>
        <Typography variant="h5" color={"white"}>
          Vocabi
        </Typography>
        <Link
          to={`/user-modules/${user_id}`}
          style={{
            marginLeft: "100px",
            color: "white",
            display: "flex",
            alignItems: "center",
            textDecoration: "none",
          }}
        >
          <School sx={{ mr: 1 }} />
          <Typography>Learn</Typography>
        </Link>

        <Link
          to={`/stat/${user_id}`}
          style={{
            marginLeft: "20px",
            color: "white",
            display: "flex",
            alignItems: "center",
            textDecoration: "none",
          }}
        >
          <DisplaySettings sx={{ mr: 1 }} />
          <Typography>Statistics</Typography>
        </Link>

        <Link
          to={`/word-list/${user_id}`}
          style={{
            marginLeft: "20px",
            color: "white",
            display: "flex",
            alignItems: "center",
            textDecoration: "none",
          }}
        >
          <InsertChart sx={{ mr: 1 }} />
          <Typography>Word List</Typography>
        </Link>

        <div style={{ flex: 1 }}></div>

        <IconButton onClick={colorMode.toggleColorMode} color="inherit">
          {theme.palette.mode === "dark" ? <Brightness7 /> : <Brightness4 />}
        </IconButton>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;
