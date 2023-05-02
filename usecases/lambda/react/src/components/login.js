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
import {useNavigate} from "react-router-dom";
import {useState} from "react";
import {AuthClient} from "@dozerjs/dozer";

const MASTER_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjYWNoZV91c2VyIiwic3ViIjoiYXBpQGRvemVyLmNvbSIsImV4cCI6MTY4MDUxMjI4MTA0MSwiYWNjZXNzIjoiQWxsIn0.lajm2jvzD-LtCn0tmuti4f1SR0P8YQwZ9zC5uEOgDtk'
function Login() {
    const navigate = useNavigate();

    const [username, setUsername] = useState("");

    const doLogin = () => {
        let client = new AuthClient({authToken: MASTER_TOKEN, serverAddress: 'http://localhost:50051'})

        let access = {
            Custom: {
                flights: {
                    filter: {
                        flight_id: {"$eq": parseInt(username)}
                    },
                    fields: []
                }
            }
        };

        console.log(JSON.stringify(access));
        client.getAuthToken(JSON.stringify(access)).then(response => {
            navigate("/orders/" + response.getToken());
        })
    }
    return <div>
        <TextField type="text"
                   onChange={(newValue) => setUsername(newValue.target.value)}
                   inputProps={{min: 0, style: {textAlign: 'center', backgroundColor: 'white'}}}
                   placeholder="Enter username"
        />
        <br/>
        <br/>
        <TextField type="password"
                   inputProps={{min: 0, style: {textAlign: 'center', backgroundColor: 'white'}}}
                   placeholder="Enter password"
        />
        <br/>
        <br/>
        <Button variant="Contained" onClick={() => doLogin()}>Login</Button>
    </div>;
}

export default Login;