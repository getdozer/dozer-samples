/* eslint-disable */
import Long from "long";
import _m0 from "protobufjs/minimal";
import { Value as Value1 } from "./google/protobuf/struct";
import { Timestamp } from "./google/protobuf/timestamp";

/** Event types that user can subscribe. */
export enum EventType {
  /** ALL - All events. */
  ALL = 0,
  /** INSERT_ONLY - Only INSERT events. */
  INSERT_ONLY = 1,
  /** UPDATE_ONLY - Only UPDATE events. */
  UPDATE_ONLY = 2,
  /** DELETE_ONLY - Only DELETE events. */
  DELETE_ONLY = 3,
  UNRECOGNIZED = -1,
}

export function eventTypeFromJSON(object: any): EventType {
  switch (object) {
    case 0:
    case "ALL":
      return EventType.ALL;
    case 1:
    case "INSERT_ONLY":
      return EventType.INSERT_ONLY;
    case 2:
    case "UPDATE_ONLY":
      return EventType.UPDATE_ONLY;
    case 3:
    case "DELETE_ONLY":
      return EventType.DELETE_ONLY;
    case -1:
    case "UNRECOGNIZED":
    default:
      return EventType.UNRECOGNIZED;
  }
}

export function eventTypeToJSON(object: EventType): string {
  switch (object) {
    case EventType.ALL:
      return "ALL";
    case EventType.INSERT_ONLY:
      return "INSERT_ONLY";
    case EventType.UPDATE_ONLY:
      return "UPDATE_ONLY";
    case EventType.DELETE_ONLY:
      return "DELETE_ONLY";
    case EventType.UNRECOGNIZED:
    default:
      return "UNRECOGNIZED";
  }
}

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

/** Supported data types in Dozer. */
export enum Type {
  /** UInt - Unsigned 64 bit integer. */
  UInt = 0,
  /** U128 - Unsigned 128 bit integer. */
  U128 = 1,
  /** Int - Signed 64 bit integer. */
  Int = 2,
  /** I128 - Signed 128 bit integer. */
  I128 = 3,
  /** Float - 64 bit floating point number. */
  Float = 4,
  /** Boolean - Boolean. */
  Boolean = 5,
  /** String - UTF-8 string. */
  String = 6,
  /** Text - UTF-8 string. */
  Text = 7,
  /** Binary - Binary data. */
  Binary = 8,
  /** Decimal - Decimal number. */
  Decimal = 9,
  /** Timestamp - ISO 8601 combined date and time with time zone. */
  Timestamp = 10,
  /** Date - ISO 8601 calendar date without timezone. */
  Date = 11,
  /** Json - JSON data. */
  Json = 12,
  /** Point - Geo Point type. */
  Point = 13,
  /** Duration - Duration type. */
  Duration = 14,
  UNRECOGNIZED = -1,
}

export function typeFromJSON(object: any): Type {
  switch (object) {
    case 0:
    case "UInt":
      return Type.UInt;
    case 1:
    case "U128":
      return Type.U128;
    case 2:
    case "Int":
      return Type.Int;
    case 3:
    case "I128":
      return Type.I128;
    case 4:
    case "Float":
      return Type.Float;
    case 5:
    case "Boolean":
      return Type.Boolean;
    case 6:
    case "String":
      return Type.String;
    case 7:
    case "Text":
      return Type.Text;
    case 8:
    case "Binary":
      return Type.Binary;
    case 9:
    case "Decimal":
      return Type.Decimal;
    case 10:
    case "Timestamp":
      return Type.Timestamp;
    case 11:
    case "Date":
      return Type.Date;
    case 12:
    case "Json":
      return Type.Json;
    case 13:
    case "Point":
      return Type.Point;
    case 14:
    case "Duration":
      return Type.Duration;
    case -1:
    case "UNRECOGNIZED":
    default:
      return Type.UNRECOGNIZED;
  }
}

export function typeToJSON(object: Type): string {
  switch (object) {
    case Type.UInt:
      return "UInt";
    case Type.U128:
      return "U128";
    case Type.Int:
      return "Int";
    case Type.I128:
      return "I128";
    case Type.Float:
      return "Float";
    case Type.Boolean:
      return "Boolean";
    case Type.String:
      return "String";
    case Type.Text:
      return "Text";
    case Type.Binary:
      return "Binary";
    case Type.Decimal:
      return "Decimal";
    case Type.Timestamp:
      return "Timestamp";
    case Type.Date:
      return "Date";
    case Type.Json:
      return "Json";
    case Type.Point:
      return "Point";
    case Type.Duration:
      return "Duration";
    case Type.UNRECOGNIZED:
    default:
      return "UNRECOGNIZED";
  }
}

