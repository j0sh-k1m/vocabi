import { FormEvent, useEffect, useState } from "react";
import { Typography, Paper, Grid, TextField, Box, Button } from "@mui/material";
import Navbar from "../../../components/Navbar/Navbar";
import { WordItem } from "../../../components/Words/WordList/WordList";
import axios from "axios";
import { useSelector } from "react-redux";
import { AuthState } from "../../../store/store";
import { useNavigate } from "react-router";

type WordData = {
  word_id: number;
  correct: number;
  incorrect: number;
};

const ExecuteModulePage = () => {
  // Auth variables
  const user_id = useSelector((state: AuthState) => state.user_id);
  const token = useSelector((state: AuthState) => state.token);

  const navigate = useNavigate();

  // Module data/stats shown to user
  const [lastAttempts, setLastAttempts] = useState<boolean[]>([]);
  const [accuracy, setAccuracy] = useState<number>();
  const [correctAttempts, setCorrectAttempts] = useState<number>(0);
  const [incorrectAttempts, setIncorrectAttempts] = useState<number>(0);

  // Module words
  const [moduleWords, setModuleWords] = useState<WordItem[]>([]);

  // Current updated word
  const [currentWord, setCurrentWord] = useState<WordItem>();

  // Users answer/guess
  const [answer, setAnswer] = useState<string>("");

  const [finishedModule, setFinshedModule] = useState<boolean>(false);

  const [wordsData, setWordsData] = useState<WordData[]>([]);

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

        if (response.data.content) {
          setModuleWords(response?.data.content);
          setCurrentWord(response?.data.content[0]);
        }
      })
      .catch((error) => {
        console.log(error);
      });
  }, [token, user_id]);

  useEffect(() => {
    setAccuracy(
      Math.round(
        (correctAttempts / (correctAttempts + incorrectAttempts)) * 100
      )
    );
  }, [incorrectAttempts, correctAttempts]);

  /**
   * Finish the module for a user
   */
  const handleFinishModule = () => {
    axios({
      method: "patch",
      url: `http://127.0.0.1:8080/user-modules/${user_id}/words`,
      data: { words: wordsData },
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    })
      .then(() => {
        axios({
          method: "post",
          url: `http://127.0.0.1:8080/user-modules/${user_id}/stats`,
          data: {
            total_words_practiced: correctAttempts + incorrectAttempts,
            correct: correctAttempts,
            incorrect: incorrectAttempts,
          },
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        })
          .then(() => {
            setFinshedModule(true);
          })
          .catch((error) => {
            console.log(error);
          });
      })
      .catch((error) => {
        console.log(error);
      });
  };

  /**
   * Updates the current displayed word. Updates to the next word in the moduleWords array (state)
   */
  const updateDisplayingWord = () => {
    moduleWords.forEach((word, index) => {
      if (word.word_id === currentWord?.word_id) {
        if (index === moduleWords.length - 1) {
          setCurrentWord(moduleWords[0]);
        } else {
          setCurrentWord(moduleWords[index + 1]);
        }
      }
    });
  };

  /**
   * Handle submitting a word. Updates attempts, and moves user to next word
   */
  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (!answer || !currentWord) {
      return;
    }

    const userGuess = answer.toLowerCase().trim();
    const correctAnswer = currentWord.word.toLowerCase().trim();

    // user inputs correct word translation
    if (userGuess === correctAnswer) {
      setCorrectAttempts((val) => val + 1);

      const updatedLastAttempts = [...lastAttempts, true];

      if (updatedLastAttempts.length > 10) {
        updatedLastAttempts.shift();
      }
      setLastAttempts(updatedLastAttempts);

      const data = [
        ...wordsData,
        { word_id: currentWord.word_id, correct: 1, incorrect: 0 },
      ];
      setWordsData(data);

      // uset inputs incorrect word translation
    } else if (userGuess !== correctAnswer) {
      setIncorrectAttempts((val) => val + 1);

      const updatedLastAttempts = [...lastAttempts, false];

      if (updatedLastAttempts.length > 10) {
        updatedLastAttempts.shift();
      }
      setLastAttempts(updatedLastAttempts);

      const data = [
        ...wordsData,
        { word_id: currentWord.word_id, correct: 0, incorrect: 1 },
      ];
      setWordsData(data);
    }
    updateDisplayingWord();
    setAnswer("");
  };

  return (
    <>
      <Navbar />
      {!finishedModule && (
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
                {currentWord?.translated_language}
              </Typography>
              <Typography
                variant="h3"
                sx={{ fontWeight: "bold", textAlign: "center", mt: 2 }}
              >
                {currentWord?.translation}
              </Typography>
            </Paper>
          </Grid>
          <Grid item sx={{ display: "flex", alignItems: "center" }}>
            <form onSubmit={handleSubmit}>
              <TextField
                sx={{ width: "300px", marginTop: "16px" }}
                label="Answer"
                variant="standard"
                size="medium"
                required
                value={answer}
                onChange={(e) => setAnswer(e.target.value)}
                error={!answer}
              />
              <Button sx={{ height: "30px", mt: 3 }} type="submit">
                Submit
              </Button>
            </form>
          </Grid>
          <Grid item sx={{ textAlign: "center" }}>
            <Typography variant="h5">
              Accuracy: <span style={{ fontWeight: "bold" }}>{accuracy}%</span>
            </Typography>
            <Typography variant="body1">
              Correct Attempts:{" "}
              <span style={{ fontWeight: "bold" }}>{correctAttempts}</span>
            </Typography>
            <Typography variant="body1">
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
                  sx={{ backgroundColor: isCorrect ? "#67f067" : "#F4444E" }}
                />
              ))}
            </Box>
          </Grid>
          <Grid item>
            <Button onClick={handleFinishModule} size="large">
              Finish
            </Button>
          </Grid>
        </Grid>
      )}
      {finishedModule && (
        <Grid
          container
          direction="column"
          justifyContent="center"
          alignItems="center"
          spacing={4}
          height="60vh"
        >
          <Paper
            elevation={5}
            sx={{ padding: "30px", textAlign: "center", wordSpacing: 2 }}
          >
            <Grid item>
              <Typography variant="h2">Module Completed!</Typography>
            </Grid>
            <Grid
              item
              sx={{
                transition: "transform 0.2s",
                "&:hover": {
                  transform: "scale(1.05)",
                },
              }}
            >
              <Typography variant="h4" sx={{ pt: 2 }}>
                Accuracy:{" "}
                <span
                  style={{
                    color:
                      accuracy && accuracy >= 80
                        ? "#67f067"
                        : accuracy && accuracy > 50
                        ? "#dbd514"
                        : "#F4444E",
                    fontWeight: "bold",
                  }}
                >
                  {accuracy}%
                </span>
              </Typography>
            </Grid>
            <Grid
              item
              sx={{
                transition: "transform 0.2s",
                "&:hover": {
                  transform: "scale(1.05)",
                },
              }}
            >
              <Typography variant="h5" sx={{ padding: "8px", pt: 2 }}>
                Words Completed:{" "}
                <span style={{ fontWeight: "bold" }}>
                  {correctAttempts + incorrectAttempts}
                </span>
              </Typography>
            </Grid>
            <Grid item>
              <Button
                onClick={() => navigate(`/user-modules/${user_id}`)}
                size="large"
              >
                Home
              </Button>
            </Grid>
          </Paper>
        </Grid>
      )}
    </>
  );
};

export default ExecuteModulePage;
