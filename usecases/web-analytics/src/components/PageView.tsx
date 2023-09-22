import { useDozerEndpoint } from '@dozerjs/dozer-react';
import { EventType, FieldDefinition } from "@dozerjs/dozer/lib/esm/generated/protos/types_pb";
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Typography } from '@mui/material';
import { BarElement, CategoryScale, Chart as ChartJS, LinearScale, Title, Tooltip } from 'chart.js';
import { Bar } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
);

function PageViewChart(props: {
  fields: FieldDefinition[] | undefined;
  records: Object[];
}) {
  const { records } = props;

  const options = {
    indexAxis: 'y' as const,
    responsive: true,
    elements: {
      bar: {
        borderWidth: 6,
      },
    },
  };

  const labels = ['Home', 'Config', 'Schema'];

  const mapping = ['/', '/config', '/schema'];

  const data = {
    labels,
    datasets: [
      {
        data: records.reduce((data: [number, number, number], item: any) => {
          const index = mapping.indexOf(item['path']);
          if (index === -1) {
            return data;
          } else {
            data[index] += item['tp'];
            return data;
          }
        }, [0, 0, 0]),
        backgroundColor: '#A73D82',
      },
    ],
  };
  return <Bar options={options} data={data} height={120} style={{
    height: 120
  }}/>
}


function PageViewTable(props: {
  fields: FieldDefinition[] | undefined;
  records: Object[];
}) {
  const { fields, records } = props;

  return (
    <TableContainer sx={{ maxHeight: 200 }}>
      <Table stickyHeader>
        <TableHead>
          <TableRow>
            {
              fields?.map((field, idx) => (
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
                <TableRow key={idx}>
                  {fields?.map(field => {
                    let val = data[field.getName()]
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


export function PageView() {
  const { records, fields } = useDozerEndpoint('pv', {
    watch: EventType.ALL,
  });

  return (
    <>
      <Typography variant="h3" color="inherit" component={'h3'}>
        Page View
      </Typography>
      <PageViewTable records={records} fields={fields} />
      <PageViewChart records={records} fields={fields} />
    </>
  )
}
