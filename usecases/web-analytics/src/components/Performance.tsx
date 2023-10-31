import { useDozerEndpoint } from '@dozerjs/dozer-react';
import { EventType, FieldDefinition } from "@dozerjs/dozer/lib/esm/generated/protos/types_pb";
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Typography } from '@mui/material';

function PerformanceTable(props: {
  fields: FieldDefinition[] | undefined;
  records: Object[];
}) {
  const { fields, records } = props;

  const columns = fields?.filter(field => field.getName() !== 'ua') ?? [];
  records.reverse();

  return (
    <TableContainer sx={{ maxHeight: 200 }}>
      <Table stickyHeader>
        <TableHead>
          <TableRow>
            {
              columns.map((field, idx) => (
                <TableCell key={idx}>{field.getName().toUpperCase()}</TableCell>
              ))
            }
          </TableRow>
        </TableHead>
        <TableBody>
          {
            records.map((row, idx) => {
              const data = row as Record<string, any>;
              return (
                <TableRow key={idx}>
                  {columns?.map(field => {
                    let val = data[field.getName()]
                    if (field.getName() === 'datetime') {
                      val = new Date(val).toLocaleString();
                    }
                    return (<TableCell component="th" scope="row" key={field.getName()}>
                      {val && val.toString()}
                    </TableCell>)
                  })}
                </TableRow>
              )
            })
          }
        </TableBody>
      </Table>
    </TableContainer>
  )
}

export function Performance() {
  const { records, fields } = useDozerEndpoint('performance', {
    watch: EventType.ALL,
  });

  const rows = [...records].reverse();

  return (
    <>
      <Typography variant="h3" color="inherit" component={'h3'}>
        Performance
      </Typography>
      <PerformanceTable records={rows} fields={fields} />
    </>
  )
}
