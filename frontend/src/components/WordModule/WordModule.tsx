import { IconButton, useTheme, Box, Typography } from "@mui/material";
import { PlayArrow } from "@mui/icons-material";
import { getDesignTokens } from "../../themes/themes";
import { useNavigate } from "react-router";
import { useSelector } from "react-redux";
import { AuthState } from "../../store/store";

type ComponentProps = {
  moduleName: string;
  wordOccurrences: number;
};

const WordModule = (props: ComponentProps) => {
  const theme = useTheme();
  const { palette } = getDesignTokens(theme.palette.mode);

  const user_id = useSelector((state: AuthState) => state.user_id)

  const navigate = useNavigate(); 

  // Function to format the number of words
  const formatWordCount = (count: number) => {
    if (count >= 1000) {
      return `${(count / 1000).toFixed(1)}K`; // Format as K for thousands
    }
    return count.toString();
  };

  const handleExecuteModule = () => {
    navigate(`/user-modules/${user_id}/modules?content=${props.moduleName}`)
  }

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
          sx={{ textAlign: "center", margin: 1, color: theme.palette.mode === 'light' ? palette.text.secondary : "#D3D3D3" }}
        >
          Words: {formatWordCount(props.wordOccurrences)}
        </Typography>
        <IconButton sx={{ alignSelf: "center", borderRadius: "50%" }} onClick={handleExecuteModule}>
          <PlayArrow />
        </IconButton>
      </Box>
    </>
  );
};

export default WordModule;
