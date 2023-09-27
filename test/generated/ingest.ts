/* eslint-disable */
import {
  ChannelCredentials,
  Client,
  ClientWritableStream,
  handleClientStreamingCall,
  makeGenericClientConstructor,
  Metadata,
} from "@grpc/grpc-js";
import type {
  CallOptions,
  ClientOptions,
  ClientUnaryCall,
  handleUnaryCall,
  ServiceError,
  UntypedServiceImplementation,
} from "@grpc/grpc-js";
import _m0 from "protobufjs/minimal";
import {
  OperationType as OperationType1,
  operationTypeFromJSON as operationTypeFromJSON2,
  operationTypeToJSON as operationTypeToJSON3,
  Record,
} from "./types";

/** The event types. */
export enum OperationType {
  /** INSERT - INSERT operation. */
  INSERT = 0,
  /** DELETE - DELETE operation. */
  DELETE = 1,
  /** UPDATE - UPDATE operation. */
  UPDATE = 2,
  UNRECOGNIZED = -1,
}

export function operationTypeFromJSON(object: any): OperationType {
  switch (object) {
    case 0:
    case "INSERT":
      return OperationType.INSERT;
    case 1:
    case "DELETE":
      return OperationType.DELETE;
    case 2:
    case "UPDATE":
      return OperationType.UPDATE;
    case -1:
    case "UNRECOGNIZED":
    default:
      return OperationType.UNRECOGNIZED;
  }
}

export function operationTypeToJSON(object: OperationType): string {
  switch (object) {
    case OperationType.INSERT:
      return "INSERT";
    case OperationType.DELETE:
      return "DELETE";
    case OperationType.UPDATE:
      return "UPDATE";
    case OperationType.UNRECOGNIZED:
    default:
      return "UNRECOGNIZED";
  }
}

export interface IngestRequest {
  schemaName: string;
  /** The operation type. */
  typ: OperationType1;
  /** Old record data, only applicable for UPDATE type. */
  old?:
    | Record
    | undefined;
  /** New record data. */
  new?: Record | undefined;
  seqNo: number;
}

export interface IngestResponse {
  seqNo: number;
}

export interface IngestArrowRequest {
  schemaName: string;
  /** Old record data, only applicable for UPDATE type. */
  records: Buffer;
  seqNo: number;
  metadata: { [key: number]: IngestMetadata };
}

export interface IngestArrowRequest_MetadataEntry {
  key: number;
  value?: IngestMetadata | undefined;
}

export interface IngestMetadata {
  /** The operation type. */
  typ: OperationType;
  /** Records with same primary key will have increasing version. */
  version: number;
}

function createBaseIngestRequest(): IngestRequest {
  return { schemaName: "", typ: 0, old: undefined, new: undefined, seqNo: 0 };
}

export const IngestRequest = {
  encode(message: IngestRequest, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.schemaName !== "") {
      writer.uint32(10).string(message.schemaName);
    }
    if (message.typ !== 0) {
      writer.uint32(16).int32(message.typ);
    }
    if (message.old !== undefined) {
      Record.encode(message.old, writer.uint32(26).fork()).ldelim();
    }
    if (message.new !== undefined) {
      Record.encode(message.new, writer.uint32(34).fork()).ldelim();
    }
    if (message.seqNo !== 0) {
      writer.uint32(40).uint32(message.seqNo);
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): IngestRequest {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseIngestRequest();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.schemaName = reader.string();
          continue;
        case 2:
          if (tag !== 16) {
            break;
          }

          message.typ = reader.int32() as any;
          continue;
        case 3:
          if (tag !== 26) {
            break;
          }

          message.old = Record.decode(reader, reader.uint32());
          continue;
        case 4:
          if (tag !== 34) {
            break;
          }

          message.new = Record.decode(reader, reader.uint32());
          continue;
        case 5:
          if (tag !== 40) {
            break;
          }

          message.seqNo = reader.uint32();
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): IngestRequest {
    return {
      schemaName: isSet(object.schemaName) ? String(object.schemaName) : "",
      typ: isSet(object.typ) ? operationTypeFromJSON2(object.typ) : 0,
      old: isSet(object.old) ? Record.fromJSON(object.old) : undefined,
      new: isSet(object.new) ? Record.fromJSON(object.new) : undefined,
      seqNo: isSet(object.seqNo) ? Number(object.seqNo) : 0,
    };
  },

  toJSON(message: IngestRequest): unknown {
    const obj: any = {};
    if (message.schemaName !== "") {
      obj.schemaName = message.schemaName;
    }
    if (message.typ !== 0) {
      obj.typ = operationTypeToJSON3(message.typ);
    }
    if (message.old !== undefined) {
      obj.old = Record.toJSON(message.old);
    }
    if (message.new !== undefined) {
      obj.new = Record.toJSON(message.new);
    }
    if (message.seqNo !== 0) {
      obj.seqNo = Math.round(message.seqNo);
    }
    return obj;
  },

  create<I extends Exact<DeepPartial<IngestRequest>, I>>(base?: I): IngestRequest {
    return IngestRequest.fromPartial(base ?? ({} as any));
  },
  fromPartial<I extends Exact<DeepPartial<IngestRequest>, I>>(object: I): IngestRequest {
    const message = createBaseIngestRequest();
    message.schemaName = object.schemaName ?? "";
    message.typ = object.typ ?? 0;
    message.old = (object.old !== undefined && object.old !== null) ? Record.fromPartial(object.old) : undefined;
    message.new = (object.new !== undefined && object.new !== null) ? Record.fromPartial(object.new) : undefined;
    message.seqNo = object.seqNo ?? 0;
    return message;
  },
};

