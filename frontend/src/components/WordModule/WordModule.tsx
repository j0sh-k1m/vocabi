import { IconButton, useTheme } from "@mui/material";
import { PlayArrow } from "@mui/icons-material";
import { Box, Typography } from "@mui/material";
import { getDesignTokens } from "../../themes/themes";

type ComponentProps = {
  moduleName: string;
  wordOccurrences: number; // Change the type to number
};

const WordModule = (props: ComponentProps) => {
  const theme = useTheme();
  const { palette } = getDesignTokens(theme.palette.mode);

  // Function to format the number of words
  const formatWordCount = (count: number) => {
    if (count >= 1000) {
      return `${(count / 1000).toFixed(1)}K`; // Format as K for thousands
    }
    return count.toString();
  };

  return (
    <>
      <Box
        sx={{
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
          padding: "20px",
          backgroundColor:
            palette.mode === "dark" ? palette.thirdBlue : palette.secondaryBlue,
          borderRadius: "10px",
          boxShadow: "0px 4px 6px rgba(0, 0, 0, 0.1)",
          transition: "transform 0.2s",
          "&:hover": {
            transform: "scale(1.05)",
          },
        }}
      >
        <Typography
          variant="h6"
          sx={{ fontWeight: "bold", textAlign: "center" }}
        >
          {props.moduleName}
        </Typography>
        <Typography
          variant="body1"
          sx={{ textAlign: "center", margin: 1, color: palette.text.secondary }}
        >
          Words: {formatWordCount(props.wordOccurrences)} {/* Format word count */}
        </Typography>
        <IconButton sx={{ alignSelf: "center", borderRadius: "50%" }}>
          <PlayArrow />
        </IconButton>
      </Box>
    </>
  );
};

export default WordModule;
