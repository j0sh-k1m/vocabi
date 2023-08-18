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

const SideNav = () => {
  const theme = useTheme();
  const colorMode = useContext(ColorModeContext);
  const { palette } = getDesignTokens(theme.palette.mode);
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
          <ListItem style={{ marginBottom: "50px", justifyContent: "center" }}>
            <School />
            <Typography>Learn</Typography>
          </ListItem>

          <ListItem style={{ marginBottom: "50px", justifyContent: "center" }}>
            <DisplaySettings />
            <Typography>Statistics</Typography>
          </ListItem>

          <ListItem style={{ justifyContent: "center" }}>
            <InsertChart />
            <Typography>Personal</Typography>
          </ListItem>
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
