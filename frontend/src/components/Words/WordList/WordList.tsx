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
} from "@mui/material";
import WordListItem from "../WordItem/WordListItem";

type ComponentProps = {
  userWords: Array<WordItem>;
};

export type WordItem = {
  category: string;
  correct: number;
  created_at: string;
  definition: string;
  incorrect: number;
  translated_language: string;
  translation: string;
  user_id: number;
  word: string;
  word_type: string;
  word_id: number;
};

const WordList = (props: ComponentProps) => {
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [selected, setSelected] = useState<number[]>([]);

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

  return (
    <>
      <TableContainer component={Paper}>
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
              <TableCell>Word</TableCell>
              <TableCell>Category</TableCell>
              <TableCell>Word Type</TableCell>
              <TableCell>Translation</TableCell>
              <TableCell>Translated Language</TableCell>
              <TableCell>Definition</TableCell>
              <TableCell>Correct</TableCell>
              <TableCell>Incorrect</TableCell>
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
                  {/* Use the WordListItem component here */}
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