/** Event filter. */
export interface EventFilter {
  /** The event type to subscribe to. */
  type: EventType;
  /** JSON filter string. */
  filter?: string | undefined;
}

/** A Dozer event. */
export interface Operation {
  /** The operation type. */
  typ: OperationType;
  /** Old record data, only applicable for UPDATE type. */
  old?:
    | Record
    | undefined;
  /** New record data. */
  new?:
    | Record
    | undefined;
  /** New record id, only applicable for INSERT type. */
  newId?:
    | number
    | undefined;
  /** Name of the endpoint that this event is from. */
  endpointName: string;
}

/** A record, can be thought of a row in the database table. */
export interface Record {
  /** The list of field values. */
  values: Value[];
  /** Records with same primary key will have increasing version. */
  version: number;
}

/** A record with its id in cache. */
export interface RecordWithId {
  /** The record id. */
  id: number;
  /** The record data. */
  record?: Record | undefined;
}

export interface SchemaEvent {
  endpoint: string;
  version: number;
  primaryIndex: number[];
  fields: FieldDefinition[];
}

/** `FieldDefinition` defines a field in a schema. */
export interface FieldDefinition {
  /** The field type. */
  typ: Type;
  /** The field name. */
  name: string;
  /** Whether the field is nullable. */
  nullable: boolean;
}

export interface PointType {
  x: number;
  y: number;
}

export interface DurationType {
  /** up to u128 */
  value: string;
  /** nanoseconds by default */
  timeUnit: string;
}

/** rust-decimal as a message */
export interface RustDecimal {
  /**
   * the lo, mid, hi, and flags fields contain the representation of the Decimal
   * value as a 96-bit integer
   */
  scale: number;
  lo: number;
  mid: number;
  hi: number;
  negative: boolean;
}

/** A field value. */
export interface Value {
  /** Unsigned 64 bit integer. */
  uintValue?:
    | number
    | undefined;
  /** Unsigned 128 bit integer. */
  uint128Value?:
    | string
    | undefined;
  /** Signed 64 bit integer. */
  intValue?:
    | number
    | undefined;
  /** Signed 128 bit integer. */
  int128Value?:
    | string
    | undefined;
  /** 64 bit floating point number. */
  floatValue?:
    | number
    | undefined;
  /** Boolean. */
  boolValue?:
    | boolean
    | undefined;
  /** UTF-8 string. */
  stringValue?:
    | string
    | undefined;
  /** Binary data. */
  bytesValue?:
    | Buffer
    | undefined;
  /** Decimal value. */
  decimalValue?:
    | RustDecimal
    | undefined;
  /** DateTime & Timestamp. */
  timestampValue?:
    | Date
    | undefined;
  /** ISO 8601 calendar date without timezone. */
  dateValue?:
    | string
    | undefined;
  /** Point type. */
  pointValue?:
    | PointType
    | undefined;
  /** Duration type. */
  durationValue?:
    | DurationType
    | undefined;
  /** JSON type. */
  jsonValue?: any | undefined;
}

function createBaseEventFilter(): EventFilter {
  return { type: 0, filter: undefined };
}

export const EventFilter = {
  encode(message: EventFilter, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.type !== 0) {
      writer.uint32(8).int32(message.type);
    }
    if (message.filter !== undefined) {
      writer.uint32(26).string(message.filter);
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): EventFilter {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseEventFilter();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 8) {
            break;
          }

          message.type = reader.int32() as any;
          continue;
        case 3:
          if (tag !== 26) {
            break;
          }

          message.filter = reader.string();
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): EventFilter {
    return {
      type: isSet(object.type) ? eventTypeFromJSON(object.type) : 0,
      filter: isSet(object.filter) ? String(object.filter) : undefined,
    };
  },

  toJSON(message: EventFilter): unknown {
    const obj: any = {};
    if (message.type !== 0) {
      obj.type = eventTypeToJSON(message.type);
    }
    if (message.filter !== undefined) {
      obj.filter = message.filter;
    }
    return obj;
  },

  create<I extends Exact<DeepPartial<EventFilter>, I>>(base?: I): EventFilter {
    return EventFilter.fromPartial(base ?? ({} as any));
  },
  fromPartial<I extends Exact<DeepPartial<EventFilter>, I>>(object: I): EventFilter {
    const message = createBaseEventFilter();
    message.type = object.type ?? 0;
    message.filter = object.filter ?? undefined;
    return message;
  },
};

