import { useDozerEndpoint } from '@dozerjs/dozer-react';
import { EventType, FieldDefinition } from "@dozerjs/dozer/lib/esm/generated/protos/types_pb";
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Typography } from '@mui/material';

function PerformanceTable(props: {
  fields: FieldDefinition[] | undefined;
  records: Object[];
}) {
  const { fields, records } = props;

  const columns = fields?.filter(field => field.getName() !== 'ua') ?? [];

  return (
    <TableContainer sx={{ maxHeight: 200 }}>
      <Table stickyHeader>
        <TableHead>
          <TableRow>
            {
              columns.map((field, idx) => (
                <TableCell key={idx}>{field.getName()}</TableCell>
              ))
            }
          </TableRow>
        </TableHead>
        <TableBody>
          {
            records.map((row, idx) => {
              const data = row as Record<string, any>;
              return (
                <>
                  <TableRow key={idx}>
                    {fields?.map(field => {
                      let val = data[field.getName()]
                      return (<TableCell component="th" scope="row" key={field.getName()}>
                        {val && val.toString()}
                      </TableCell>)
                    })}
                  </TableRow>
                  <TableRow>
                    <TableCell style={{ paddingBottom: 0, paddingTop: 0 }} colSpan={columns.length}>
                      {data['ua']}
                    </TableCell>
                  </TableRow>
                </>
              )
            })
          }
        </TableBody>
      </Table>
    </TableContainer>
  )
}

export function Performance() {
  const { records, fields } = useDozerEndpoint('peformance', {
    watch: EventType.ALL,
  });

  return (
    <>
      <Typography variant="h3" color="inherit" component={'h3'}>
        Performance Table
      </Typography>
      <PerformanceTable records={records} fields={fields} />
    </>
  )
}
