import { useDozerEndpoint } from "@dozerjs/dozer-react";
import { Type } from "@dozerjs/dozer/lib/esm/generated/protos/types";
import { Order } from "@dozerjs/dozer/lib/esm/query_helper";
import { Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from "@mui/material";

function DeparturesCount() {
  const query = { orderBy: { start: Order.ASC } };
  const { records, fields } = useDozerEndpoint('departures_count', { query, watch: 0 });

  if (!fields?.length) {
    return null;
  }

  return <div>
    <TableContainer component={Paper}>
      <Table sx={{ minWidth: 650 }} aria-label="simple table">
        <TableHead>
          <TableRow>
            {fields.map(f => <TableCell key={f.getName()}>{f.getName()}</TableCell>)}
          </TableRow>
        </TableHead>
        <TableBody>
          {
            records.map(r => (
              <TableRow
                key={r[fields[0].getName()]}
                sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
              >
                {
                  fields.map(f => {
                    if (f.getName() === 'start') {
                      return <TableCell key={f.getName()}>{r[f.getName()]}:00 to {r[f.getName()] + 4}:00 </TableCell>;
                    } else if (f.getTyp() === Type.Point) {
                      return <TableCell key={f.getName()}>{r[f.getName()].getX()}, {r[f.getName()].getY()}</TableCell>;
                    } else {
                      return <TableCell key={f.getName()}>{r[f.getName()]}</TableCell>;
                    }
                  })
                }
              </TableRow>
            ))
          }
        </TableBody>
      </Table>
    </TableContainer>
  </div>;
}

export default DeparturesCount;