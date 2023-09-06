import { Container, Divider, Grid } from "@mui/material";
import Navbar from "../../../components/Navbar/Navbar";
import { useEffect, useState } from "react";
import axios from "axios";
import { useSelector } from "react-redux";
import { authState } from "../../../store/store";
import WordModule from "../../../components/WordModule/WordModule";
import { useTheme } from "@mui/material";
import { getDesignTokens } from "../../../themes/themes";
import LoadingPage from "../../Loading/LoadingPage";

type WordModule = {
  category: string;
  id: string;
  occurrences: string;
};

const ModulesPage = () => {
  const theme = useTheme();
  const { palette } = getDesignTokens(theme.palette.mode);

  const user_id = useSelector((state: authState) => state.user_id);
  const token = useSelector((state: authState) => state.token);

  const [modules, setModules] = useState<Array<WordModule>>([]);

  useEffect(() => {
    axios({
      method: "get",
      url: `http://127.0.0.1:8080/user-modules/${user_id}`,
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((response) => {
        console.log(response.data?.message);
        setModules(response.data?.message);
      })
      .catch((error) => {
        console.log(error);
      });
  }, [token, user_id]);

  return (
    <>
      <Navbar />
      {modules.length === 0 && <LoadingPage />}
      {modules.length !== 0 && (
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