function createBaseIngestResponse(): IngestResponse {
  return { seqNo: 0 };
}

export const IngestResponse = {
  encode(message: IngestResponse, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.seqNo !== 0) {
      writer.uint32(8).uint32(message.seqNo);
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): IngestResponse {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseIngestResponse();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 8) {
            break;
          }

          message.seqNo = reader.uint32();
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): IngestResponse {
    return { seqNo: isSet(object.seqNo) ? Number(object.seqNo) : 0 };
  },

  toJSON(message: IngestResponse): unknown {
    const obj: any = {};
    if (message.seqNo !== 0) {
      obj.seqNo = Math.round(message.seqNo);
    }
    return obj;
  },

  create<I extends Exact<DeepPartial<IngestResponse>, I>>(base?: I): IngestResponse {
    return IngestResponse.fromPartial(base ?? ({} as any));
  },
  fromPartial<I extends Exact<DeepPartial<IngestResponse>, I>>(object: I): IngestResponse {
    const message = createBaseIngestResponse();
    message.seqNo = object.seqNo ?? 0;
    return message;
  },
};

function createBaseIngestArrowRequest(): IngestArrowRequest {
  return { schemaName: "", records: Buffer.alloc(0), seqNo: 0, metadata: {} };
}

export const IngestArrowRequest = {
  encode(message: IngestArrowRequest, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.schemaName !== "") {
      writer.uint32(10).string(message.schemaName);
    }
    if (message.records.length !== 0) {
      writer.uint32(18).bytes(message.records);
    }
    if (message.seqNo !== 0) {
      writer.uint32(24).uint32(message.seqNo);
    }
    Object.entries(message.metadata).forEach(([key, value]) => {
      IngestArrowRequest_MetadataEntry.encode({ key: key as any, value }, writer.uint32(34).fork()).ldelim();
    });
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): IngestArrowRequest {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseIngestArrowRequest();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.schemaName = reader.string();
          continue;
        case 2:
          if (tag !== 18) {
            break;
          }

          message.records = reader.bytes() as Buffer;
          continue;
        case 3:
          if (tag !== 24) {
            break;
          }

          message.seqNo = reader.uint32();
          continue;
        case 4:
          if (tag !== 34) {
            break;
          }

          const entry4 = IngestArrowRequest_MetadataEntry.decode(reader, reader.uint32());
          if (entry4.value !== undefined) {
            message.metadata[entry4.key] = entry4.value;
          }
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): IngestArrowRequest {
    return {
      schemaName: isSet(object.schemaName) ? String(object.schemaName) : "",
      records: isSet(object.records) ? Buffer.from(bytesFromBase64(object.records)) : Buffer.alloc(0),
      seqNo: isSet(object.seqNo) ? Number(object.seqNo) : 0,
      metadata: isObject(object.metadata)
        ? Object.entries(object.metadata).reduce<{ [key: number]: IngestMetadata }>((acc, [key, value]) => {
          acc[Number(key)] = IngestMetadata.fromJSON(value);
          return acc;
        }, {})
        : {},
    };
  },

  toJSON(message: IngestArrowRequest): unknown {
    const obj: any = {};
    if (message.schemaName !== "") {
      obj.schemaName = message.schemaName;
    }
    if (message.records.length !== 0) {
      obj.records = base64FromBytes(message.records);
    }
    if (message.seqNo !== 0) {
      obj.seqNo = Math.round(message.seqNo);
    }
    if (message.metadata) {
      const entries = Object.entries(message.metadata);
      if (entries.length > 0) {
        obj.metadata = {};
        entries.forEach(([k, v]) => {
          obj.metadata[k] = IngestMetadata.toJSON(v);
        });
      }
    }
    return obj;
  },

  create<I extends Exact<DeepPartial<IngestArrowRequest>, I>>(base?: I): IngestArrowRequest {
    return IngestArrowRequest.fromPartial(base ?? ({} as any));
  },
  fromPartial<I extends Exact<DeepPartial<IngestArrowRequest>, I>>(object: I): IngestArrowRequest {
    const message = createBaseIngestArrowRequest();
    message.schemaName = object.schemaName ?? "";
    message.records = object.records ?? Buffer.alloc(0);
    message.seqNo = object.seqNo ?? 0;
    message.metadata = Object.entries(object.metadata ?? {}).reduce<{ [key: number]: IngestMetadata }>(
      (acc, [key, value]) => {
        if (value !== undefined) {
          acc[Number(key)] = IngestMetadata.fromPartial(value);
        }
        return acc;
      },
      {},
    );
    return message;
  },
};

