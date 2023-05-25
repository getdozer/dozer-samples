import {useEffect, useState} from "react";
import {Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow} from "@mui/material";

import {useOnEvent, useQueryCommon} from "@dozerjs/dozer-react";
import {OperationType} from "@dozerjs/dozer/lib/esm/generated/protos/types";
import {useNavigate} from "react-router-dom";

function pad(num, size) {
    num = num.toString();
    while (num.length < size) num = "0" + num;
    return num;
}

function Dashboard() {
    const navigate = useNavigate();
    const token = localStorage.getItem('token');
    if (!token) {
        navigate("/admin");
    }
    const [values, setValues] = useState([]);
    const query = { limit: 500000};
    const { records: events } = useQueryCommon("movies_with_bookings", query, token);

    useOnEvent('movies_with_bookings', (data, _1, primaryIndexKeys, mapper) => {
        setValues(recs => {
            if (data.getTyp() === OperationType.UPDATE) {
                let oldValue = mapper.mapRecord(data.getOld().getValuesList());
                let existingIndex = recs.findIndex(v => primaryIndexKeys.every(k => v[k] === oldValue[k]))

                if (existingIndex > -1) {
                    recs[existingIndex] = mapper.mapRecord(data.getNew().getValuesList());

                    return [...recs]
                }
            }

            if (data.getTyp() === OperationType.INSERT) {
                console.log('insert');
                return [...recs, mapper.mapRecord(data.getNew().getValuesList())]
            }

            if (data.getTyp() === OperationType.DELETE && data.getNew()) {
                console.log('delete');
                let oldValue = mapper.mapRecord(data.getNew().getValuesList());
                let existingIndex = recs.findIndex(v => primaryIndexKeys.every(k => {
                    return v[k] === oldValue[k]
                }))

                if (existingIndex > -1) {
                    recs.splice(existingIndex, 1);
                    return [...recs]
                }
            }

            return recs;
        });
    }, token);


    useEffect(() => {
        if(values.length === 0) {
            setValues(events);
        }
    }, [events])


    if (values.length === 0) {
        return null;
    }

    return <div>
        <h3>Admin dashboard</h3>
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
                    { values.map(f => (
                        <TableRow
                            key={ f.id }
                            sx={ { '&:last-child td, &:last-child th': { border: 0 } } }
                        >
                            <TableCell component="th" scope="row">{ f.id }</TableCell>
                            <TableCell>{ f.name }</TableCell>
                            <TableCell align="center">{ f.count }</TableCell>
                        </TableRow>
                    )) }
                </TableBody>
            </Table>
        </TableContainer>
    </div>;
}

export default Dashboard;