function createBaseOperation(): Operation {
  return { typ: 0, old: undefined, new: undefined, newId: undefined, endpointName: "" };
}

export const Operation = {
  encode(message: Operation, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.typ !== 0) {
      writer.uint32(8).int32(message.typ);
    }
    if (message.old !== undefined) {
      Record.encode(message.old, writer.uint32(18).fork()).ldelim();
    }
    if (message.new !== undefined) {
      Record.encode(message.new, writer.uint32(26).fork()).ldelim();
    }
    if (message.newId !== undefined) {
      writer.uint32(32).uint64(message.newId);
    }
    if (message.endpointName !== "") {
      writer.uint32(42).string(message.endpointName);
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): Operation {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseOperation();
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
          if (tag !== 18) {
            break;
          }

          message.old = Record.decode(reader, reader.uint32());
          continue;
        case 3:
          if (tag !== 26) {
            break;
          }

          message.new = Record.decode(reader, reader.uint32());
          continue;
        case 4:
          if (tag !== 32) {
            break;
          }

          message.newId = longToNumber(reader.uint64() as Long);
          continue;
        case 5:
          if (tag !== 42) {
            break;
          }

          message.endpointName = reader.string();
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): Operation {
    return {
      typ: isSet(object.typ) ? operationTypeFromJSON(object.typ) : 0,
      old: isSet(object.old) ? Record.fromJSON(object.old) : undefined,
      new: isSet(object.new) ? Record.fromJSON(object.new) : undefined,
      newId: isSet(object.newId) ? Number(object.newId) : undefined,
      endpointName: isSet(object.endpointName) ? String(object.endpointName) : "",
    };
  },

  toJSON(message: Operation): unknown {
    const obj: any = {};
    if (message.typ !== 0) {
      obj.typ = operationTypeToJSON(message.typ);
    }
    if (message.old !== undefined) {
      obj.old = Record.toJSON(message.old);
    }
    if (message.new !== undefined) {
      obj.new = Record.toJSON(message.new);
    }
    if (message.newId !== undefined) {
      obj.newId = Math.round(message.newId);
    }
    if (message.endpointName !== "") {
      obj.endpointName = message.endpointName;
    }
    return obj;
  },

  create<I extends Exact<DeepPartial<Operation>, I>>(base?: I): Operation {
    return Operation.fromPartial(base ?? ({} as any));
  },
  fromPartial<I extends Exact<DeepPartial<Operation>, I>>(object: I): Operation {
    const message = createBaseOperation();
    message.typ = object.typ ?? 0;
    message.old = (object.old !== undefined && object.old !== null) ? Record.fromPartial(object.old) : undefined;
    message.new = (object.new !== undefined && object.new !== null) ? Record.fromPartial(object.new) : undefined;
    message.newId = object.newId ?? undefined;
    message.endpointName = object.endpointName ?? "";
    return message;
  },
};

function createBaseRecord(): Record {
  return { values: [], version: 0 };
}

