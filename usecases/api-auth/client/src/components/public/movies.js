import { useEffect, useState } from "react";
import { DozerProvider } from '@dozerjs/dozer-react';
import MoviesList from "./moviesList";

function Movies() {
    let [token, setToken] = useState(null);

    useEffect(() => {
        if (localStorage.getItem('public_jwt')) {
            setToken(localStorage.getItem('public_jwt'));
        } else {
            fetch('http://localhost:4000/public/new_user', {
                method: 'GET',
                headers: {
                    'Content-type': 'application/json; charset=UTF-8',
                },
            })
                .then((response) => response.json())
                .then((data) => {
                    if (data.token) {
                        localStorage.setItem("public_jwt", data.token);
                        setToken(data.token);
                    } else {
                        alert(data.msg);
                    }
                    // Handle data
                })
                .catch((err) => {
                    console.log(err.message);
                });
        }
    }, []);

    if (!token) {
        return null;
    }

    return <DozerProvider value={{
        authToken: token,
    }}>
        <MoviesList token={token} />
    </DozerProvider>
}

export default Movies;