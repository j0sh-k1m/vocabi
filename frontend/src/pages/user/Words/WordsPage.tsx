import { Button, Container, Grid, Typography } from "@mui/material";
import Navbar from "../../../components/Navbar/Navbar";
import WordList, {
  WordItem,
} from "../../../components/Words/WordList/WordList";
import { useEffect, useState } from "react";
import axios from "axios";
import { useSelector } from "react-redux";
import { AuthState } from "../../../store/store";
import LoadingPage from "../../Loading/LoadingPage";
import { useNavigate } from "react-router-dom";

const WordListPage = () => {
  const user_id = useSelector((state: AuthState) => state.user_id);
  const token = useSelector((state: AuthState) => state.token);

  const navigate = useNavigate(); 
  const [words, setWords] = useState<Array<WordItem>>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios({
      method: "get",
      url: `http://127.0.0.1:8080/word-list/${user_id}`,
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((response) => {
        console.log(response);
        setWords(response.data.user_words);
      })
      .catch((error) => {
        console.log(error);
      })
      .finally(() => {
        setLoading(false);
      });
  }, [token, user_id]);

  const handleCreateNewWord = () => {
    navigate(`/word-list/${user_id}/create-word`)
  }

  return (
    <>
      <Navbar />
      {loading ? (
        <LoadingPage />
      ) : (
        <Container>
          <Grid container spacing={2}>
            <Grid item xs={12} sx={{ display: "flex" }}>
              <Button
                sx={{
                  fontWeight: "bold",
                  borderRadius: "8px",
                  mb: 2,
                }}
                onClick={handleCreateNewWord}
              >
                Create New Word
              </Button>
              <Button
                sx={{
                  color: "#71C562",
                  fontWeight: "bold",
                  borderRadius: "8px",
                  mb: 2,
                  ml: "auto",
                  mr: 1,
                }}
              >
                Edit
              </Button>
              <Button
                sx={{
                  color: "red",
                  fontWeight: "bold",
                  borderRadius: "8px",
                  mb: 2,
                  mr: 1,
                }}
              >
                Delete
              </Button>
            </Grid>
            {words.length > 0 ? (
              <WordList userWords={words} />
            ) : (
              <Typography>No words available.</Typography>
            )}
          </Grid>
        </Container>
      )}
    </>
  );
};

export default WordListPage;
