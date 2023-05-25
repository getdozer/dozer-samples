const express = require('express')
const app = express()
const {ApiClient, AuthClient} = require("@dozerjs/dozer");
const axios = require('axios');
const cors = require('cors');
const { faker } = require('@faker-js/faker');

app.use(cors())

app.use(express.json());

const { Client } = require('pg')

const client = new Client({
    host: '127.0.0.1',
    port: 5438,
    database: 'omdb',
    user: 'postgres',
    password: 'postgres',
});

client.connect();

const MASTER_TOKEN = process.env.MASTER_TOKEN;

app.post('/admin/login', function(req, res){
    console.log(req.body);
    if(!req.body.username || !req.body.password){
        res.status(400);
        res.json({msg: "Invalid details!"});
    } else {
        if (req.body.username == 'admin' && req.body.password == 'admin') {
            const data = JSON.stringify("All");
            const config = {
                method: 'post',
                url: 'http://127.0.0.1:8080/auth/token',
                headers: {
                    'Authorization': 'Bearer ' + MASTER_TOKEN,
                    'Content-Type': 'application/json'
                },
                data : data
            };

            axios(config)
                .then(function (response) {
                    res.status(200);
                    res.json(response.data);
                })
                .catch(function (error) {
                    console.log(error);
                    res.status(500).send('Something broke!')
                });
        } else {
            res.status(400);
            res.json({msg: "Invalid details!"});
        }
    }
})

app.get('/public/new_user', function(req, response){
    let name = faker.internet.userName();
    let uuid = faker.datatype.uuid();

    const text = 'INSERT INTO users(id, name) VALUES($1, $2) RETURNING *'
    const values = [uuid, name]
    client.query(text, values, (err, res) => {
        if (err) {
            response.status(500).send('Something broke!')
        } else {
            const data = JSON.stringify({
                "Custom": {
                    "bookings": {
                        "filter": {
                            "user_id": {
                                "$eq": uuid
                            }
                        },
                        "fields": []
                    },
                    "only_movies": {
                        "filter": {},
                        "limit": 100,
                        "fields": []
                    },
                    "user_bookings": {
                        "filter": {
                            "user_id": {
                                "$eq": uuid
                            }
                        },
                        "fields": []
                    },
                    "users": {
                        "filter": {
                            "id": {
                                "$eq": uuid
                            }
                        },
                        "fields": []
                    }
                }
            });

            const config = {
                method: 'post',
                url: 'http://127.0.0.1:8080/auth/token',
                headers: {
                    'Authorization': 'Bearer ' + MASTER_TOKEN,
                    'Content-Type': 'application/json'
                },
                data : data
            };

            axios(config)
                .then(function (r) {
                    response.status(200);
                    response.json(r.data);
                })
                .catch(function (error) {
                    console.log(error);
                    response.status(500).json({msg: 'Something broke!'})
                });
        }
    })
})

app.post('/public/book_movie', function(req, response){
    const config = {
        method: 'get',
        url: 'http://127.0.0.1:8080/api/users',
        headers: {
            'Authorization': req.get('Authorization'),
            'Content-Type': 'application/json'
        },
    };

    axios(config)
        .then(function (r) {
            const text = 'INSERT INTO bookings(user_id, movie_id) VALUES($1, $2) RETURNING *'
            const values = [r.data[0].id, req.body.movie_id];

            client.query(text, values, (err, res) => {
                if (err) {
                    console.log(err.stack)
                    response.status(500).json({msg: 'Something broke!'})
                } else {
                    response.status(200).json({});
                }
            });
        })
        .catch(function (error) {
            console.log(error);
            response.status(500).json({msg: 'Something broke!'})
        });
})

app.use((err, request, response, next) => {
    // log the error, for now just console.log
    console.log(err)
    response.status(500).send('Something broke!')
})

app.listen(4000)