function createBaseIngestArrowRequest_MetadataEntry(): IngestArrowRequest_MetadataEntry {
  return { key: 0, value: undefined };
}

export const IngestArrowRequest_MetadataEntry = {
  encode(message: IngestArrowRequest_MetadataEntry, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.key !== 0) {
      writer.uint32(8).uint32(message.key);
    }
    if (message.value !== undefined) {
      IngestMetadata.encode(message.value, writer.uint32(18).fork()).ldelim();
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): IngestArrowRequest_MetadataEntry {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseIngestArrowRequest_MetadataEntry();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 8) {
            break;
          }

          message.key = reader.uint32();
          continue;
        case 2:
          if (tag !== 18) {
            break;
          }

          message.value = IngestMetadata.decode(reader, reader.uint32());
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): IngestArrowRequest_MetadataEntry {
    return {
      key: isSet(object.key) ? Number(object.key) : 0,
      value: isSet(object.value) ? IngestMetadata.fromJSON(object.value) : undefined,
    };
  },

  toJSON(message: IngestArrowRequest_MetadataEntry): unknown {
    const obj: any = {};
    if (message.key !== 0) {
      obj.key = Math.round(message.key);
    }
    if (message.value !== undefined) {
      obj.value = IngestMetadata.toJSON(message.value);
    }
    return obj;
  },

  create<I extends Exact<DeepPartial<IngestArrowRequest_MetadataEntry>, I>>(
    base?: I,
  ): IngestArrowRequest_MetadataEntry {
    return IngestArrowRequest_MetadataEntry.fromPartial(base ?? ({} as any));
  },
  fromPartial<I extends Exact<DeepPartial<IngestArrowRequest_MetadataEntry>, I>>(
    object: I,
  ): IngestArrowRequest_MetadataEntry {
    const message = createBaseIngestArrowRequest_MetadataEntry();
    message.key = object.key ?? 0;
    message.value = (object.value !== undefined && object.value !== null)
      ? IngestMetadata.fromPartial(object.value)
      : undefined;
    return message;
  },
};

function createBaseIngestMetadata(): IngestMetadata {
  return { typ: 0, version: 0 };
}

