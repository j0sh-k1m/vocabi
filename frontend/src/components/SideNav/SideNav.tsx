import { useTheme } from "@mui/material";
import {
  Brightness4,
  Brightness7,
  DisplaySettings,
  InsertChart,
  School,
} from "@mui/icons-material";
import { Drawer, ListItem, Typography, Box, IconButton } from "@mui/material";
import { useContext } from "react";
import { ColorModeContext } from "../../App";
import { getDesignTokens } from "../../themes/themes";
import { Link } from "react-router-dom";

const SideNav = () => {
  const theme = useTheme();
  const colorMode = useContext(ColorModeContext);
  const { palette } = getDesignTokens(theme.palette.mode);

  const user_id = 1; 

  return (
    <>
      <Drawer
        anchor="left"
        variant="permanent"
        sx={{
          display: "flex",
          justifyContent: "center",
        }}
      >
        <Box display="flex" margin="10px" justifyContent="center">
          <Typography variant="h5" color={palette.niceBlue}>
            Vocabi
          </Typography>
        </Box>
        <Box
          display="flex"
          flexDirection="column"
          justifyContent="center"
          height="80%"
        >
          <Link to={`/user-modules/${user_id}`} style={{marginBottom: "50px", color: palette.text.primary}}>
            <ListItem style={{ justifyContent: "center" }}>    
              <School style={{ marginRight: "5px" }} />
              <Typography>Learn</Typography>
            </ListItem>
          </Link>

          <Link to={`/stat/${user_id}`} style={{marginBottom: "50px", color: palette.text.primary}}>
            <ListItem style={{ justifyContent: "center" }}>      
              <DisplaySettings style={{ marginRight: "5px" }} />
              <Typography>Statistics</Typography>
            </ListItem>
          </Link>


          <Link to={`/word-list/${user_id}`} style={{marginBottom: "50px", color: palette.text.primary}}>
            <ListItem style={{ justifyContent: "center" }}>
              <InsertChart style={{ marginRight: "5px" }} />
              <Typography>Word List</Typography>
            </ListItem>
          </Link>

        </Box>
        <Box sx={{ justifyContent: "center" }}>
          <IconButton
            sx={{ ml: 1, justifyContent: "center" }}
            style={{ borderRadius: 0, width: "5px", height: "5px" }}
            onClick={colorMode.toggleColorMode}
            color="inherit"
          >
            {theme.palette.mode === "dark" ? <Brightness7 /> : <Brightness4 />}
          </IconButton>
        </Box>
      </Drawer>
    </>
  );
};

export default SideNav;
