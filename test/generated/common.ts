/* eslint-disable */
import {
  ChannelCredentials,
  Client,
  ClientReadableStream,
  handleServerStreamingCall,
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
import Long from "long";
import _m0 from "protobufjs/minimal";
import { EventFilter, FieldDefinition, Operation, RecordWithId } from "./types";

/** The _common_ gRPC API handles Pull and Push queries of all endpoints with a single service, `CommonGrpcService`. */

/** Request for `count` and `query`. */
export interface QueryRequest {
  /** The name of the endpoint to query. */
  endpoint: string;
  /** JSON query string. */
  query?: string | undefined;
}

/** Response for `count`. */
export interface CountResponse {
  /** The number of records satisfying the query. */
  count: number;
}

/** Request for `OnEvent`. */
export interface OnEventRequest {
  /** The endpoints to subscribe to. Key is the endpoint name, value is the filter. */
  endpoints: { [key: string]: EventFilter };
}

export interface OnEventRequest_EndpointsEntry {
  key: string;
  value?: EventFilter | undefined;
}

/** Request for `getFields`. */
export interface GetFieldsRequest {
  /** The endpoint name. */
  endpoint: string;
}

/** Response for `getFields`. */
export interface GetFieldsResponse {
  /** The list of indexes of the keys that are used as the primary index. */
  primaryIndex: number[];
  /** The list of field definitions. */
  fields: FieldDefinition[];
}

/** Response for `query`. */
export interface QueryResponse {
  /** The list of field definitions. */
  fields: FieldDefinition[];
  /** The list of record data. */
  records: RecordWithId[];
}

/** Request for `getEndpoints`. */
export interface GetEndpointsRequest {
}

/** Response for `getEndpoints`. */
export interface GetEndpointsResponse {
  /** List of endpoint names. */
  endpoints: string[];
}

function createBaseQueryRequest(): QueryRequest {
  return { endpoint: "", query: undefined };
}

export const QueryRequest = {
  encode(message: QueryRequest, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.endpoint !== "") {
      writer.uint32(10).string(message.endpoint);
    }
    if (message.query !== undefined) {
      writer.uint32(18).string(message.query);
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): QueryRequest {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseQueryRequest();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.endpoint = reader.string();
          continue;
        case 2:
          if (tag !== 18) {
            break;
          }

          message.query = reader.string();
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): QueryRequest {
    return {
      endpoint: isSet(object.endpoint) ? String(object.endpoint) : "",
      query: isSet(object.query) ? String(object.query) : undefined,
    };
  },

  toJSON(message: QueryRequest): unknown {
    const obj: any = {};
    if (message.endpoint !== "") {
      obj.endpoint = message.endpoint;
    }
    if (message.query !== undefined) {
      obj.query = message.query;
    }
    return obj;
  },

  create<I extends Exact<DeepPartial<QueryRequest>, I>>(base?: I): QueryRequest {
    return QueryRequest.fromPartial(base ?? ({} as any));
  },
  fromPartial<I extends Exact<DeepPartial<QueryRequest>, I>>(object: I): QueryRequest {
    const message = createBaseQueryRequest();
    message.endpoint = object.endpoint ?? "";
    message.query = object.query ?? undefined;
    return message;
  },
};

function createBaseCountResponse(): CountResponse {
  return { count: 0 };
}

export const CountResponse = {
  encode(message: CountResponse, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.count !== 0) {
      writer.uint32(8).uint64(message.count);
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): CountResponse {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseCountResponse();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 8) {
            break;
          }

          message.count = longToNumber(reader.uint64() as Long);
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): CountResponse {
    return { count: isSet(object.count) ? Number(object.count) : 0 };
  },

  toJSON(message: CountResponse): unknown {
    const obj: any = {};
    if (message.count !== 0) {
      obj.count = Math.round(message.count);
    }
    return obj;
  },

  create<I extends Exact<DeepPartial<CountResponse>, I>>(base?: I): CountResponse {
    return CountResponse.fromPartial(base ?? ({} as any));
  },
  fromPartial<I extends Exact<DeepPartial<CountResponse>, I>>(object: I): CountResponse {
    const message = createBaseCountResponse();
    message.count = object.count ?? 0;
    return message;
  },
};

