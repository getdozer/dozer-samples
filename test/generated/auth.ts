/* eslint-disable */
import { ChannelCredentials, Client, makeGenericClientConstructor, Metadata } from "@grpc/grpc-js";
import type {
  CallOptions,
  ClientOptions,
  ClientUnaryCall,
  handleUnaryCall,
  ServiceError,
  UntypedServiceImplementation,
} from "@grpc/grpc-js";
import _m0 from "protobufjs/minimal";

/** The _common_ gRPC API handles Pull and Push queries of all endpoints with a single service, `AuthGrpcService`. */

/** Request for `GetAuthTokenRequest`. */
export interface GetAuthTokenRequest {
  accessFilter: string;
}

/** Response for `GetAuthTokenResponse`. */
export interface GetAuthTokenResponse {
  /** Generate token for access */
  token: string;
}

function createBaseGetAuthTokenRequest(): GetAuthTokenRequest {
  return { accessFilter: "" };
}

export const GetAuthTokenRequest = {
  encode(message: GetAuthTokenRequest, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.accessFilter !== "") {
      writer.uint32(10).string(message.accessFilter);
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): GetAuthTokenRequest {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseGetAuthTokenRequest();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.accessFilter = reader.string();
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): GetAuthTokenRequest {
    return { accessFilter: isSet(object.accessFilter) ? String(object.accessFilter) : "" };
  },

  toJSON(message: GetAuthTokenRequest): unknown {
    const obj: any = {};
    if (message.accessFilter !== "") {
      obj.accessFilter = message.accessFilter;
    }
    return obj;
  },

  create<I extends Exact<DeepPartial<GetAuthTokenRequest>, I>>(base?: I): GetAuthTokenRequest {
    return GetAuthTokenRequest.fromPartial(base ?? ({} as any));
  },
  fromPartial<I extends Exact<DeepPartial<GetAuthTokenRequest>, I>>(object: I): GetAuthTokenRequest {
    const message = createBaseGetAuthTokenRequest();
    message.accessFilter = object.accessFilter ?? "";
    return message;
  },
};

function createBaseGetAuthTokenResponse(): GetAuthTokenResponse {
  return { token: "" };
}

export const GetAuthTokenResponse = {
  encode(message: GetAuthTokenResponse, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.token !== "") {
      writer.uint32(10).string(message.token);
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): GetAuthTokenResponse {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseGetAuthTokenResponse();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.token = reader.string();
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): GetAuthTokenResponse {
    return { token: isSet(object.token) ? String(object.token) : "" };
  },

  toJSON(message: GetAuthTokenResponse): unknown {
    const obj: any = {};
    if (message.token !== "") {
      obj.token = message.token;
    }
    return obj;
  },

  create<I extends Exact<DeepPartial<GetAuthTokenResponse>, I>>(base?: I): GetAuthTokenResponse {
    return GetAuthTokenResponse.fromPartial(base ?? ({} as any));
  },
  fromPartial<I extends Exact<DeepPartial<GetAuthTokenResponse>, I>>(object: I): GetAuthTokenResponse {
    const message = createBaseGetAuthTokenResponse();
    message.token = object.token ?? "";
    return message;
  },
};

/** AuthGrpcService allows developers to generate JWT token for restricted access to data. */
export type AuthGrpcServiceService = typeof AuthGrpcServiceService;
export const AuthGrpcServiceService = {
  /** Creates auth token with custom access */
  getAuthToken: {
    path: "/dozer.auth.AuthGrpcService/getAuthToken",
    requestStream: false,
    responseStream: false,
    requestSerialize: (value: GetAuthTokenRequest) => Buffer.from(GetAuthTokenRequest.encode(value).finish()),
    requestDeserialize: (value: Buffer) => GetAuthTokenRequest.decode(value),
    responseSerialize: (value: GetAuthTokenResponse) => Buffer.from(GetAuthTokenResponse.encode(value).finish()),
    responseDeserialize: (value: Buffer) => GetAuthTokenResponse.decode(value),
  },
} as const;

export interface AuthGrpcServiceServer extends UntypedServiceImplementation {
  /** Creates auth token with custom access */
  getAuthToken: handleUnaryCall<GetAuthTokenRequest, GetAuthTokenResponse>;
}

export interface AuthGrpcServiceClient extends Client {
  /** Creates auth token with custom access */
  getAuthToken(
    request: GetAuthTokenRequest,
    callback: (error: ServiceError | null, response: GetAuthTokenResponse) => void,
  ): ClientUnaryCall;
  getAuthToken(
    request: GetAuthTokenRequest,
    metadata: Metadata,
    callback: (error: ServiceError | null, response: GetAuthTokenResponse) => void,
  ): ClientUnaryCall;
  getAuthToken(
    request: GetAuthTokenRequest,
    metadata: Metadata,
    options: Partial<CallOptions>,
    callback: (error: ServiceError | null, response: GetAuthTokenResponse) => void,
  ): ClientUnaryCall;
}

export const AuthGrpcServiceClient = makeGenericClientConstructor(
  AuthGrpcServiceService,
  "dozer.auth.AuthGrpcService",
) as unknown as {
  new (address: string, credentials: ChannelCredentials, options?: Partial<ClientOptions>): AuthGrpcServiceClient;
  service: typeof AuthGrpcServiceService;
};

type Builtin = Date | Function | Uint8Array | string | number | boolean | undefined;

type DeepPartial<T> = T extends Builtin ? T
  : T extends Array<infer U> ? Array<DeepPartial<U>> : T extends ReadonlyArray<infer U> ? ReadonlyArray<DeepPartial<U>>
  : T extends {} ? { [K in keyof T]?: DeepPartial<T[K]> }
  : Partial<T>;

type KeysOfUnion<T> = T extends T ? keyof T : never;
type Exact<P, I extends P> = P extends Builtin ? P
  : P & { [K in keyof P]: Exact<P[K], I[K]> } & { [K in Exclude<keyof I, KeysOfUnion<P>>]: never };

function isSet(value: any): boolean {
  return value !== null && value !== undefined;
}
