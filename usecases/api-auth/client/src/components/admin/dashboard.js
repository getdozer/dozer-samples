import { Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from "@mui/material";
import { DozerProvider, useDozerEvent, useDozerQuery } from "@dozerjs/dozer-react";
import { Navigate } from "react-router-dom";

function pad(num, size) {
    num = num.toString();
    while (num.length < size) num = "0" + num;
    return num;
}

function DataTable() {
    const query = { limit: 500000 };
    const { records, connect } = useDozerQuery("movies_with_bookings", query);
    const { stream } = useDozerEvent([{ endpoint: 'movies_with_bookings' }]);
    connect(stream);

    if (records.length === 0) {
        return null;
    }
    return (
        <TableContainer component={Paper}>
            <Table sx={{ minWidth: 650 }} aria-label="simple table">
                <TableHead>
                    <TableRow>
                        <TableCell>ID</TableCell>
                        <TableCell>NAME</TableCell>
                        <TableCell>BOOKINGS</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {records.map(f => (
                        <TableRow
                            key={f.id}
                            sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                        >
                            <TableCell component="th" scope="row">{f.id}</TableCell>
                            <TableCell>{f.name}</TableCell>
                            <TableCell align="center">{f.count}</TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </TableContainer>
    )
}

function Dashboard() {
    const token = localStorage.getItem('token');
    if (!token) {
        return <Navigate to="/admin" />
    }


    return <DozerProvider value={{
        authToken: token,
    }}>
        <h3>Admin dashboard</h3>
        <DataTable />
    </DozerProvider>;
}

export default Dashboard;