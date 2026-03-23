export type BackendHealth = {
  status: string;
  storage_mode: string;
  mqtt_bridge_connected: boolean;
  command_bridge_connected: boolean;
};

export type BackendRecord = {
  category: string;
  topic: string;
  msg_id: string;
  ts: string;
  source: string;
  type: string;
  mode: string;
  state: string;
  severity: string;
  payload: Record<string, unknown>;
  corr_id?: string | null;
  ack_required: boolean;
  received_at: string;
};

export type CommandReceipt = {
  published: boolean;
  topic: string;
  payload: string;
  qos: number;
  retain: boolean;
};

export type LiveFrame = Record<string, unknown>;
