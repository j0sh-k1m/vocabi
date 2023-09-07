import { useState } from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  TablePagination,
  TableFooter,
  Checkbox,
  Button,
  Container,
} from "@mui/material";
import WordListItem from "../WordItem/WordListItem";
import { useNavigate } from "react-router-dom";
import { useSelector } from "react-redux";
import { AuthState } from "../../../store/store";
import axios from "axios";

type ComponentProps = {
  userWords: Array<WordItem>;
  handleDeleteWord: (word_ids: number[]) => void;
};

export type WordItem = {
  category: string;
  created_at: string;
  definition: string;
  translated_language: string;
  translation: string;
  user_id: number;
  word: string;
  word_type: string;
  word_id: number;
  correctness: number;
  total_attempts: number; 
};

const WordList = (props: ComponentProps) => {
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [selected, setSelected] = useState<number[]>([]); // stores words by word_id

  const navigate = useNavigate();
  const user_id = useSelector((state: AuthState) => state.user_id);
  const token = useSelector((state: AuthState) => state.token);

  const startIndex = page * rowsPerPage;
  const endIndex = startIndex + rowsPerPage;

  const handleChangePage = (
    event: React.MouseEvent<HTMLButtonElement> | null,
    newPage: number
  ) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const handleSelectAllClick = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.checked) {
      const newSelects = props.userWords.map((element) => element.word_id);
      setSelected(newSelects);
    } else {
      setSelected([]);
    }
  };

  const handleClick = (event: React.MouseEvent<unknown>, word_id: number) => {
    const selectedIndex = selected.indexOf(word_id);
    let newSelected: number[] = [];

    // Item is not present in selected array -> Add the item
    if (selectedIndex === -1) {
      newSelected = newSelected.concat(selected, word_id);
      // Item is the first in selected array -> Remove the item
    } else if (selectedIndex === 0) {
      newSelected = newSelected.concat(selected.slice(1));
      // Item is the last item in the array -> Remove the item
    } else if (selectedIndex === selected.length - 1) {
      newSelected = newSelected.concat(selected.slice(0, -1));
      // Item is in the array -> Remove the item
    } else if (selectedIndex > 0) {
      newSelected = newSelected.concat(
        selected.slice(0, selectedIndex),
        selected.slice(selectedIndex + 1)
      );
    }
    setSelected(newSelected);
  };

  const isSelected = (word_id: number) => selected.indexOf(word_id) !== -1;

  const handleCreateNewWord = () => {
    navigate(`/word-list/${user_id}/create-word`);
  };

  const handleDeleteWord = () => {
    if (selected.length === 0) {
      return;
    }
    axios({
      method: "delete",
      url: `http://127.0.0.1:8080/word-list/${user_id}`,
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      // Change backend to accommodate arrays
      data: { word_ids: selected },
    })
      .then((response) => {
        console.log(response);
        props.handleDeleteWord(response.data.words);
        setSelected([]);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  return (
    <>
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
        {selected.length !== 0 && (
          <Button
            sx={{
              color: "red",
              fontWeight: "bold",
              borderRadius: "8px",
              mb: 2,
              mr: 1,
              ml: "auto",
            }}
            onClick={handleDeleteWord}
          >
            Delete
          </Button>
        )}
      </Container>
      <TableContainer component={Paper} sx={{ mb: "100px" }}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>
                <Checkbox
                  indeterminate={
                    selected.length > 0 &&
                    selected.length < props.userWords.length
                  }
                  checked={selected.length === props.userWords.length}
                  onChange={handleSelectAllClick}
                />
              </TableCell>
              <TableCell sx={{ textAlign: "center", fontWeight: "bold" }}>
                Word
              </TableCell>
              <TableCell sx={{ textAlign: "center", fontWeight: "bold" }}>
                Category
              </TableCell>
              <TableCell sx={{ textAlign: "center", fontWeight: "bold" }}>
                Word Type
              </TableCell>
              <TableCell sx={{ textAlign: "center", fontWeight: "bold" }}>
                Translation
              </TableCell>
              <TableCell sx={{ textAlign: "center", fontWeight: "bold" }}>
                Translated Language
              </TableCell>
              <TableCell sx={{ textAlign: "center", fontWeight: "bold" }}>
                Definition
              </TableCell>
              <TableCell sx={{ textAlign: "center", fontWeight: "bold" }}>
                Correctness
              </TableCell>
              <TableCell sx={{ textAlign: "center", fontWeight: "bold" }}>
                Total Attempts
              </TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {props.userWords.slice(startIndex, endIndex).map((element) => {
              const isItemSelected = isSelected(element.word_id);
              return (
                <TableRow
                  key={element.word_id}
                  onClick={(event) => handleClick(event, element.word_id)}
                  selected={isItemSelected}
                >
                  <TableCell>
                    <Checkbox checked={isItemSelected} />
                  </TableCell>
                  <WordListItem word={element} />
                </TableRow>
              );
            })}
          </TableBody>
          <TableFooter>
            <TableRow>
              <TablePagination
                rowsPerPageOptions={[10, 20, 40]}
                count={props.userWords.length}
                rowsPerPage={rowsPerPage}
                page={page}
                onPageChange={handleChangePage}
                onRowsPerPageChange={handleChangeRowsPerPage}
              />
            </TableRow>
          </TableFooter>
        </Table>
      </TableContainer>
    </>
  );
};

export default WordList;
