import { Box, Button, Grid, TextField, Typography } from "@mui/material";
import axios from "axios";
import { ChangeEvent, useState } from "react";
import { useSelector } from "react-redux";
import { AuthState } from "../../../store/store";
import { useNavigate } from "react-router-dom";

const CreateWordPage = () => {
  const user_id = useSelector((state: AuthState) => state.user_id);
  const token = useSelector((state: AuthState) => state.token);
  const navigate = useNavigate();

  const [wordData, setWordData] = useState({
    word: "",
    category: "",
    word_type: "",
    translation: "",
    translated_language: "",
    definition: "",
  });

  const {
    word,
    category,
    word_type,
    translation,
    translated_language,
    definition,
  } = wordData;

  const handleInputChange = (event: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target;
    setWordData({ ...wordData, [name]: value });
  };

  const handleCreateWord = () => {
    if (
      !word ||
      !category ||
      !word_type ||
      !translation ||
      !translated_language ||
      !definition
    ) {
      return;
    }

    axios({
      method: "post",
      url: `http://127.0.0.1:8080/word-list/${user_id}`,
      data: wordData,
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    })
      .then((response) => {

      })
      .catch((error) => {
        console.log(error);
      });

    setTimeout(() => {
      navigate(`/word-list/${user_id}`);
    }, 200);
  };

  const handleCancel = () => {
    navigate(`/word-list/${user_id}`);
  };

  return (
    <Grid container justifyContent="center" alignItems="center" height="90vh">
      <Box
        sx={{
          display: "flex",
          flexDirection: "column",
          textAlign: "center",
          boxShadow: 3,
          padding: "20px",
          borderRadius: "10px",
          width: "50%",
        }}
      >
        <Typography variant="h4" gutterBottom>
          Create New Word
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Word"
              name="word"
              value={wordData.word}
              onChange={handleInputChange}
              required
              error={!word}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Category"
              name="category"
              value={wordData.category}
              onChange={handleInputChange}
              required
              error={!category}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Word Type"
              name="word_type"
              value={wordData.word_type}
              onChange={handleInputChange}
              required
              error={!word_type}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Translation"
              name="translation"
              value={wordData.translation}
              onChange={handleInputChange}
              required
              error={!translation}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Translated Language"
              name="translated_language"
              value={wordData.translated_language}
              onChange={handleInputChange}
              required
              error={!translated_language}
            />
          </Grid>
          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Definition"
              name="definition"
              multiline
              rows={4}
              value={wordData.definition}
              onChange={handleInputChange}
              required
              error={!definition}
            />
          </Grid>
          <Grid item xs={12}>
            <Box display="flex" justifyContent="space-between">
              <Button onClick={handleCreateWord}>Create Word</Button>
              <Button onClick={handleCancel}>Cancel</Button>
            </Box>
          </Grid>
        </Grid>
      </Box>
    </Grid>
  );
};

export default CreateWordPage;
