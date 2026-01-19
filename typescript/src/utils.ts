export function isNullish(val: unknown): boolean {
  return val === null || val === undefined;
}

export function shouldStrConcat(left: unknown, right: unknown): boolean {
  if (typeof left !== 'string' && typeof right !== 'string') {
    return false;
  }

  // We know at least one of them is a string here, let's check the other one
  const valOther = typeof left === 'string' ? right : left;

  if (!isPrimitive(valOther)) {
    return false;
  }

  return true;
}

export function isPrimitive(value: unknown): boolean {
  const type = typeof value;
  return (
    type === 'boolean' ||
    type === 'string' ||
    type === 'number' ||
    type === 'bigint' ||
    value === null ||
    value === undefined
  );
}

export function asString(val: unknown): string {
  if (typeof val === 'boolean') {
    return val ? 'true' : 'false';
  }
  if (isNullish(val)) {
    return '';
  }

  return String(val);
}

export function isNumericOrNull(val: unknown): boolean {
  return isNullish(val) || typeof val === 'number';
}

export function asNum(val: unknown): number {
  if (isNullish(val)) {
    return 0;
  }
  return val as number;
}
