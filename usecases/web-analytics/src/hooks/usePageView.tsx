import { IngestRequest } from '@dozerjs/dozer/lib/esm/generated/protos/ingest_pb';
import { OperationType, Value } from '@dozerjs/dozer/lib/esm/generated/protos/types_pb';
import { DozerIngestClient } from '@dozerjs/dozer/lib/esm/ingest_client';
import { useInterval } from "ahooks";
import { useCallback, useEffect, useRef } from 'react';
import { useLocation } from 'react-router-dom';
import { useVid } from '../hooks/useVid';

export function usePageView() {
  const vid = useVid();
  const { pathname } = useLocation();
  const client = new DozerIngestClient('pv', 'http://127.0.0.1:8085');

  const now = useRef(Date.now());
  const old = useRef<Value[]>();
  const version = useRef(1);

  const report = useCallback(() => {
    const request = new IngestRequest();
    request.setSchemaName('pv');

    request.setTyp(version.current === 1 ? OperationType.INSERT : OperationType.UPDATE);

    request.addNew(new Value().setStringValue(vid));
    request.addNew(new Value().setIntValue(now.current));
    request.addNew(new Value().setStringValue(pathname));
    request.addNew(new Value().setIntValue(Date.now() - now.current));
    old.current && request.setOldList(old.current);

    old.current = request.getNewList();

    version.current += 1;

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
  }, 1000, {
    immediate: false,
  });
}

