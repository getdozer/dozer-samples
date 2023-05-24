import {useEffect, useState} from "react";
import {Alert, Snackbar} from "@mui/material";

import {
    Charts,
    ChartContainer,
    ChartRow,
    YAxis,
    styler,
    LineChart
} from "react-timeseries-charts";

import { TimeSeries } from "pondjs";
import { Index } from "pondjs";
import {useOnEvent, useQueryCommon} from "@dozerjs/dozer-react";

function pad(num, size) {
    num = num.toString();
    while (num.length < size) num = "0" + num;
    return num;
}

function Temperature(props) {
    const [values, setValues] = useState([]);
    const [open, setOpen] = useState(false);
    const query = { limit: 500000};
    const { records: events } = useQueryCommon("events", query);

    useOnEvent('events', (data, _1, _2, mapper) => {
        console.log(data.getNew().getValuesList());
        console.log(mapper);
        console.log(mapper.mapRecord(data.getNew().getValuesList()));
        setValues(recs => {
            return [...recs, mapper.mapRecord(data.getNew().getValuesList())]
        });

        if (mapper.mapRecord(data.getNew().getValuesList()).temperature <= 22.8) {
            setOpen(false);
        }
    });

    useOnEvent('alerts', (_data, _1, _2, mapper) => {
        setOpen(true);
    });

    const date = new Date();
    let day = pad(date.getDate(),2);
    let month = pad(date.getMonth() + 1, 2);
    let year = date.getFullYear();

    useEffect(() => {
        if(values.length === 0) {
            setValues(events);
        }
    }, [events])


    console.log(values);
    if (values.length === 0) {
        return null;
    }

    let currentDate = `${year}-${month}-${day}`;

    const data = {
        name: "temperature",
        columns: ["time", "temperature"],
        points: values.map(v => [`${currentDate}T${v.time}`, v.temperature])
    };

    let series = new TimeSeries({
        name: "temperature",
        columns: ["index", "temperature"],
        points: data.points.map(([d, value]) => [
            Index.getIndexString("1s", new Date(d)),
            value
        ])
    });

    const style = styler([
        {
            key: "temperature",
            color: "#A5C8E1",
            selected: "#2CB1CF"
        }
    ]);

    return (<>
        <Snackbar
            open={open}
            autoHideDuration={10000}
            onClose={() => setOpen(false)}
            anchorOrigin={{vertical: 'top', horizontal: 'right'}}
        >
            <Alert severity="error">
                It is superhot!
            </Alert>
        </Snackbar>
            <ChartContainer timeRange={series.range()}>
                <ChartRow height="150">
                    <YAxis
                        id="temperature"
                        label="Temperature"
                        min={series.min('temperature')}
                        max={series.max('temperature')}
                        format=".1f"
                        width="70"
                        type="linear"
                    />
                    <Charts>
                        <LineChart
                            axis="temperature"
                            style={style}
                            spacing={0}
                            columns={["temperature"]}
                            series={series}
                            minBarHeight={1}
                        />
                    </Charts>
                </ChartRow>
            </ChartContainer>
        </>
    );
}

export default Temperature;