import { Box, Container, Divider, Grid, Typography } from "@mui/material";
import Navbar from "../../../components/Navbar/Navbar";
import { useEffect, useState } from "react";
import axios from "axios";
import { useSelector } from "react-redux";
import { AuthState } from "../../../store/store";
import WordModule from "../../../components/WordModule/WordModule";

import LoadingPage from "../../Loading/LoadingPage";

type WordModule = {
  category: string;
  id: string;
  occurrences: number;
};

const ModulesPage = () => {
  const user_id = useSelector((state: AuthState) => state.user_id);
  const token = useSelector((state: AuthState) => state.token);

  const [modules, setModules] = useState<Array<WordModule>>();
  const [error, setError] = useState<string>("");

  useEffect(() => {
    axios({
      method: "get",
      url: `http://127.0.0.1:8080/user-modules/${user_id}`,
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((response) => {
        if (typeof response.data.message !== "string") {
          setModules(response.data.message);
          setError("");
        } else if (typeof response.data.message === "string") {
          setError(response.data.message);
        }
      })
      .catch((error) => {
        console.log(error);
      });
  }, [token, user_id]);

  return (
    <>
      <Navbar />
      {!error && !modules && <LoadingPage />}
      {error && !modules && (
        <Grid
          container
          justifyContent="center"
          alignItems="center"
          height="80vh"
        >
          <Box sx={{ textAlign: "center" }}>
            <Typography variant="h5">No Words Have Been Added!</Typography>
            <Typography variant="h5">Please add some words</Typography>
          </Box>
        </Grid>
      )}
      {modules && (
        <Container>
          <Grid container spacing={2}>
            {modules.map((element) => (
              <Grid item xs={12} sm={6} md={4} lg={3} key={element.id}>
                <WordModule
                  moduleName={element.category}
                  wordOccurrences={element.occurrences}
                />
                <Divider sx={{ marginY: 2 }} />
              </Grid>
            ))}
          </Grid>
        </Container>
      )}
    </>
  );
};

export default ModulesPage;
