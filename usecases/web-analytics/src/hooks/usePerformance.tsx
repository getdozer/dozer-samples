import { IngestRequest } from '@dozerjs/dozer/lib/esm/generated/protos/ingest_pb';
import { OperationType, Record, Value } from '@dozerjs/dozer/lib/esm/generated/protos/types_pb';
import { DozerIngestClient } from '@dozerjs/dozer/lib/esm/ingest_client';
import { useEffect, useRef, useState } from 'react';
import { Metric, onCLS, onFCP, onFID, onINP, onLCP, onTTFB } from 'web-vitals';
import { useVid } from './useVid';
import { Timestamp } from 'google-protobuf/google/protobuf/timestamp_pb';

export function usePerformance() {
  const vid = useVid();
  const client = new DozerIngestClient('performance', 'http://127.0.0.1:8085');
  const [metrics, setMetrics] = useState<Partial<{
    CLS: number,
    FCP: number,
    FID: number,
    INP: number,
    LCP: number,
    TTFB: number,
  }>>({});

  const metricsRef = useRef(metrics);

  const updateMetrics = (metric: Metric) => {
    metricsRef.current = Object.assign({}, metricsRef.current, { [metric.name]: metric.value });
    setMetrics(metricsRef.current);
  };

  useEffect(() => {
    onCLS(updateMetrics);
    onFID(updateMetrics);
    onLCP(updateMetrics);
    onINP(updateMetrics);
    onFCP(updateMetrics);
    onTTFB(updateMetrics);
  }, [])

  const now = useRef(Date.now());
  const old = useRef<Value[]>();
  const version = useRef(1);

  useEffect(() => {
    console.log(JSON.stringify(metrics))
    const request = new IngestRequest();
    request.setSchemaName('performance');

    request.setTyp(version.current === 1 ? OperationType.INSERT : OperationType.UPDATE);

    request.addNew(new Value().setStringValue(vid));
    request.addNew(new Value().setIntValue(now.current));
    request.addNew(new Value().setStringValue(window.navigator.userAgent));
    metrics.CLS ? request.addNew(new Value().setFloatValue(metrics.CLS)) : request.addNew();
    metrics.FID ? request.addNew(new Value().setFloatValue(metrics.FID)) : request.addNew();
    metrics.LCP ? request.addNew(new Value().setFloatValue(metrics.LCP)) : request.addNew();
    metrics.INP ? request.addNew(new Value().setFloatValue(metrics.INP)) : request.addNew();
    metrics.FCP ? request.addNew(new Value().setFloatValue(metrics.FCP)) : request.addNew();
    metrics.TTFB ? request.addNew(new Value().setFloatValue(metrics.TTFB)) : request.addNew();

    old.current && request.setOldList(old.current);

    old.current = request.getNewList();

    version.current += 1;

    client.ingest_raw(request);
  }, [metrics])
}