export const IngestMetadata = {
  encode(message: IngestMetadata, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.typ !== 0) {
      writer.uint32(8).int32(message.typ);
    }
    if (message.version !== 0) {
      writer.uint32(16).uint32(message.version);
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): IngestMetadata {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseIngestMetadata();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 8) {
            break;
          }

          message.typ = reader.int32() as any;
          continue;
        case 2:
          if (tag !== 16) {
            break;
          }

          message.version = reader.uint32();
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): IngestMetadata {
    return {
      typ: isSet(object.typ) ? operationTypeFromJSON(object.typ) : 0,
      version: isSet(object.version) ? Number(object.version) : 0,
    };
  },

  toJSON(message: IngestMetadata): unknown {
    const obj: any = {};
    if (message.typ !== 0) {
      obj.typ = operationTypeToJSON(message.typ);
    }
    if (message.version !== 0) {
      obj.version = Math.round(message.version);
    }
    return obj;
  },

  create<I extends Exact<DeepPartial<IngestMetadata>, I>>(base?: I): IngestMetadata {
    return IngestMetadata.fromPartial(base ?? ({} as any));
  },
  fromPartial<I extends Exact<DeepPartial<IngestMetadata>, I>>(object: I): IngestMetadata {
    const message = createBaseIngestMetadata();
    message.typ = object.typ ?? 0;
    message.version = object.version ?? 0;
    return message;
  },
};

export type IngestServiceService = typeof IngestServiceService;
export const IngestServiceService = {
  ingest: {
    path: "/dozer.ingest.IngestService/ingest",
    requestStream: false,
    responseStream: false,
    requestSerialize: (value: IngestRequest) => Buffer.from(IngestRequest.encode(value).finish()),
    requestDeserialize: (value: Buffer) => IngestRequest.decode(value),
    responseSerialize: (value: IngestResponse) => Buffer.from(IngestResponse.encode(value).finish()),
    responseDeserialize: (value: Buffer) => IngestResponse.decode(value),
  },
  ingestStream: {
    path: "/dozer.ingest.IngestService/ingest_stream",
    requestStream: true,
    responseStream: false,
    requestSerialize: (value: IngestRequest) => Buffer.from(IngestRequest.encode(value).finish()),
    requestDeserialize: (value: Buffer) => IngestRequest.decode(value),
    responseSerialize: (value: IngestResponse) => Buffer.from(IngestResponse.encode(value).finish()),
    responseDeserialize: (value: Buffer) => IngestResponse.decode(value),
  },
  ingestArrow: {
    path: "/dozer.ingest.IngestService/ingest_arrow",
    requestStream: false,
    responseStream: false,
    requestSerialize: (value: IngestArrowRequest) => Buffer.from(IngestArrowRequest.encode(value).finish()),
    requestDeserialize: (value: Buffer) => IngestArrowRequest.decode(value),
    responseSerialize: (value: IngestResponse) => Buffer.from(IngestResponse.encode(value).finish()),
    responseDeserialize: (value: Buffer) => IngestResponse.decode(value),
  },
  ingestArrowStream: {
    path: "/dozer.ingest.IngestService/ingest_arrow_stream",
    requestStream: true,
    responseStream: false,
    requestSerialize: (value: IngestArrowRequest) => Buffer.from(IngestArrowRequest.encode(value).finish()),
    requestDeserialize: (value: Buffer) => IngestArrowRequest.decode(value),
    responseSerialize: (value: IngestResponse) => Buffer.from(IngestResponse.encode(value).finish()),
    responseDeserialize: (value: Buffer) => IngestResponse.decode(value),
  },
} as const;

export interface IngestServiceServer extends UntypedServiceImplementation {
  ingest: handleUnaryCall<IngestRequest, IngestResponse>;
  ingestStream: handleClientStreamingCall<IngestRequest, IngestResponse>;
  ingestArrow: handleUnaryCall<IngestArrowRequest, IngestResponse>;
  ingestArrowStream: handleClientStreamingCall<IngestArrowRequest, IngestResponse>;
}

