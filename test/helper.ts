/* eslint-disable no-await-in-loop */

import assert from 'assert';
import { ChildProcess, execSync, spawn } from 'child_process';
import { credentials, Metadata } from '@grpc/grpc-js';
import { promisify } from 'util';
import { CommonGrpcServiceClient, GetEndpointsRequest, GetEndpointsResponse } from './generated/common';

export const onClose = (code?: number) => {
  assert.equal(code || 0, 0);
};

export const initProcessHandler = (childProcess: ChildProcess) => {
  childProcess.on('message', onClose);
  childProcess.on('exit', onClose);
  childProcess.on('close', onClose);
  childProcess.on('error', (err) => {
    throw err;
  });
};
export const initDozer = async () => {
  const dozer = spawn('dozer', ['run'], { stdio: 'inherit' });
  initProcessHandler(dozer);
  return dozer;
};

export class CommonGrpc {
  private readonly client: CommonGrpcServiceClient = new CommonGrpcServiceClient('localhost:50051', credentials.createInsecure());

  public async getEndpoints(
    params: GetEndpointsRequest,
    metadata: Metadata = new Metadata(),
  ): Promise<GetEndpointsResponse> {
    return promisify(this.client.getEndpoints.bind(this.client, params, metadata, {}))();
  }
}

export async function checkEndpoints() {
  try {
    const client = new CommonGrpc();
    // const client = new CommonGrpcServiceClient();
    const endpointsRes = await client.getEndpoints({});
    const { endpoints } = endpointsRes;
    console.log(endpoints);
    assert(endpoints.length > 0);
    return true;
  } catch (err) {
    console.log('dozer is not up yet, retrying...');
    return false;
  }
}

export async function assertEndpointsWithRetry(
  maxRetries: number = 10,
  retryInterval: number = 500,
) {
  let i = 0;
  let endpointsReady = false;

  while (i < maxRetries) {
    console.log('calling dozer endpoints...');
    endpointsReady = await checkEndpoints();
    if (endpointsReady) {
      break;
    }
    await new Promise((r) => { setTimeout(r, retryInterval); });
    i += 1;
  }
  assert(endpointsReady, 'get endpoints failed');
}
