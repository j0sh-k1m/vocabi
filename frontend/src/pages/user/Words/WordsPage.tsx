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
import { useNavigate } from "react-router";

const WordListPage = () => {
  const user_id = useSelector((state: AuthState) => state.user_id);
  const token = useSelector((state: AuthState) => state.token);

  const apiURL = import.meta.env.VITE_API_URL; 

  const navigate = useNavigate();

  const [words, setWords] = useState<Array<WordItem>>([]);
  const [loading, setLoading] = useState(true);

  const handleDeleteWord = (word_ids: number[]) => {
    const updatedWords = words.filter(
      (word) => !word_ids.includes(word.word_id)
    );
    setWords(updatedWords);
  };

  useEffect(() => {
    axios({
      method: "get",
      url: `${apiURL}/word-list/${user_id}`,
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((response) => {
        setWords(response.data.user_words);
      })
      .catch((error) => {
        console.log(error);
      })
      .finally(() => {
        setLoading(false);
      });
  }, [apiURL, token, user_id]);

  const handleCreateNewWord = () => {
    navigate(`/word-list/${user_id}/create-word`);
  };

  return (
    <>
      <Navbar />
      {loading ? (
        <LoadingPage />
      ) : (
        <Container>
          <Grid container spacing={2}>
            <Grid item xs={12} sx={{ display: "flex" }}></Grid>
            {words.length > 0 ? (
              <WordList userWords={words} handleDeleteWord={handleDeleteWord} />
            ) : (
              <>
                <Typography>No words available.</Typography>
                <Container sx={{ display: "flex" }}>
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
                </Container>
              </>
            )}
          </Grid>
        </Container>
      )}
    </>
  );
};

export default WordListPage;
