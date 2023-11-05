import { Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from "@mui/material";
import { useParams } from "react-router-dom";
import { DozerProvider, useDozerQuery } from "@dozerjs/dozer-react";

function DataTable() {
    const { records: flights } = useDozerQuery("flights");
    return (
        <TableContainer component={Paper}>
            <Table sx={{ minWidth: 650 }} aria-label="simple table">
                <TableHead>
                    <TableRow>
                        <TableCell>FLIGHT NO</TableCell>
                        <TableCell>ROUTE</TableCell>
                        {/*/!*<TableCell>TOTALP RICE</TableCell>*!/*/}
                        {/*<TableCell>COMMENT</TableCell>*/}
                    </TableRow>
                </TableHead>
                <TableBody>
                    {flights.map(f => (
                        <TableRow
                            key={f.flight_no}
                            sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                        >
                            <TableCell component="th" scope="row">{f.flight_no}</TableCell>
                            <TableCell>{f.departure_airport} -> {f.arrival_airport}</TableCell>
                            {/*/!*<TableCell>{ JSON.stringify(o.O_TOTALPRICE) }</TableCell>*!/*/}
                            {/*<TableCell>{ o.O_COMMENT }</TableCell>*/}
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </TableContainer>
    )
}

function Orders() {
    const params = useParams();
    return (
        <DozerProvider value={{
            authToken: params.jwt
        }}>
            <h3>My Orders</h3>
            <DataTable />
        </DozerProvider >
    );
}

export default Orders;