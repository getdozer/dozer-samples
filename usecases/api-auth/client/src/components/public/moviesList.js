import {useEffect, useState} from "react";
import {ApiClient} from "@dozerjs/dozer";
import {Button, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow} from "@mui/material";
import {useOnEvent} from "@dozerjs/dozer-react";
import {OperationType} from "@dozerjs/dozer/lib/esm/generated/protos/types";

function MoviesList({ token }) {
    let [movies, setMovies] = useState([]);
    let [tickets, setTickets] = useState({});
    let [user, setUser] = useState({});

    useEffect(() => {
        if (token) {
            let client = new ApiClient("only_movies", {authToken: token});
            client.query().then(response => {
                setMovies(response[1]);
            });

            let bookings_client = new ApiClient("user_bookings", {authToken: token});
            bookings_client.query().then(response => {
                let r = {};
                console.log(response);
                response[1].forEach(value => {
                    r[value.movie_id] = value;
                })
                setTickets(r);
            });

            let users_client = new ApiClient("users", {authToken: token});
            users_client.query().then(response => {
                setUser(response[1][0]);
            });
        }
    }, [token]);

    useOnEvent('user_bookings', (data, _1, primaryIndexKeys, mapper) => {
            setTickets(recs => {
                if (data.getTyp() === OperationType.UPDATE) {
                    let recNew = mapper.mapRecord(data.getNew().getValuesList());
                    let recOld = mapper.mapRecord(data.getOld().getValuesList());

                    return {
                        ...recs,
                        [recOld.movie_id]: {...recOld},
                        [recNew.movie_id]: {...recNew}
                    };
                }

                if (data.getTyp() === OperationType.INSERT) {
                    let recNew = mapper.mapRecord(data.getNew().getValuesList());

                    return {
                        [recNew.movie_id]: recNew,
                        ...recs
                    };
                }

                if (data.getTyp() === OperationType.DELETE && data.getNew()) {
                    let recOld = mapper.mapRecord(data.getNew().getValuesList());
                    return {
                        [recOld.movie_id]: null,
                        ...recs
                    };
                }

                return recs;
            });
        },
        token)

    useOnEvent('users', (data, _1, primaryIndexKeys, mapper) => {
            setUser(recs => {
                if (data.getTyp() === OperationType.UPDATE || data.getTyp() === OperationType.INSERT) {
                    return mapper.mapRecord(data.getNew().getValuesList());
                }

                if (data.getTyp() === OperationType.DELETE && data.getNew()) {
                    return null;
                }

                return recs;
            });
        },
        token)
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
                    { movies.map(f => (
                        <TableRow
                            key={ f.id }
                            sx={ { '&:last-child td, &:last-child th': { border: 0 } } }
                        >
                            <TableCell component="th" scope="row">{ f.id }</TableCell>
                            <TableCell>{ f.name }</TableCell>
                            <TableCell align={"center"}>{ tickets[f.id]?.count ?? 0 }</TableCell>
                            <TableCell>
                                <Button onClick={() => buyTicket(f.id)} variant="contained" color="primary">Buy ticket</Button>
                            </TableCell>
                        </TableRow>
                    )) }
                </TableBody>
            </Table>
        </TableContainer>
    </div>;
}

export default MoviesList;
