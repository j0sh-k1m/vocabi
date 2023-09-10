import { useState } from "react";
import {
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  SelectChangeEvent,
} from "@mui/material";
import { ModuleData } from "../../pages/user/Stats/StatsPage";

type ComponentProps = {
  moduleStats: ModuleData[];
  getSelectedModule: (module: string) => void;
};

const ModuleSelect = (props: ComponentProps) => {
  const [selectedOption, setSelectedOption] = useState(
    ""
  );

  const handleChange = (event: SelectChangeEvent<string>) => {
    setSelectedOption(event.target.value);
    props.getSelectedModule(event.target.value);
  };

  return (
    <div>
      <FormControl sx={{ m: 1, width: 300 }}>
        <InputLabel id="demo-simple-select-autowidth-label">Module</InputLabel>
        <Select
          value={selectedOption}
          onChange={handleChange}
          autoWidth
          label="Module"
        >
          {props.moduleStats.map((module) => (
            <MenuItem key={module.module} value={module.module}>
              {module.module}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
    </div>
  );
};

export default ModuleSelect;
