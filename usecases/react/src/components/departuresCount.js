import { Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from "@mui/material";
import { useOnEvent, useQueryCommon } from "@getdozer/dozer-react";
import { OperationType, Type } from "@getdozer/dozer-js/lib/esm/generated/protos/types";
import { useEffect, useState } from "react";

function DeparturesCount() {
  const [counts, setCounts] = useState([]);
  const {records, fields} = useQueryCommon('departures_count', "{\"$order_by\":{\"start\":\"asc\"}}");

  useOnEvent('departures_count', (data, fields, primaryIndexKeys, mapper) => {
    if (fields.length) {
      setCounts(records => {
        if (data.getTyp() === OperationType.UPDATE) {
          let oldValue = mapper.mapRecord(data.getOld().getValuesList());
          let existingIndex = records.findIndex(v => v[primaryIndexKeys[0]] === oldValue[primaryIndexKeys[0]])

          if (records.length > 0) {
            if (existingIndex > -1) {
              records[existingIndex] = mapper.mapRecord(data.getNew().getValuesList());
              return [...records];
            } else {
              return [...records, mapper.mapRecord(data.getNew().getValuesList())];
            }
          }
        } else if (data.getTyp() === OperationType.INSERT) {
          return [...records, mapper.mapRecord(data.getNew().getValuesList())];
        }

        return records;
      });
    }
  });


  useEffect(() => {
    setCounts(records);
  }, [records])

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
          { counts.map(r => (
            <TableRow
              key={ r[fields[0].getName()] }
              sx={ { '&:last-child td, &:last-child th': { border: 0 } } }
            >
              { fields.map(f => <>
                {f.getName() === 'start' ? <TableCell>{r[f.getName()]}:00 to {r[f.getName()] + 4}:00 </TableCell>:
                  <>
                    {(f.getTyp() === Type.Point) && <TableCell>{r[f.getName()].getX()}, {r[f.getName()].getY()}</TableCell>}
                {(f.getTyp() !== Type.Point) && <TableCell>{r[f.getName()]}</TableCell>}
                  </>
                }

              </>)}
            </TableRow>
          )) }
        </TableBody>
      </Table>
    </TableContainer>
  </div>;
}

export default DeparturesCount;