export const Record = {
  encode(message: Record, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    for (const v of message.values) {
      Value.encode(v!, writer.uint32(10).fork()).ldelim();
    }
    if (message.version !== 0) {
      writer.uint32(16).uint32(message.version);
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): Record {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseRecord();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.values.push(Value.decode(reader, reader.uint32()));
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

  fromJSON(object: any): Record {
    return {
      values: Array.isArray(object?.values) ? object.values.map((e: any) => Value.fromJSON(e)) : [],
      version: isSet(object.version) ? Number(object.version) : 0,
    };
  },

  toJSON(message: Record): unknown {
    const obj: any = {};
    if (message.values?.length) {
      obj.values = message.values.map((e) => Value.toJSON(e));
    }
    if (message.version !== 0) {
      obj.version = Math.round(message.version);
    }
    return obj;
  },

  create<I extends Exact<DeepPartial<Record>, I>>(base?: I): Record {
    return Record.fromPartial(base ?? ({} as any));
  },
  fromPartial<I extends Exact<DeepPartial<Record>, I>>(object: I): Record {
    const message = createBaseRecord();
    message.values = object.values?.map((e) => Value.fromPartial(e)) || [];
    message.version = object.version ?? 0;
    return message;
  },
};

function createBaseRecordWithId(): RecordWithId {
  return { id: 0, record: undefined };
}

export const RecordWithId = {
  encode(message: RecordWithId, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.id !== 0) {
      writer.uint32(8).uint64(message.id);
    }
    if (message.record !== undefined) {
      Record.encode(message.record, writer.uint32(18).fork()).ldelim();
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): RecordWithId {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseRecordWithId();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 8) {
            break;
          }

          message.id = longToNumber(reader.uint64() as Long);
          continue;
        case 2:
          if (tag !== 18) {
            break;
          }

          message.record = Record.decode(reader, reader.uint32());
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): RecordWithId {
    return {
      id: isSet(object.id) ? Number(object.id) : 0,
      record: isSet(object.record) ? Record.fromJSON(object.record) : undefined,
    };
  },

  toJSON(message: RecordWithId): unknown {
    const obj: any = {};
    if (message.id !== 0) {
      obj.id = Math.round(message.id);
    }
    if (message.record !== undefined) {
      obj.record = Record.toJSON(message.record);
    }
    return obj;
  },

  create<I extends Exact<DeepPartial<RecordWithId>, I>>(base?: I): RecordWithId {
    return RecordWithId.fromPartial(base ?? ({} as any));
  },
  fromPartial<I extends Exact<DeepPartial<RecordWithId>, I>>(object: I): RecordWithId {
    const message = createBaseRecordWithId();
    message.id = object.id ?? 0;
    message.record = (object.record !== undefined && object.record !== null)
      ? Record.fromPartial(object.record)
      : undefined;
    return message;
  },
};

function createBaseSchemaEvent(): SchemaEvent {
  return { endpoint: "", version: 0, primaryIndex: [], fields: [] };
}

export const SchemaEvent = {
  encode(message: SchemaEvent, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.endpoint !== "") {
      writer.uint32(10).string(message.endpoint);
    }
    if (message.version !== 0) {
      writer.uint32(16).uint64(message.version);
    }
    writer.uint32(26).fork();
    for (const v of message.primaryIndex) {
      writer.int32(v);
    }
    writer.ldelim();
    for (const v of message.fields) {
      FieldDefinition.encode(v!, writer.uint32(34).fork()).ldelim();
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): SchemaEvent {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseSchemaEvent();
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
          if (tag !== 16) {
            break;
          }

          message.version = longToNumber(reader.uint64() as Long);
          continue;
        case 3:
          if (tag === 24) {
            message.primaryIndex.push(reader.int32());

            continue;
          }

          if (tag === 26) {
            const end2 = reader.uint32() + reader.pos;
            while (reader.pos < end2) {
              message.primaryIndex.push(reader.int32());
            }

            continue;
          }

          break;
        case 4:
          if (tag !== 34) {
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

  fromJSON(object: any): SchemaEvent {
    return {
      endpoint: isSet(object.endpoint) ? String(object.endpoint) : "",
      version: isSet(object.version) ? Number(object.version) : 0,
      primaryIndex: Array.isArray(object?.primaryIndex) ? object.primaryIndex.map((e: any) => Number(e)) : [],
      fields: Array.isArray(object?.fields) ? object.fields.map((e: any) => FieldDefinition.fromJSON(e)) : [],
    };
  },

  toJSON(message: SchemaEvent): unknown {
    const obj: any = {};
    if (message.endpoint !== "") {
      obj.endpoint = message.endpoint;
    }
    if (message.version !== 0) {
      obj.version = Math.round(message.version);
    }
    if (message.primaryIndex?.length) {
      obj.primaryIndex = message.primaryIndex.map((e) => Math.round(e));
    }
    if (message.fields?.length) {
      obj.fields = message.fields.map((e) => FieldDefinition.toJSON(e));
    }
    return obj;
  },

  create<I extends Exact<DeepPartial<SchemaEvent>, I>>(base?: I): SchemaEvent {
    return SchemaEvent.fromPartial(base ?? ({} as any));
  },
  fromPartial<I extends Exact<DeepPartial<SchemaEvent>, I>>(object: I): SchemaEvent {
    const message = createBaseSchemaEvent();
    message.endpoint = object.endpoint ?? "";
    message.version = object.version ?? 0;
    message.primaryIndex = object.primaryIndex?.map((e) => e) || [];
    message.fields = object.fields?.map((e) => FieldDefinition.fromPartial(e)) || [];
    return message;
  },
};

function createBaseFieldDefinition(): FieldDefinition {
  return { typ: 0, name: "", nullable: false };
}

export const FieldDefinition = {
  encode(message: FieldDefinition, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.typ !== 0) {
      writer.uint32(8).int32(message.typ);
    }
    if (message.name !== "") {
      writer.uint32(18).string(message.name);
    }
    if (message.nullable === true) {
      writer.uint32(24).bool(message.nullable);
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): FieldDefinition {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseFieldDefinition();
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
          if (tag !== 18) {
            break;
          }

          message.name = reader.string();
          continue;
        case 3:
          if (tag !== 24) {
            break;
          }

          message.nullable = reader.bool();
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): FieldDefinition {
    return {
      typ: isSet(object.typ) ? typeFromJSON(object.typ) : 0,
      name: isSet(object.name) ? String(object.name) : "",
      nullable: isSet(object.nullable) ? Boolean(object.nullable) : false,
    };
  },

  toJSON(message: FieldDefinition): unknown {
    const obj: any = {};
    if (message.typ !== 0) {
      obj.typ = typeToJSON(message.typ);
    }
    if (message.name !== "") {
      obj.name = message.name;
    }
    if (message.nullable === true) {
      obj.nullable = message.nullable;
    }
    return obj;
  },

  create<I extends Exact<DeepPartial<FieldDefinition>, I>>(base?: I): FieldDefinition {
    return FieldDefinition.fromPartial(base ?? ({} as any));
  },
  fromPartial<I extends Exact<DeepPartial<FieldDefinition>, I>>(object: I): FieldDefinition {
    const message = createBaseFieldDefinition();
    message.typ = object.typ ?? 0;
    message.name = object.name ?? "";
    message.nullable = object.nullable ?? false;
    return message;
  },
};

function createBasePointType(): PointType {
  return { x: 0, y: 0 };
}

export const PointType = {
  encode(message: PointType, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.x !== 0) {
      writer.uint32(9).double(message.x);
    }
    if (message.y !== 0) {
      writer.uint32(17).double(message.y);
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): PointType {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBasePointType();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 9) {
            break;
          }

          message.x = reader.double();
          continue;
        case 2:
          if (tag !== 17) {
            break;
          }

          message.y = reader.double();
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): PointType {
    return { x: isSet(object.x) ? Number(object.x) : 0, y: isSet(object.y) ? Number(object.y) : 0 };
  },

  toJSON(message: PointType): unknown {
    const obj: any = {};
    if (message.x !== 0) {
      obj.x = message.x;
    }
    if (message.y !== 0) {
      obj.y = message.y;
    }
    return obj;
  },

  create<I extends Exact<DeepPartial<PointType>, I>>(base?: I): PointType {
    return PointType.fromPartial(base ?? ({} as any));
  },
  fromPartial<I extends Exact<DeepPartial<PointType>, I>>(object: I): PointType {
    const message = createBasePointType();
    message.x = object.x ?? 0;
    message.y = object.y ?? 0;
    return message;
  },
};

function createBaseDurationType(): DurationType {
  return { value: "", timeUnit: "" };
}

export const DurationType = {
  encode(message: DurationType, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.value !== "") {
      writer.uint32(10).string(message.value);
    }
    if (message.timeUnit !== "") {
      writer.uint32(18).string(message.timeUnit);
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): DurationType {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseDurationType();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 10) {
            break;
          }

          message.value = reader.string();
          continue;
        case 2:
          if (tag !== 18) {
            break;
          }

          message.timeUnit = reader.string();
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): DurationType {
    return {
      value: isSet(object.value) ? String(object.value) : "",
      timeUnit: isSet(object.timeUnit) ? String(object.timeUnit) : "",
    };
  },

  toJSON(message: DurationType): unknown {
    const obj: any = {};
    if (message.value !== "") {
      obj.value = message.value;
    }
    if (message.timeUnit !== "") {
      obj.timeUnit = message.timeUnit;
    }
    return obj;
  },

  create<I extends Exact<DeepPartial<DurationType>, I>>(base?: I): DurationType {
    return DurationType.fromPartial(base ?? ({} as any));
  },
  fromPartial<I extends Exact<DeepPartial<DurationType>, I>>(object: I): DurationType {
    const message = createBaseDurationType();
    message.value = object.value ?? "";
    message.timeUnit = object.timeUnit ?? "";
    return message;
  },
};

function createBaseRustDecimal(): RustDecimal {
  return { scale: 0, lo: 0, mid: 0, hi: 0, negative: false };
}

export const RustDecimal = {
  encode(message: RustDecimal, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.scale !== 0) {
      writer.uint32(8).uint32(message.scale);
    }
    if (message.lo !== 0) {
      writer.uint32(16).uint32(message.lo);
    }
    if (message.mid !== 0) {
      writer.uint32(24).uint32(message.mid);
    }
    if (message.hi !== 0) {
      writer.uint32(32).uint32(message.hi);
    }
    if (message.negative === true) {
      writer.uint32(40).bool(message.negative);
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): RustDecimal {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseRustDecimal();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 8) {
            break;
          }

          message.scale = reader.uint32();
          continue;
        case 2:
          if (tag !== 16) {
            break;
          }

          message.lo = reader.uint32();
          continue;
        case 3:
          if (tag !== 24) {
            break;
          }

          message.mid = reader.uint32();
          continue;
        case 4:
          if (tag !== 32) {
            break;
          }

          message.hi = reader.uint32();
          continue;
        case 5:
          if (tag !== 40) {
            break;
          }

          message.negative = reader.bool();
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): RustDecimal {
    return {
      scale: isSet(object.scale) ? Number(object.scale) : 0,
      lo: isSet(object.lo) ? Number(object.lo) : 0,
      mid: isSet(object.mid) ? Number(object.mid) : 0,
      hi: isSet(object.hi) ? Number(object.hi) : 0,
      negative: isSet(object.negative) ? Boolean(object.negative) : false,
    };
  },

  toJSON(message: RustDecimal): unknown {
    const obj: any = {};
    if (message.scale !== 0) {
      obj.scale = Math.round(message.scale);
    }
    if (message.lo !== 0) {
      obj.lo = Math.round(message.lo);
    }
    if (message.mid !== 0) {
      obj.mid = Math.round(message.mid);
    }
    if (message.hi !== 0) {
      obj.hi = Math.round(message.hi);
    }
    if (message.negative === true) {
      obj.negative = message.negative;
    }
    return obj;
  },

  create<I extends Exact<DeepPartial<RustDecimal>, I>>(base?: I): RustDecimal {
    return RustDecimal.fromPartial(base ?? ({} as any));
  },
  fromPartial<I extends Exact<DeepPartial<RustDecimal>, I>>(object: I): RustDecimal {
    const message = createBaseRustDecimal();
    message.scale = object.scale ?? 0;
    message.lo = object.lo ?? 0;
    message.mid = object.mid ?? 0;
    message.hi = object.hi ?? 0;
    message.negative = object.negative ?? false;
    return message;
  },
};

