export const AUDIT_CONSTANTS = {
  OPERATION: {
    INSERT: "INSERT",
    DELETE: "DELETE",
    UPDATE: "UPDATE"
  }
};

export const STATUS_CONSTANTS = {
  FAIL: "FAIL",
  PASS_WARNING: "PASS",
  WARNING: "WARNING",
  PASS_SKIPPED: "PASS",
  SKIPPED: "SKIPPED",
  PASS: "PASS",
  UNEXECUTED: "UNEXECUTED"
};

export const STATUS_CONSTANTS_COLORS = {
  FAIL: "text-danger",
  PASS_WARNING: "text-success",
  WARNING: "text-warning",
  PASS_SKIPPED: "text-success",
  SKIPPED: "text-info",
  PASS: "text-success",
  UNEXECUTED: "text-secondary"
};

export const TOAST = {
  TIMER: 10000
};

export const REFRESH_TIMER = 15000;
