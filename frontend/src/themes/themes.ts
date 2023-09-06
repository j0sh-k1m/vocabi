import { PaletteMode } from "@mui/material";
import { blue, grey } from "@mui/material/colors";

export const getDesignTokens = (mode: PaletteMode) => ({
  palette: {
    mode,
    background: {
      default: mode === "light" ? "#F5F5F5" : "#333333", // Set the background color here
    },
    ...(mode === "light"
      ? {
          primary: blue,
          divider: blue[200],
          text: {
            primary: grey[900],
            secondary: grey[700],
          },
          niceBlue: "#007cfc",
          secondaryBlue: "#AED8FF",
          thirdBlue: "#1487fa",
          offBlack: "#303030", // Text color for light mode
        }
      : {
          divider: "#fff",
          text: {
            primary: "#fff",
            secondary: grey[500],
          },
          niceBlue: "#007cfc",
          secondaryBlue: "#AED8FF",
          thirdBlue: "#1487fa",
          offBlack: "#303030", // Text color for dark mode
        }),
  },
});