function createBaseValue(): Value {
  return {
    uintValue: undefined,
    uint128Value: undefined,
    intValue: undefined,
    int128Value: undefined,
    floatValue: undefined,
    boolValue: undefined,
    stringValue: undefined,
    bytesValue: undefined,
    decimalValue: undefined,
    timestampValue: undefined,
    dateValue: undefined,
    pointValue: undefined,
    durationValue: undefined,
    jsonValue: undefined,
  };
}

export const Value = {
  encode(message: Value, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.uintValue !== undefined) {
      writer.uint32(8).uint64(message.uintValue);
    }
    if (message.uint128Value !== undefined) {
      writer.uint32(18).string(message.uint128Value);
    }
    if (message.intValue !== undefined) {
      writer.uint32(24).int64(message.intValue);
    }
    if (message.int128Value !== undefined) {
      writer.uint32(34).string(message.int128Value);
    }
    if (message.floatValue !== undefined) {
      writer.uint32(41).double(message.floatValue);
    }
    if (message.boolValue !== undefined) {
      writer.uint32(48).bool(message.boolValue);
    }
    if (message.stringValue !== undefined) {
      writer.uint32(58).string(message.stringValue);
    }
    if (message.bytesValue !== undefined) {
      writer.uint32(66).bytes(message.bytesValue);
    }
    if (message.decimalValue !== undefined) {
      RustDecimal.encode(message.decimalValue, writer.uint32(74).fork()).ldelim();
    }
    if (message.timestampValue !== undefined) {
      Timestamp.encode(toTimestamp(message.timestampValue), writer.uint32(82).fork()).ldelim();
    }
    if (message.dateValue !== undefined) {
      writer.uint32(90).string(message.dateValue);
    }
    if (message.pointValue !== undefined) {
      PointType.encode(message.pointValue, writer.uint32(98).fork()).ldelim();
    }
    if (message.durationValue !== undefined) {
      DurationType.encode(message.durationValue, writer.uint32(106).fork()).ldelim();
    }
    if (message.jsonValue !== undefined) {
      Value1.encode(Value1.wrap(message.jsonValue), writer.uint32(114).fork()).ldelim();
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): Value {
    const reader = input instanceof _m0.Reader ? input : _m0.Reader.create(input);
    let end = length === undefined ? reader.len : reader.pos + length;
    const message = createBaseValue();
    while (reader.pos < end) {
      const tag = reader.uint32();
      switch (tag >>> 3) {
        case 1:
          if (tag !== 8) {
            break;
          }

          message.uintValue = longToNumber(reader.uint64() as Long);
          continue;
        case 2:
          if (tag !== 18) {
            break;
          }

          message.uint128Value = reader.string();
          continue;
        case 3:
          if (tag !== 24) {
            break;
          }

          message.intValue = longToNumber(reader.int64() as Long);
          continue;
        case 4:
          if (tag !== 34) {
            break;
          }

          message.int128Value = reader.string();
          continue;
        case 5:
          if (tag !== 41) {
            break;
          }

          message.floatValue = reader.double();
          continue;
        case 6:
          if (tag !== 48) {
            break;
          }

          message.boolValue = reader.bool();
          continue;
        case 7:
          if (tag !== 58) {
            break;
          }

          message.stringValue = reader.string();
          continue;
        case 8:
          if (tag !== 66) {
            break;
          }

          message.bytesValue = reader.bytes() as Buffer;
          continue;
        case 9:
          if (tag !== 74) {
            break;
          }

          message.decimalValue = RustDecimal.decode(reader, reader.uint32());
          continue;
        case 10:
          if (tag !== 82) {
            break;
          }

          message.timestampValue = fromTimestamp(Timestamp.decode(reader, reader.uint32()));
          continue;
        case 11:
          if (tag !== 90) {
            break;
          }

          message.dateValue = reader.string();
          continue;
        case 12:
          if (tag !== 98) {
            break;
          }

          message.pointValue = PointType.decode(reader, reader.uint32());
          continue;
        case 13:
          if (tag !== 106) {
            break;
          }

          message.durationValue = DurationType.decode(reader, reader.uint32());
          continue;
        case 14:
          if (tag !== 114) {
            break;
          }

          message.jsonValue = Value1.unwrap(Value1.decode(reader, reader.uint32()));
          continue;
      }
      if ((tag & 7) === 4 || tag === 0) {
        break;
      }
      reader.skipType(tag & 7);
    }
    return message;
  },

  fromJSON(object: any): Value {
    return {
      uintValue: isSet(object.uintValue) ? Number(object.uintValue) : undefined,
      uint128Value: isSet(object.uint128Value) ? String(object.uint128Value) : undefined,
      intValue: isSet(object.intValue) ? Number(object.intValue) : undefined,
      int128Value: isSet(object.int128Value) ? String(object.int128Value) : undefined,
      floatValue: isSet(object.floatValue) ? Number(object.floatValue) : undefined,
      boolValue: isSet(object.boolValue) ? Boolean(object.boolValue) : undefined,
      stringValue: isSet(object.stringValue) ? String(object.stringValue) : undefined,
      bytesValue: isSet(object.bytesValue) ? Buffer.from(bytesFromBase64(object.bytesValue)) : undefined,
      decimalValue: isSet(object.decimalValue) ? RustDecimal.fromJSON(object.decimalValue) : undefined,
      timestampValue: isSet(object.timestampValue) ? fromJsonTimestamp(object.timestampValue) : undefined,
      dateValue: isSet(object.dateValue) ? String(object.dateValue) : undefined,
      pointValue: isSet(object.pointValue) ? PointType.fromJSON(object.pointValue) : undefined,
      durationValue: isSet(object.durationValue) ? DurationType.fromJSON(object.durationValue) : undefined,
      jsonValue: isSet(object?.jsonValue) ? object.jsonValue : undefined,
    };
  },

  toJSON(message: Value): unknown {
    const obj: any = {};
    if (message.uintValue !== undefined) {
      obj.uintValue = Math.round(message.uintValue);
    }
    if (message.uint128Value !== undefined) {
      obj.uint128Value = message.uint128Value;
    }
    if (message.intValue !== undefined) {
      obj.intValue = Math.round(message.intValue);
    }
    if (message.int128Value !== undefined) {
      obj.int128Value = message.int128Value;
    }
    if (message.floatValue !== undefined) {
      obj.floatValue = message.floatValue;
    }
    if (message.boolValue !== undefined) {
      obj.boolValue = message.boolValue;
    }
    if (message.stringValue !== undefined) {
      obj.stringValue = message.stringValue;
    }
    if (message.bytesValue !== undefined) {
      obj.bytesValue = base64FromBytes(message.bytesValue);
    }
    if (message.decimalValue !== undefined) {
      obj.decimalValue = RustDecimal.toJSON(message.decimalValue);
    }
    if (message.timestampValue !== undefined) {
      obj.timestampValue = message.timestampValue.toISOString();
    }
    if (message.dateValue !== undefined) {
      obj.dateValue = message.dateValue;
    }
    if (message.pointValue !== undefined) {
      obj.pointValue = PointType.toJSON(message.pointValue);
    }
    if (message.durationValue !== undefined) {
      obj.durationValue = DurationType.toJSON(message.durationValue);
    }
    if (message.jsonValue !== undefined) {
      obj.jsonValue = message.jsonValue;
    }
    return obj;
  },

  create<I extends Exact<DeepPartial<Value>, I>>(base?: I): Value {
    return Value.fromPartial(base ?? ({} as any));
  },
  fromPartial<I extends Exact<DeepPartial<Value>, I>>(object: I): Value {
    const message = createBaseValue();
    message.uintValue = object.uintValue ?? undefined;
    message.uint128Value = object.uint128Value ?? undefined;
    message.intValue = object.intValue ?? undefined;
    message.int128Value = object.int128Value ?? undefined;
    message.floatValue = object.floatValue ?? undefined;
    message.boolValue = object.boolValue ?? undefined;
    message.stringValue = object.stringValue ?? undefined;
    message.bytesValue = object.bytesValue ?? undefined;
    message.decimalValue = (object.decimalValue !== undefined && object.decimalValue !== null)
      ? RustDecimal.fromPartial(object.decimalValue)
      : undefined;
    message.timestampValue = object.timestampValue ?? undefined;
    message.dateValue = object.dateValue ?? undefined;
    message.pointValue = (object.pointValue !== undefined && object.pointValue !== null)
      ? PointType.fromPartial(object.pointValue)
      : undefined;
    message.durationValue = (object.durationValue !== undefined && object.durationValue !== null)
      ? DurationType.fromPartial(object.durationValue)
      : undefined;
    message.jsonValue = object.jsonValue ?? undefined;
    return message;
  },
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

function toTimestamp(date: Date): Timestamp {
  const seconds = date.getTime() / 1_000;
  const nanos = (date.getTime() % 1_000) * 1_000_000;
  return { seconds, nanos };
}

function fromTimestamp(t: Timestamp): Date {
  let millis = (t.seconds || 0) * 1_000;
  millis += (t.nanos || 0) / 1_000_000;
  return new Date(millis);
}

function fromJsonTimestamp(o: any): Date {
  if (o instanceof Date) {
    return o;
  } else if (typeof o === "string") {
    return new Date(o);
  } else {
    return fromTimestamp(Timestamp.fromJSON(o));
  }
}

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

function isSet(value: any): boolean {
  return value !== null && value !== undefined;
}
