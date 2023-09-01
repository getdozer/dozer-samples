import { Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from "@mui/material";
import { useParams } from "react-router-dom";
import { useDozerEndpoint } from "@dozerjs/dozer-react";
import { Type } from "@dozerjs/dozer/lib/esm/generated/protos/types";

function Customer() {
  let { key } = useParams();
  let query = {
    filter: {
      "C_CUSTKEY": Number(`${key}`)
    }
  }
  const { records, fields } = useDozerEndpoint('customers_orders', query);

  console.log(records);
  console.log(query);

  if (fields?.length === 0) {
    return null;
  }

  return <div>
    <h3>Customers</h3>
    <TableContainer component={Paper}>
      <Table sx={{ minWidth: 650 }} aria-label="simple table">
        <TableHead>
          <TableRow>
            {fields?.map(f => <TableCell key={`header-${f.getName()}`}>{f.getName()}</TableCell>)}
          </TableRow>
        </TableHead>
        <TableBody>
          {records?.map(r => (
            <TableRow
              key={r[fields[0].getName()]}
              sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
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

export default Customer;
