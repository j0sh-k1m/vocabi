import { Box, CircularProgress, Grid, Paper, Typography } from "@mui/material";
import Navbar from "../../../components/Navbar/Navbar";
import ModuleSelect from "../../../components/Select/ModuleSelect";
import { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import { AuthState } from "../../../store/store";
import axios from "axios";

export type UserStats = {
  accuracy: number;
  bestWord: ModuleStatWord;
  challenge_wins: number;
  correct: number;
  incorrect: number;
  stat_id: number;
  total_words_added: number;
  total_words_practiced: number;
  worstWord: ModuleStatWord;
};

export type ModuleStatWord = {
  accuracy: number;
  word: string;
};

export type ModuleData = {
  module: string;
  accuracy: number;
  bestWord: ModuleStatWord;
  correctAttempts: number;
  incorrectAttempts: number;
  wordsAdded: number;
  worstWord: ModuleStatWord;
};

const StatsPage = () => {
  const user_id = useSelector((state: AuthState) => state.user_id);
  const token = useSelector((state: AuthState) => state.token);
  const apiURL = import.meta.env.VITE_API_URL

  const [moduleData, setModuleData] = useState<ModuleData[]>([]);
  const [userStats, setUserStats] = useState<UserStats>({
    accuracy: 0,
    bestWord: { accuracy: 0, word: "" },
    challenge_wins: 0,
    correct: 0,
    incorrect: 0,
    stat_id: 0,
    total_words_added: 0,
    total_words_practiced: 0,
    worstWord: { accuracy: 0, word: "" },
  });

  const [selectedModule, setSelectedModule] = useState<string>();
  const [module, setModule] = useState<ModuleData>({
    accuracy: 0,
    bestWord: { accuracy: 0, word: "" },
    correctAttempts: 0,
    incorrectAttempts: 0,
    worstWord: { accuracy: 0, word: "" },
    wordsAdded: 0,
    module: "",
  });

  useEffect(() => {
    moduleData.forEach((module) => {
      if (module.module === selectedModule) {
        setModule(module);
      }
    });
  }, [moduleData, selectedModule]);

  const getSelectedModule = (module: string) => {
    setSelectedModule(module);
  };

  useEffect(() => {
    axios({
      method: "get",
      url: `${apiURL}/stat/${user_id}`,
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((response) => {
        if (response.data.user_stats) {
          setUserStats(response.data.user_stats);
        }
      })
      .catch((error) => {
        console.log(error);
      });

    axios({
      method: "get",
      url: `http://127.0.0.1:8080/stat/${user_id}/modules`,
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((response) => {
        if (response.data.content) {
          setModuleData(response.data.content);
        }
      })
      .catch((error) => {
        console.log(error);
      });
  }, [apiURL, token, user_id]);

  return (
    <>
      <Navbar />
      {/* User Personal/Overall stats */}
      <Typography variant="h4" sx={{ mb: 2, textAlign: "center" }}>
        Your Stats
      </Typography>
      <Grid container spacing={3} sx={{ margin: "0 auto", maxWidth: "900px" }}>
        {/* Accuracy Stat */}
        <Grid item xs={12} sm={6} md={4} sx={{ textAlign: "center" }}>
          <Paper elevation={3} sx={{ p: 3 }}>
            <Typography variant="h6">Accuracy</Typography>
            <Box
              mt={2}
              display="flex"
              justifyContent="center"
              alignItems="center"
            >
              <CircularProgress
                variant="determinate"
                value={userStats.accuracy}
                color={userStats.accuracy >= 70 ? "success" : userStats.accuracy >= 50 ? "warning" : "error"}
                sx={{ width: "100px", height: "100px", mr: 2 }}
              />
              <Typography variant="h4">{userStats.accuracy.toFixed(0)}%</Typography>
            </Box>
          </Paper>
        </Grid>

        {/* Total Words Added Stat */}
        <Grid item xs={12} sm={6} md={4} sx={{ textAlign: "center" }}>
          <Paper elevation={3} sx={{ p: 3 }}>
            <Typography variant="h6">Total Words Added</Typography>
            <Typography variant="h4">{userStats.total_words_added}</Typography>
          </Paper>
        </Grid>

        {/* Total Correct Attempts Stat */}
        <Grid item xs={12} sm={6} md={4} sx={{ textAlign: "center" }}>
          <Paper elevation={3} sx={{ p: 3 }}>
            <Typography variant="h6">Total Correct Attempts</Typography>
            <Typography variant="h4">{userStats.correct}</Typography>
          </Paper>
        </Grid>

        {/* Total Incorrect Attempts Stat */}
        <Grid item xs={12} sm={6} md={4} sx={{ textAlign: "center" }}>
          <Paper elevation={3} sx={{ p: 3 }}>
            <Typography variant="h6">Total Incorrect Attempts</Typography>
            <Typography variant="h4">{userStats.incorrect}</Typography>
          </Paper>
        </Grid>

        {/* Best Word Stat */}
        <Grid item xs={12} sm={6} md={4} sx={{ textAlign: "center" }}>
          <Paper elevation={3} sx={{ p: 3 }}>
            <Typography variant="h6">Best Word</Typography>
            <Typography variant="h4">{userStats.bestWord.word}</Typography>
            <Typography variant="body1">
              Accuracy: {userStats.bestWord.accuracy.toFixed(0)}%
            </Typography>
          </Paper>
        </Grid>

        {/* Worst Word Stat */}
        <Grid item xs={12} sm={6} md={4} sx={{ textAlign: "center" }}>
          <Paper elevation={3} sx={{ p: 3 }}>
            <Typography variant="h6">Worst Word</Typography>
            <Typography variant="h4">{userStats.worstWord.word}</Typography>
            <Typography variant="body1">
              Accuracy: {userStats.worstWord.accuracy.toFixed(0)}%
            </Typography>
          </Paper>
        </Grid>
      </Grid>

      {/* Specific Module Stats */}
      <Grid
        container
        justifyContent="center"
        alignItems="center"
        sx={{ mt: 10, display: "flex", flexDirection: "column" }}
      >
        {/* Header for Module Stats */}
        <Typography variant="h4" sx={{ mb: 2, textAlign: "center" }}>
          Module Stats
        </Typography>
        {moduleData.length > 0 && (
          <ModuleSelect
            moduleStats={moduleData}
            getSelectedModule={getSelectedModule}
          />
        )}
      </Grid>
      <Grid container spacing={3} sx={{ margin: "0 auto", maxWidth: "900px", mb: 4 }}>
        {/* Accuracy Stat */}
        <Grid item xs={12} sm={6} md={4} sx={{ textAlign: "center" }}>
          <Paper elevation={3} sx={{ p: 3 }}>
            <Typography variant="h6">Accuracy</Typography>
            <Box
              mt={2}
              display="flex"
              justifyContent="center"
              alignItems="center"
            >
              <CircularProgress
                variant="determinate"
                value={module?.accuracy}
                color={module?.accuracy >= 70.0 ? "success" : module?.accuracy >= 50 ? 'warning' : "error"}
                sx={{ width: "100px", height: "100px", mr: 2 }}
              />
              <Typography variant="h4">{module?.accuracy.toFixed(0)}%</Typography>
            </Box>
          </Paper>
        </Grid>

        {/* Total Words Added Stat */}
        <Grid item xs={12} sm={6} md={4} sx={{ textAlign: "center" }}>
          <Paper elevation={3} sx={{ p: 3 }}>
            <Typography variant="h6">Total Words Added</Typography>
            <Typography variant="h4">
              {module.wordsAdded}
            </Typography>
          </Paper>
        </Grid>

        {/* Total Correct Attempts Stat */}
        <Grid item xs={12} sm={6} md={4} sx={{ textAlign: "center" }}>
          <Paper elevation={3} sx={{ p: 3 }}>
            <Typography variant="h6">Total Correct Attempts</Typography>
            <Typography variant="h4">{module.correctAttempts}</Typography>
          </Paper>
        </Grid>

        {/* Total Incorrect Attempts Stat */}
        <Grid item xs={12} sm={6} md={4} sx={{ textAlign: "center" }}>
          <Paper elevation={3} sx={{ p: 3 }}>
            <Typography variant="h6">Total Incorrect Attempts</Typography>
            <Typography variant="h4">{module.incorrectAttempts}</Typography>
          </Paper>
        </Grid>

        {/* Best Word Stat */}
        <Grid item xs={12} sm={6} md={4} sx={{ textAlign: "center" }}>
          <Paper elevation={3} sx={{ p: 3 }}>
            <Typography variant="h6">Best Word</Typography>
            <Typography variant="h4">{module.bestWord.word}</Typography>
            <Typography variant="body1">
              Accuracy {module.bestWord.accuracy.toFixed(0)}%
            </Typography>
          </Paper>
        </Grid>

        {/* Worst Word Stat */}
        <Grid item xs={12} sm={6} md={4} sx={{ textAlign: "center" }}>
          <Paper elevation={3} sx={{ p: 3 }}>
            <Typography variant="h6">Worst Word</Typography>
            <Typography variant="h4">{module.worstWord.word}</Typography>
            <Typography variant="body1">
              Accuracy {module.worstWord.accuracy.toFixed(0)}%
            </Typography>
          </Paper>
        </Grid>
      </Grid>
    </>
  );
};

export default StatsPage;
