import { Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from "@mui/material";
import { useEffect, useState } from "react";
import { useDozerEvent, useDozerQuery } from "@dozerjs/dozer-react";
import { Order } from "@dozerjs/dozer/lib/esm/query_helper";
import { OperationType, Type } from "@dozerjs/dozer/lib/esm/generated/protos/types";

function DeparturesCount() {
  let query = { orderBy: { start: Order.ASC } };
  const { records, fields, connect } = useDozerQuery('departures_count', query);
  const { stream } = useDozerEvent([{ endpoint: 'departures_count' }]);
  connect(stream)


  if (fields.length === 0) {
    return null;
  }

  return <div>
    <TableContainer component={Paper}>
      <Table sx={{ minWidth: 650 }} aria-label="simple table">
        <TableHead>
          <TableRow>
            {fields.map(f => <TableCell>{f.getName()}</TableCell>)}
          </TableRow>
        </TableHead>
        <TableBody>
          {records.map(r => (
            <TableRow
              key={r.__dozer_record_id}
              sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
            >
              {fields.map(f => <>
                {f.getName() === 'start' ? <TableCell>{r[f.getName()]}:00 to {r[f.getName()] + 4}:00 </TableCell> :
                  <>
                    {(f.getTyp() === Type.Point) && <TableCell key={f.getName()}>{r[f.getName()].getX()}, {r[f.getName()].getY()}</TableCell>}
                    {(f.getTyp() !== Type.Point) && <TableCell key={f.getName()}>{r[f.getName()]}</TableCell>}
                  </>
                }

              </>)}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  </div>;
}

export default DeparturesCount;