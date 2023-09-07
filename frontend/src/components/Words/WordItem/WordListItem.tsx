import { WordItem } from "../WordList/WordList";
import { TableCell } from "@mui/material";

type ComponentProps = {
  word: WordItem;
};

const WordListItem = (props: ComponentProps) => {
  const { word } = props;

  return (
    <>
      <TableCell>{word.word}</TableCell>
      <TableCell>{word.category}</TableCell>
      <TableCell>{word.word_type}</TableCell>
      <TableCell>{word.translation}</TableCell>
      <TableCell>{word.translated_language}</TableCell>
      <TableCell>{word.definition}</TableCell>
      <TableCell>{word.correct}</TableCell>
      <TableCell>{word.incorrect}</TableCell>
    </>
  );
};

export default WordListItem;
