let isFirstCall = true;
const prevPrices = new Map();
async function fetchDataAndIngest() {
    const url = 'http://api.coincap.io/v2/assets';
    const response = await fetch(url);
    const result = await response.json();
    const data = result.data;

    if (isFirstCall) {
        const snapshot_msg = { typ: "SnapshottingDone", old_val: null, new_val: null };
        await Deno[Deno.internal].core.ops.ingest(snapshot_msg);

        for (const record of data) {
            const msg = {
                typ: "Insert",
                old_val: null,
                new_val: { Name: record.name, Price: record.priceUsd },
            };
            await Deno[Deno.internal].core.ops.ingest(msg);
            prevPrices.set(record.name, record.priceUsd);
        }

        isFirstCall = false;
    } else {
        for (const record of data) {
            let prev = prevPrices.get(record.name);
            if (record.priceUsd === prev) continue;
            const msg = {
                typ: "Update",
                old_val: { Name: record.name, Price: prevPrices.get(record.name) },
                new_val: { Name: record.name, Price: record.priceUsd },
            };
            await Deno[Deno.internal].core.ops.ingest(msg);
            prevPrices.set(record.name, record.priceUsd);
        }
    }
}

fetchDataAndIngest();

setInterval(fetchDataAndIngest, 5000);
