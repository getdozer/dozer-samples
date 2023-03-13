import { Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from "@mui/material";
import { useNavigate } from "react-router-dom";
import { useQueryCommon } from "@getdozer/dozer-react";
import { Type } from "@getdozer/dozer-js/lib/esm/generated/protos/types";

function Airports() {
  const {records, fields} = useQueryCommon('airports');
  const navigate = useNavigate();

  if (fields.length === 0) {
    return null;
  }

  return <div>
    <TableContainer component={Paper}>
      <Table sx={{ minWidth: 650 }} aria-label="simple table">
        <TableHead>
          <TableRow>
            { fields.map(f => <TableCell>{f.getName()}</TableCell>) }
          </TableRow>
        </TableHead>
        <TableBody>
          { records.map(r => (
            <TableRow
              key={ r[fields[0].getName()] }
              sx={ { '&:last-child td, &:last-child th': { border: 0 } } }
              onClick={ () => navigate(`/airport/${r[fields[0].getName()]}`)}
            >
              { fields.map(f => <>
                {(f.getTyp() === Type.Point) && <TableCell>{r[f.getName()].getX()}, {r[f.getName()].getY()}</TableCell>}
                {(f.getTyp() !== Type.Point) && <TableCell>{r[f.getName()]}</TableCell>}
              </>)}
            </TableRow>
          )) }
        </TableBody>
      </Table>
    </TableContainer>
  </div>;
}

export default Airports;