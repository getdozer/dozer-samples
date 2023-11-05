import { useEffect, useState } from "react";
import { Alert, Snackbar } from "@mui/material";
import { RecordMapper } from "@dozerjs/dozer/lib/esm/helper";
import { DozerProvider } from '@dozerjs/dozer-react';

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
import { types_pb } from '@dozerjs/dozer';
import { useDozerEvent, useDozerQuery } from "@dozerjs/dozer-react";

function pad(num, size) {
    num = num.toString();
    while (num.length < size) num = "0" + num;
    return num;
}

function Temperature() {
    const [open, setOpen] = useState(false);
    const query = { limit: 500000 };
    const { records: values, fields, consume } = useDozerQuery("events", query);
    const { stream } = useDozerEvent([
        {
            endpoint: 'events',
            eventType: types_pb.EventType.ALL,
        },
        {
            endpoint: 'alerts',
            eventType: types_pb.EventType.ALL,
        },
    ]);

    useEffect(() => {
        const cb = (operation) => {
            const mapper = new RecordMapper(fields)
            if (operation.getEndpointName() === 'events') {
                consume(operation);
                const newRecord = mapper.mapRecord(operation.getNew());
                if (newRecord && newRecord.temperature <= 22.8) {
                    setOpen(false);
                }
            }
            if (operation.getEndpointName() === 'alerts') {
                setOpen(true);
            }
        }
        stream?.on('data', cb);
        return () => {
            stream?.removeListener('data', cb);
        }
    }, [stream, fields]);

    const date = new Date();
    let day = pad(date.getDate(), 2);
    let month = pad(date.getMonth() + 1, 2);
    let year = date.getFullYear();

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
            anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
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

export default () => <DozerProvider><Temperature /></DozerProvider>;