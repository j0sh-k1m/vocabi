import { WordItem } from "../WordList/WordList";
import { TableCell } from "@mui/material";

type ComponentProps = {
  word: WordItem;
};

const WordListItem = (props: ComponentProps) => {
  const { word } = props;

  return (
    <>
      <TableCell sx={{ textAlign: "center" }}>{word.word}</TableCell>
      <TableCell sx={{ textAlign: "center" }}>{word.category}</TableCell>
      <TableCell sx={{ textAlign: "center" }}>{word.word_type}</TableCell>
      <TableCell sx={{ textAlign: "center" }}>{word.translation}</TableCell>
      <TableCell sx={{ textAlign: "center" }}>{word.translated_language}</TableCell>
      <TableCell sx={{ textAlign: "center" }}>{word.definition}</TableCell>
      <TableCell sx={{ textAlign: "center" }}>{word.correctness}%</TableCell>
      <TableCell sx={{ textAlign: "center" }}>{word.total_attempts}</TableCell>
    </>
  );
};

export default WordListItem;
