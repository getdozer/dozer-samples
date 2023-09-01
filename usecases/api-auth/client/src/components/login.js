import {
    Button,
    Paper,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    TextField
} from "@mui/material";
import { useNavigate } from "react-router-dom";
import { useState } from "react";

function Login() {
    const navigate = useNavigate();

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    const doLogin = () => {
        fetch('http://localhost:4000/admin/login', {
            method: 'POST',
            body: JSON.stringify({
                username,
                password
            }),
            headers: {
                'Content-type': 'application/json; charset=UTF-8',
            },
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.token) {
                    localStorage.setItem("token", data.token)
                    navigate("/admin/dashboard");
                } else {
                    alert(data.msg);
                }
                // Handle data
            })
            .catch((err) => {
                console.log(err.message);
            });
    }
    return <div>
        <TextField type="text"
            onChange={(newValue) => setUsername(newValue.target.value)}
            inputProps={{ min: 0, style: { textAlign: 'center', backgroundColor: 'white' } }}
            placeholder="Enter username"
        />
        <br />
        <br />
        <TextField type="password"
            onChange={(newValue) => setPassword(newValue.target.value)}
            inputProps={{ min: 0, style: { textAlign: 'center', backgroundColor: 'white' } }}
            placeholder="Enter password"
        />
        <br />
        <br />
        <Button variant="Contained" onClick={() => doLogin()}>Login</Button>
    </div>;
}

export default Login;