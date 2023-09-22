import { IngestRequest } from '@dozerjs/dozer/lib/esm/generated/protos/ingest_pb';
import { OperationType, Record, Value } from '@dozerjs/dozer/lib/esm/generated/protos/types_pb';
import { DozerIngestClient } from '@dozerjs/dozer/lib/esm/ingest_client';
import { useInterval } from "ahooks";
import { useCallback, useEffect, useRef } from 'react';
import { useLocation } from 'react-router-dom';
import { tableFromArrays } from '@apache-arrow/ts';
import { useVid } from '../hooks/useVid';

export function usePageView () {
  const vid = useVid();
  const { pathname } = useLocation();
  const client = new DozerIngestClient('pv', 'http://127.0.0.1:8085');

  const now = Date.now();
  const version = useRef(1);

  const report = useCallback(() => {
    const request = new IngestRequest();
    request.setSchemaName('pv');

    request.setTyp(version.current === 1 ? OperationType.INSERT : OperationType.UPDATE);

    const record = new Record();
    record.addValues(new Value().setStringValue(vid));
    record.addValues(new Value().setIntValue(now));
    record.addValues(new Value().setStringValue(pathname));
    record.addValues(new Value().setIntValue(Date.now() - now));
    record.setVersion(version.current++);
    request.setNew(record);

    client.ingest_raw(request);
  }, [])

  useEffect(() => {
    if (version.current === 1) {
      report();
    } else {
      return () => {
        report();
      }
    }
  }, []);

  useInterval(() => {
    report();
  }, 5000, {
    immediate: false,
  });
}

