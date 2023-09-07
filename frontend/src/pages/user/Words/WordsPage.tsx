import { Container, Grid, Typography } from "@mui/material";
import Navbar from "../../../components/Navbar/Navbar";
import WordList, {
  WordItem,
} from "../../../components/Words/WordList/WordList";
import { useEffect, useState } from "react";
import axios from "axios";
import { useSelector } from "react-redux";
import { AuthState } from "../../../store/store";
import LoadingPage from "../../Loading/LoadingPage";

const WordListPage = () => {
  const user_id = useSelector((state: AuthState) => state.user_id);
  const token = useSelector((state: AuthState) => state.token);

  const [words, setWords] = useState<Array<WordItem>>([]);
  const [loading, setLoading] = useState(true);

  const handleDeleteWord = (word_ids: number[]) => {
    console.log(word_ids)
    const updatedWords = words.filter((word) => !word_ids.includes(word.word_id))
    setWords(updatedWords)
  };

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
              <Typography>No words available.</Typography>
            )}
          </Grid>
        </Container>
      )}
    </>
  );
};

export default WordListPage;
