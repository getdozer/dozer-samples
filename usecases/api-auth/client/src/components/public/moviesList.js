import { useCallback, useEffect, useState } from "react";
import { useDozerEvent, useDozerQuery } from "@dozerjs/dozer-react";
import { Button, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from "@mui/material";
import { OperationType } from "@dozerjs/dozer/lib/esm/generated/protos/types";
import { types_pb } from "@dozerjs/dozer";
import { RecordMapper } from "@dozerjs/dozer/lib/esm/helper";

function MoviesList({ token }) {
    let [tickets, setTickets] = useState({});
    let [user, setUser] = useState({});

    const { records: movies } = useDozerQuery("only_movies");
    const { records: userBookingsRecords, fields: userBookingsFields } = useDozerQuery("user_bookings");
    const { records: usersRecords, fields: usersFields } = useDozerQuery("users");
    const { stream } = useDozerEvent([
        {
            endpoint: 'user_bookings',
            eventType: types_pb.EventType.ALL,
        },
        {
            endpoint: 'users',
            eventType: types_pb.EventType.ALL,
        },
    ]);

    const handleUserBookingsEvent = useCallback((data) => {
        if (userBookingsFields.length) {
            const mapper = new RecordMapper(userBookingsFields);
            setTickets(recs => {
                if (data.getTyp() === OperationType.UPDATE) {
                    let recNew = mapper.mapRecord(data.getNew());
                    let recOld = mapper.mapRecord(data.getOld());

                    return {
                        ...recs,
                        [recOld.movie_id]: { ...recOld },
                        [recNew.movie_id]: { ...recNew }
                    };
                }

                if (data.getTyp() === OperationType.INSERT) {
                    let recNew = mapper.mapRecord(data.getNew());

                    return {
                        [recNew.movie_id]: recNew,
                        ...recs
                    };
                }

                if (data.getTyp() === OperationType.DELETE && data.getNew()) {
                    let recOld = mapper.mapRecord(data.getNew());
                    return {
                        [recOld.movie_id]: null,
                        ...recs
                    };
                }

                return recs;
            });
        }
    }, [userBookingsFields]);

    const handleUsersEvent = useCallback((data) => {
        const mapper = new RecordMapper(usersFields);
        setUser(recs => {
            if (data.getTyp() === OperationType.UPDATE || data.getTyp() === OperationType.INSERT) {
                return mapper.mapRecord(data.getNew());
            }

            if (data.getTyp() === OperationType.DELETE && data.getNew()) {
                return null;
            }

            return recs;
        });
    }, [usersFields]);

    useEffect(() => {
        const r = {};
        userBookingsRecords.forEach(value => {
            r[value.movie_id] = value;
        })
        setTickets(r);
    }, [userBookingsRecords])

    useEffect(() => {
        setUser(usersRecords[0]);
    }, [usersRecords])

    useEffect(() => {
        const cb = (operation) => {
            if (operation.getEndpointName() === 'user_bookings') {
                handleUserBookingsEvent(operation);
            }
            if (operation.getEndpointName() === 'users') {
                handleUsersEvent(operation);
            }
        }
        stream?.on('data', cb);
        return () => {
            stream?.removeListener(cb);
        }
    }, [stream, handleUserBookingsEvent, handleUsersEvent])

    const buyTicket = (id) => {
        fetch('http://localhost:4000/public/book_movie', {
            method: 'POST',
            headers: {
                'Content-type': 'application/json; charset=UTF-8',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                movie_id: id
            })
        })
            .then((response) => response.json())
            .then((data) => {
                console.log('added booking');
            })
            .catch((err) => {
                alert(err.message)
            });
    }

    if (movies.length === 0) {
        return null;
    }

    return <div>
        <p>User: {user?.name}</p>
        <TableContainer component={Paper}>
            <Table sx={{ minWidth: 650 }} aria-label="simple table">
                <TableHead>
                    <TableRow>
                        <TableCell>ID</TableCell>
                        <TableCell>NAME</TableCell>
                        <TableCell>Tickets</TableCell>
                        <TableCell></TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {movies.map(f => (
                        <TableRow
                            key={f.id}
                            sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                        >
                            <TableCell component="th" scope="row">{f.id}</TableCell>
                            <TableCell>{f.name}</TableCell>
                            <TableCell align={"center"}>{tickets[f.id]?.count ?? 0}</TableCell>
                            <TableCell>
                                <Button onClick={() => buyTicket(f.id)} variant="contained" color="primary">Buy ticket</Button>
                            </TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </TableContainer>
    </div>;
}

export default MoviesList;