function createBaseOnEventRequest(): OnEventRequest {
  return { endpoints: {} };
}

export const OnEventRequest = {
  encode(message: OnEventRequest, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    Object.entries(message.endpoints).forEach(([key, value]) => {
      OnEventRequest_EndpointsEntry.encode({ key: key as any, value }, writer.uint32(10).fork()).ldelim();
    });
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): OnEventRequest {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseOnEventRequest();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          const entry1 = OnEventRequest_EndpointsEntry.decode(reader, reader.uint32());
          if (entry1.value !== undefined) {
            message.endpoints[entry1.key] = entry1.value;
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

  fromJSON(object: any): OnEventRequest {
    return {
      endpoints: isObject(object.endpoints)
        ? Object.entries(object.endpoints).reduce<{ [key: string]: EventFilter }>((acc, [key, value]) => {
          acc[key] = EventFilter.fromJSON(value);
          return acc;
        }, {})
        : {},
    };
  },

  toJSON(message: OnEventRequest): unknown {
    const obj: any = {};
    if (message.endpoints) {
      const entries = Object.entries(message.endpoints);
      if (entries.length > 0) {
        obj.endpoints = {};
        entries.forEach(([k, v]) => {
          obj.endpoints[k] = EventFilter.toJSON(v);
        });
      }
    }
    return obj;
  },

  create<I extends Exact<DeepPartial<OnEventRequest>, I>>(base?: I): OnEventRequest {
    return OnEventRequest.fromPartial(base ?? ({} as any));
  },
  fromPartial<I extends Exact<DeepPartial<OnEventRequest>, I>>(object: I): OnEventRequest {
    const message = createBaseOnEventRequest();
    message.endpoints = Object.entries(object.endpoints ?? {}).reduce<{ [key: string]: EventFilter }>(
      (acc, [key, value]) => {
        if (value !== undefined) {
          acc[key] = EventFilter.fromPartial(value);
        }
        return acc;
      },
      {},
    );
    return message;
  },
};

function createBaseOnEventRequest_EndpointsEntry(): OnEventRequest_EndpointsEntry {
  return { key: "", value: undefined };
}

export const OnEventRequest_EndpointsEntry = {
  encode(message: OnEventRequest_EndpointsEntry, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.key !== "") {
      writer.uint32(10).string(message.key);
    }
    if (message.value !== undefined) {
      EventFilter.encode(message.value, writer.uint32(18).fork()).ldelim();
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): OnEventRequest_EndpointsEntry {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseOnEventRequest_EndpointsEntry();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.key = reader.string();
          continue;
        case 2:
          if (tag !== 18) {
            break;
          }

          message.value = EventFilter.decode(reader, reader.uint32());
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): OnEventRequest_EndpointsEntry {
    return {
      key: isSet(object.key) ? String(object.key) : "",
      value: isSet(object.value) ? EventFilter.fromJSON(object.value) : undefined,
    };
  },

  toJSON(message: OnEventRequest_EndpointsEntry): unknown {
    const obj: any = {};
    if (message.key !== "") {
      obj.key = message.key;
    }
    if (message.value !== undefined) {
      obj.value = EventFilter.toJSON(message.value);
    }
    return obj;
  },

  create<I extends Exact<DeepPartial<OnEventRequest_EndpointsEntry>, I>>(base?: I): OnEventRequest_EndpointsEntry {
    return OnEventRequest_EndpointsEntry.fromPartial(base ?? ({} as any));
  },
  fromPartial<I extends Exact<DeepPartial<OnEventRequest_EndpointsEntry>, I>>(
    object: I,
  ): OnEventRequest_EndpointsEntry {
    const message = createBaseOnEventRequest_EndpointsEntry();
    message.key = object.key ?? "";
    message.value = (object.value !== undefined && object.value !== null)
      ? EventFilter.fromPartial(object.value)
      : undefined;
    return message;
  },
};

function createBaseGetFieldsRequest(): GetFieldsRequest {
  return { endpoint: "" };
}

export const GetFieldsRequest = {
  encode(message: GetFieldsRequest, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.endpoint !== "") {
      writer.uint32(10).string(message.endpoint);
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): GetFieldsRequest {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseGetFieldsRequest();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.endpoint = reader.string();
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): GetFieldsRequest {
    return { endpoint: isSet(object.endpoint) ? String(object.endpoint) : "" };
  },

  toJSON(message: GetFieldsRequest): unknown {
    const obj: any = {};
    if (message.endpoint !== "") {
      obj.endpoint = message.endpoint;
    }
    return obj;
  },

  create<I extends Exact<DeepPartial<GetFieldsRequest>, I>>(base?: I): GetFieldsRequest {
    return GetFieldsRequest.fromPartial(base ?? ({} as any));
  },
  fromPartial<I extends Exact<DeepPartial<GetFieldsRequest>, I>>(object: I): GetFieldsRequest {
    const message = createBaseGetFieldsRequest();
    message.endpoint = object.endpoint ?? "";
    return message;
  },
};

function createBaseGetFieldsResponse(): GetFieldsResponse {
  return { primaryIndex: [], fields: [] };
}

export const GetFieldsResponse = {
  encode(message: GetFieldsResponse, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    writer.uint32(10).fork();
    for (const v of message.primaryIndex) {
      writer.int32(v);
    }
    writer.ldelim();
    for (const v of message.fields) {
      FieldDefinition.encode(v!, writer.uint32(18).fork()).ldelim();
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): GetFieldsResponse {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseGetFieldsResponse();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag === 8) {
            message.primaryIndex.push(reader.int32());

            continue;
          }

          if (tag === 10) {
            const end2 = reader.uint32() + reader.pos;
            while (reader.pos < end2) {
              message.primaryIndex.push(reader.int32());
            }

            continue;
          }

          break;
        case 2:
          if (tag !== 18) {
            break;
          }

          message.fields.push(FieldDefinition.decode(reader, reader.uint32()));
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): GetFieldsResponse {
    return {
      primaryIndex: Array.isArray(object?.primaryIndex) ? object.primaryIndex.map((e: any) => Number(e)) : [],
      fields: Array.isArray(object?.fields) ? object.fields.map((e: any) => FieldDefinition.fromJSON(e)) : [],
    };
  },

  toJSON(message: GetFieldsResponse): unknown {
    const obj: any = {};
    if (message.primaryIndex?.length) {
      obj.primaryIndex = message.primaryIndex.map((e) => Math.round(e));
    }
    if (message.fields?.length) {
      obj.fields = message.fields.map((e) => FieldDefinition.toJSON(e));
    }
    return obj;
  },

  create<I extends Exact<DeepPartial<GetFieldsResponse>, I>>(base?: I): GetFieldsResponse {
    return GetFieldsResponse.fromPartial(base ?? ({} as any));
  },
  fromPartial<I extends Exact<DeepPartial<GetFieldsResponse>, I>>(object: I): GetFieldsResponse {
    const message = createBaseGetFieldsResponse();
    message.primaryIndex = object.primaryIndex?.map((e) => e) || [];
    message.fields = object.fields?.map((e) => FieldDefinition.fromPartial(e)) || [];
    return message;
  },
};

function createBaseQueryResponse(): QueryResponse {
  return { fields: [], records: [] };
}

export const QueryResponse = {
  encode(message: QueryResponse, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    for (const v of message.fields) {
      FieldDefinition.encode(v!, writer.uint32(10).fork()).ldelim();
    }
    for (const v of message.records) {
      RecordWithId.encode(v!, writer.uint32(18).fork()).ldelim();
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): QueryResponse {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseQueryResponse();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.fields.push(FieldDefinition.decode(reader, reader.uint32()));
          continue;
        case 2:
          if (tag !== 18) {
            break;
          }

          message.records.push(RecordWithId.decode(reader, reader.uint32()));
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): QueryResponse {
    return {
      fields: Array.isArray(object?.fields) ? object.fields.map((e: any) => FieldDefinition.fromJSON(e)) : [],
      records: Array.isArray(object?.records) ? object.records.map((e: any) => RecordWithId.fromJSON(e)) : [],
    };
  },

  toJSON(message: QueryResponse): unknown {
    const obj: any = {};
    if (message.fields?.length) {
      obj.fields = message.fields.map((e) => FieldDefinition.toJSON(e));
    }
    if (message.records?.length) {
      obj.records = message.records.map((e) => RecordWithId.toJSON(e));
    }
    return obj;
  },

  create<I extends Exact<DeepPartial<QueryResponse>, I>>(base?: I): QueryResponse {
    return QueryResponse.fromPartial(base ?? ({} as any));
  },
  fromPartial<I extends Exact<DeepPartial<QueryResponse>, I>>(object: I): QueryResponse {
    const message = createBaseQueryResponse();
    message.fields = object.fields?.map((e) => FieldDefinition.fromPartial(e)) || [];
    message.records = object.records?.map((e) => RecordWithId.fromPartial(e)) || [];
    return message;
  },
};

function createBaseGetEndpointsRequest(): GetEndpointsRequest {
  return {};
}

export const GetEndpointsRequest = {
  encode(_: GetEndpointsRequest, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): GetEndpointsRequest {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseGetEndpointsRequest();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(_: any): GetEndpointsRequest {
    return {};
  },

  toJSON(_: GetEndpointsRequest): unknown {
    const obj: any = {};
    return obj;
  },

  create<I extends Exact<DeepPartial<GetEndpointsRequest>, I>>(base?: I): GetEndpointsRequest {
    return GetEndpointsRequest.fromPartial(base ?? ({} as any));
  },
  fromPartial<I extends Exact<DeepPartial<GetEndpointsRequest>, I>>(_: I): GetEndpointsRequest {
    const message = createBaseGetEndpointsRequest();
    return message;
  },
};

function createBaseGetEndpointsResponse(): GetEndpointsResponse {
  return { endpoints: [] };
}

export const GetEndpointsResponse = {
  encode(message: GetEndpointsResponse, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    for (const v of message.endpoints) {
      writer.uint32(10).string(v!);
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): GetEndpointsResponse {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseGetEndpointsResponse();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.endpoints.push(reader.string());
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): GetEndpointsResponse {
    return { endpoints: Array.isArray(object?.endpoints) ? object.endpoints.map((e: any) => String(e)) : [] };
  },

  toJSON(message: GetEndpointsResponse): unknown {
    const obj: any = {};
    if (message.endpoints?.length) {
      obj.endpoints = message.endpoints;
    }
    return obj;
  },

  create<I extends Exact<DeepPartial<GetEndpointsResponse>, I>>(base?: I): GetEndpointsResponse {
    return GetEndpointsResponse.fromPartial(base ?? ({} as any));
  },
  fromPartial<I extends Exact<DeepPartial<GetEndpointsResponse>, I>>(object: I): GetEndpointsResponse {
    const message = createBaseGetEndpointsResponse();
    message.endpoints = object.endpoints?.map((e) => e) || [];
    return message;
  },
};

/**
 * CommonGrpcService allows developers to query data from various endpoints.
 *
 * The service supports both Pull and Push queries. It provides methods to return metadata about the fields that can be used to construct the data types dynamically.
 *
 * This is preferred while working with libraries or in the case of dynamic scenarios and interpreted languages.
 */
export type CommonGrpcServiceService = typeof CommonGrpcServiceService;
export const CommonGrpcServiceService = {
  /**
   * Counts the number of records satisfying the given query. See [Query](../query) for the query format.
   *
   * If no query is specified, total number of records will be returned.
   */
  count: {
    path: "/dozer.common.CommonGrpcService/count",
    requestStream: false,
    responseStream: false,
    requestSerialize: (value: QueryRequest) => Buffer.from(QueryRequest.encode(value).finish()),
    requestDeserialize: (value: Buffer) => QueryRequest.decode(value),
    responseSerialize: (value: CountResponse) => Buffer.from(CountResponse.encode(value).finish()),
    responseDeserialize: (value: Buffer) => CountResponse.decode(value),
  },
  /**
   * Performs query on an endpoint. See [Query](../query) for the query format.
   *
   * If no query is specified, the first 50 records will be returned.
   */
  query: {
    path: "/dozer.common.CommonGrpcService/query",
    requestStream: false,
    responseStream: false,
    requestSerialize: (value: QueryRequest) => Buffer.from(QueryRequest.encode(value).finish()),
    requestDeserialize: (value: Buffer) => QueryRequest.decode(value),
    responseSerialize: (value: QueryResponse) => Buffer.from(QueryResponse.encode(value).finish()),
    responseDeserialize: (value: Buffer) => QueryResponse.decode(value),
  },
  /**
   * Subscribes to the Dozer event stream, optionally applies a filter. See [Query](../query) for the filter format.
   *
   * This API is unstable and may change in the future.
   */
  onEvent: {
    path: "/dozer.common.CommonGrpcService/OnEvent",
    requestStream: false,
    responseStream: true,
    requestSerialize: (value: OnEventRequest) => Buffer.from(OnEventRequest.encode(value).finish()),
    requestDeserialize: (value: Buffer) => OnEventRequest.decode(value),
    responseSerialize: (value: Operation) => Buffer.from(Operation.encode(value).finish()),
    responseDeserialize: (value: Buffer) => Operation.decode(value),
  },
  /** Gets all the endpoints Dozer is currently serving. */
  getEndpoints: {
    path: "/dozer.common.CommonGrpcService/getEndpoints",
    requestStream: false,
    responseStream: false,
    requestSerialize: (value: GetEndpointsRequest) => Buffer.from(GetEndpointsRequest.encode(value).finish()),
    requestDeserialize: (value: Buffer) => GetEndpointsRequest.decode(value),
    responseSerialize: (value: GetEndpointsResponse) => Buffer.from(GetEndpointsResponse.encode(value).finish()),
    responseDeserialize: (value: Buffer) => GetEndpointsResponse.decode(value),
  },
  /** Gets the field description of an endpoint. */
  getFields: {
    path: "/dozer.common.CommonGrpcService/getFields",
    requestStream: false,
    responseStream: false,
    requestSerialize: (value: GetFieldsRequest) => Buffer.from(GetFieldsRequest.encode(value).finish()),
    requestDeserialize: (value: Buffer) => GetFieldsRequest.decode(value),
    responseSerialize: (value: GetFieldsResponse) => Buffer.from(GetFieldsResponse.encode(value).finish()),
    responseDeserialize: (value: Buffer) => GetFieldsResponse.decode(value),
  },
} as const;

export interface CommonGrpcServiceServer extends UntypedServiceImplementation {
  /**
   * Counts the number of records satisfying the given query. See [Query](../query) for the query format.
   *
   * If no query is specified, total number of records will be returned.
   */
  count: handleUnaryCall<QueryRequest, CountResponse>;
  /**
   * Performs query on an endpoint. See [Query](../query) for the query format.
   *
   * If no query is specified, the first 50 records will be returned.
   */
  query: handleUnaryCall<QueryRequest, QueryResponse>;
  /**
   * Subscribes to the Dozer event stream, optionally applies a filter. See [Query](../query) for the filter format.
   *
   * This API is unstable and may change in the future.
   */
  onEvent: handleServerStreamingCall<OnEventRequest, Operation>;
  /** Gets all the endpoints Dozer is currently serving. */
  getEndpoints: handleUnaryCall<GetEndpointsRequest, GetEndpointsResponse>;
  /** Gets the field description of an endpoint. */
  getFields: handleUnaryCall<GetFieldsRequest, GetFieldsResponse>;
}

export interface CommonGrpcServiceClient extends Client {
  /**
   * Counts the number of records satisfying the given query. See [Query](../query) for the query format.
   *
   * If no query is specified, total number of records will be returned.
   */
  count(
    request: QueryRequest,
    callback: (error: ServiceError | null, response: CountResponse) => void,
  ): ClientUnaryCall;
  count(
    request: QueryRequest,
    metadata: Metadata,
    callback: (error: ServiceError | null, response: CountResponse) => void,
  ): ClientUnaryCall;
  count(
    request: QueryRequest,
    metadata: Metadata,
    options: Partial<CallOptions>,
    callback: (error: ServiceError | null, response: CountResponse) => void,
  ): ClientUnaryCall;
  /**
   * Performs query on an endpoint. See [Query](../query) for the query format.
   *
   * If no query is specified, the first 50 records will be returned.
   */
  query(
    request: QueryRequest,
    callback: (error: ServiceError | null, response: QueryResponse) => void,
  ): ClientUnaryCall;
  query(
    request: QueryRequest,
    metadata: Metadata,
    callback: (error: ServiceError | null, response: QueryResponse) => void,
  ): ClientUnaryCall;
  query(
    request: QueryRequest,
    metadata: Metadata,
    options: Partial<CallOptions>,
    callback: (error: ServiceError | null, response: QueryResponse) => void,
  ): ClientUnaryCall;
  /**
   * Subscribes to the Dozer event stream, optionally applies a filter. See [Query](../query) for the filter format.
   *
   * This API is unstable and may change in the future.
   */
  onEvent(request: OnEventRequest, options?: Partial<CallOptions>): ClientReadableStream<Operation>;
  onEvent(
    request: OnEventRequest,
    metadata?: Metadata,
    options?: Partial<CallOptions>,
  ): ClientReadableStream<Operation>;
  /** Gets all the endpoints Dozer is currently serving. */
  getEndpoints(
    request: GetEndpointsRequest,
    callback: (error: ServiceError | null, response: GetEndpointsResponse) => void,
  ): ClientUnaryCall;
  getEndpoints(
    request: GetEndpointsRequest,
    metadata: Metadata,
    callback: (error: ServiceError | null, response: GetEndpointsResponse) => void,
  ): ClientUnaryCall;
  getEndpoints(
    request: GetEndpointsRequest,
    metadata: Metadata,
    options: Partial<CallOptions>,
    callback: (error: ServiceError | null, response: GetEndpointsResponse) => void,
  ): ClientUnaryCall;
  /** Gets the field description of an endpoint. */
  getFields(
    request: GetFieldsRequest,
    callback: (error: ServiceError | null, response: GetFieldsResponse) => void,
  ): ClientUnaryCall;
  getFields(
    request: GetFieldsRequest,
    metadata: Metadata,
    callback: (error: ServiceError | null, response: GetFieldsResponse) => void,
  ): ClientUnaryCall;
  getFields(
    request: GetFieldsRequest,
    metadata: Metadata,
    options: Partial<CallOptions>,
    callback: (error: ServiceError | null, response: GetFieldsResponse) => void,
  ): ClientUnaryCall;
}

export const CommonGrpcServiceClient = makeGenericClientConstructor(
  CommonGrpcServiceService,
  "dozer.common.CommonGrpcService",
) as unknown as {
  new (address: string, credentials: ChannelCredentials, options?: Partial<ClientOptions>): CommonGrpcServiceClient;
  service: typeof CommonGrpcServiceService;
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

type Builtin = Date | Function | Uint8Array | string | number | boolean | undefined;

type DeepPartial<T> = T extends Builtin ? T
  : T extends Array<infer U> ? Array<DeepPartial<U>> : T extends ReadonlyArray<infer U> ? ReadonlyArray<DeepPartial<U>>
  : T extends {} ? { [K in keyof T]?: DeepPartial<T[K]> }
  : Partial<T>;

type KeysOfUnion<T> = T extends T ? keyof T : never;
type Exact<P, I extends P> = P extends Builtin ? P
  : P & { [K in keyof P]: Exact<P[K], I[K]> } & { [K in Exclude<keyof I, KeysOfUnion<P>>]: never };

function longToNumber(long: Long): number {
  if (long.gt(Number.MAX_SAFE_INTEGER)) {
    throw new tsProtoGlobalThis.Error("Value is larger than Number.MAX_SAFE_INTEGER");
  }
  return long.toNumber();
}

if (_m0.util.Long !== Long) {
  _m0.util.Long = Long as any;
  _m0.configure();
}

function isObject(value: any): boolean {
  return typeof value === "object" && value !== null;
}

function isSet(value: any): boolean {
  return value !== null && value !== undefined;
}
