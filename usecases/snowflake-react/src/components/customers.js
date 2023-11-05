import { Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from "@mui/material";
import { useNavigate } from "react-router-dom";
import { useDozerQuery } from "@dozerjs/dozer-react";
import { Type } from "@dozerjs/dozer/lib/esm/generated/protos/types";

function Customers() {
  const { records, fields } = useDozerQuery('customers');
  const navigate = useNavigate();

  if (fields.length === 0) {
    return null;
  }

  console.log(records);
  console.log(fields);
  console.log(fields[0].getName());

  return <div>
    <h3>Customers</h3>
    <TableContainer component={Paper}>
      <Table sx={{ minWidth: 650 }} aria-label="simple table">
        <TableHead>
          <TableRow>
            {fields.map(f => <TableCell key={`header-${f.getName()}`}>{f.getName()}</TableCell>)}
          </TableRow>
        </TableHead>
        <TableBody>
          {records.map(r => (
            <TableRow
              key={r.__dozer_record_id}
              sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
              onClick={() => navigate(`/customer/${r[fields[0].getName()]}`)}
            >
              {fields.map(f => <>
                {(f.getTyp() === Type.Decimal) && <TableCell key={f.getName()}>{r[f.getName()].getLo() / 10 ** r[f.getName()].getFlags()}</TableCell>}
                {(f.getTyp() !== Type.Decimal) && <TableCell key={f.getName()}>{r[f.getName()]}</TableCell>}
              </>)}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  </div>;
}

export default Customers;
