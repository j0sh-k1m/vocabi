import { useEffect, useState } from "react";
import { Typography, Paper, Grid, TextField, Box, Button } from "@mui/material";
import Navbar from "../../../components/Navbar/Navbar";
import { WordItem } from "../../../components/Words/WordList/WordList";
import axios from "axios";
import { useSelector } from "react-redux";
import { AuthState } from "../../../store/store";

const ExecuteModulePage = () => {
  const user_id = useSelector((state: AuthState) => state.user_id);
  const token = useSelector((state: AuthState) => state.token);

  const [lastAttempts, setLastAttempts] = useState<Array<boolean>>([]);
  const [accuracy, setAccuracy] = useState<number | string>("N/A");
  const [correctAttempts, setCorrectAttempts] = useState<number>(0);
  const [incorrectAttempts, setIncorrectAttempts] = useState<number>(0);

  const [moduleWords, setModuleWords] = useState<Array<WordItem>>([]);

  useEffect(() => {
    const searchParams = new URLSearchParams(window.location.search);
    const moduleName = searchParams.get("content");

    if (!moduleName) {
      return;
    }

    axios({
      method: "get",
      url: `http://127.0.0.1:8080/user-modules/${user_id}/module?content=${moduleName}`,
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((response) => {
        console.log(response);
      })
      .catch((error) => {
        console.log(error);
      });
  });

  const handleSubmit = () => {};

  return (
    <>
      <Navbar />
      <Grid
        container
        direction="column"
        justifyContent="center"
        alignItems="center"
        spacing={3}
        height="60vh"
      >
        <Grid item>
          <Paper
            elevation={3}
            sx={{
              width: "700px",
              height: "350px",
              alignItems: "center",
              justifyContent: "center",
              display: "flex",
              flexDirection: "column",
            }}
          >
            <Typography variant="h4" fontWeight="light">
              korean
            </Typography>
            <Typography
              variant="h3"
              sx={{ fontWeight: "bold", textAlign: "center", mt: 2 }}
            >
              포도
            </Typography>
          </Paper>
        </Grid>
        <Grid item sx={{ display: "flex", alignItems: "center" }}>
          <TextField
            sx={{ width: "300px", marginTop: "16px" }}
            label="Answer"
            variant="standard"
            size="medium"
          />
          <Button sx={{ height: "30px", mt: 3 }} onClick={handleSubmit}>
            Submit
          </Button>
        </Grid>
        <Grid item sx={{ textAlign: "center" }}>
          <Typography variant="h6">
            Accuracy: <span style={{ fontWeight: "bold" }}>{accuracy}%</span>
          </Typography>
          <Typography variant="h6">
            Correct Attempts:{" "}
            <span style={{ fontWeight: "bold" }}>{correctAttempts}</span>
          </Typography>
          <Typography variant="h6">
            Incorrect Attempts:{" "}
            <span style={{ fontWeight: "bold" }}>{incorrectAttempts}</span>
          </Typography>
        </Grid>
        <Grid item>
          <Box display="flex" justifyContent="center">
            {lastAttempts.map((isCorrect) => (
              <Box
                key={Math.random()}
                width="20px"
                height="20px"
                margin="2px"
                sx={{ backgroundColor: isCorrect ? "#90EE90" : "#F4444E" }}
              />
            ))}
          </Box>
        </Grid>
      </Grid>
    </>
  );
};

export default ExecuteModulePage;