export interface IngestServiceClient extends Client {
  ingest(
    request: IngestRequest,
    callback: (error: ServiceError | null, response: IngestResponse) => void,
  ): ClientUnaryCall;
  ingest(
    request: IngestRequest,
    metadata: Metadata,
    callback: (error: ServiceError | null, response: IngestResponse) => void,
  ): ClientUnaryCall;
  ingest(
    request: IngestRequest,
    metadata: Metadata,
    options: Partial<CallOptions>,
    callback: (error: ServiceError | null, response: IngestResponse) => void,
  ): ClientUnaryCall;
  ingestStream(
    callback: (error: ServiceError | null, response: IngestResponse) => void,
  ): ClientWritableStream<IngestRequest>;
  ingestStream(
    metadata: Metadata,
    callback: (error: ServiceError | null, response: IngestResponse) => void,
  ): ClientWritableStream<IngestRequest>;
  ingestStream(
    options: Partial<CallOptions>,
    callback: (error: ServiceError | null, response: IngestResponse) => void,
  ): ClientWritableStream<IngestRequest>;
  ingestStream(
    metadata: Metadata,
    options: Partial<CallOptions>,
    callback: (error: ServiceError | null, response: IngestResponse) => void,
  ): ClientWritableStream<IngestRequest>;
  ingestArrow(
    request: IngestArrowRequest,
    callback: (error: ServiceError | null, response: IngestResponse) => void,
  ): ClientUnaryCall;
  ingestArrow(
    request: IngestArrowRequest,
    metadata: Metadata,
    callback: (error: ServiceError | null, response: IngestResponse) => void,
  ): ClientUnaryCall;
  ingestArrow(
    request: IngestArrowRequest,
    metadata: Metadata,
    options: Partial<CallOptions>,
    callback: (error: ServiceError | null, response: IngestResponse) => void,
  ): ClientUnaryCall;
  ingestArrowStream(
    callback: (error: ServiceError | null, response: IngestResponse) => void,
  ): ClientWritableStream<IngestArrowRequest>;
  ingestArrowStream(
    metadata: Metadata,
    callback: (error: ServiceError | null, response: IngestResponse) => void,
  ): ClientWritableStream<IngestArrowRequest>;
  ingestArrowStream(
    options: Partial<CallOptions>,
    callback: (error: ServiceError | null, response: IngestResponse) => void,
  ): ClientWritableStream<IngestArrowRequest>;
  ingestArrowStream(
    metadata: Metadata,
    options: Partial<CallOptions>,
    callback: (error: ServiceError | null, response: IngestResponse) => void,
  ): ClientWritableStream<IngestArrowRequest>;
}

export const IngestServiceClient = makeGenericClientConstructor(
  IngestServiceService,
  "dozer.ingest.IngestService",
) as unknown as {
  new (address: string, credentials: ChannelCredentials, options?: Partial<ClientOptions>): IngestServiceClient;
  service: typeof IngestServiceService;
};

declare const self: any | undefined;
declare const window: any | undefined;
declare const global: any | undefined;
const tsProtoGlobalThis: any = (() => {
  if (typeof globalThis !== "undefined") {
    return globalThis;
  }
  if (typeof self !== "undefined") {
    return self;
  }
  if (typeof window !== "undefined") {
    return window;
  }
  if (typeof global !== "undefined") {
    return global;
  }
  throw "Unable to locate global object";
})();

function bytesFromBase64(b64: string): Uint8Array {
  if (tsProtoGlobalThis.Buffer) {
    return Uint8Array.from(tsProtoGlobalThis.Buffer.from(b64, "base64"));
  } else {
    const bin = tsProtoGlobalThis.atob(b64);
    const arr = new Uint8Array(bin.length);
    for (let i = 0; i < bin.length; ++i) {
      arr[i] = bin.charCodeAt(i);
    }
    return arr;
  }
}

function base64FromBytes(arr: Uint8Array): string {
  if (tsProtoGlobalThis.Buffer) {
    return tsProtoGlobalThis.Buffer.from(arr).toString("base64");
  } else {
    const bin: string[] = [];
    arr.forEach((byte) => {
      bin.push(String.fromCharCode(byte));
    });
    return tsProtoGlobalThis.btoa(bin.join(""));
  }
}

type Builtin = Date | Function | Uint8Array | string | number | boolean | undefined;

type DeepPartial<T> = T extends Builtin ? T
  : T extends Array<infer U> ? Array<DeepPartial<U>> : T extends ReadonlyArray<infer U> ? ReadonlyArray<DeepPartial<U>>
  : T extends {} ? { [K in keyof T]?: DeepPartial<T[K]> }
  : Partial<T>;

type KeysOfUnion<T> = T extends T ? keyof T : never;
type Exact<P, I extends P> = P extends Builtin ? P
  : P & { [K in keyof P]: Exact<P[K], I[K]> } & { [K in Exclude<keyof I, KeysOfUnion<P>>]: never };

function isObject(value: any): boolean {
  return typeof value === "object" && value !== null;
}

function isSet(value: any): boolean {
  return value !== null && value !== undefined;
}
