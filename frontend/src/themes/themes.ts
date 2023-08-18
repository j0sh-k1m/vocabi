import { PaletteMode } from "@mui/material";
import { blue, grey } from "@mui/material/colors";

export const getDesignTokens = (mode: PaletteMode) => ({
  palette: {
    mode,
    ...(mode === "light"
      ? {
          primary: blue,
          divider: blue[200],
          text: {
            primary: grey[900],
            secondary: grey[700],
          },
          niceBlue: "#007cfc",
        }
      : {
          divider: "#fff",
          text: {
            primary: "#fff",
            secondary: grey[500],
          },
          niceBlue: "#1487fa",
        }),
  },
});
