# TypeScript Architecture

> **Agent load:** You open Project Structure, Principles, Error Handling, Configuration, and Project Prompt / Validation first. You open the rest only when your task needs them. Read project `AGENTS.md` if present. For reviews use `skills/review/audit/SKILL.md` (scope + mode). For naming/comments use `skills/engineering/craft/SKILL.md` (not detector scoring). Extend an existing repo instead of scaffolding a parallel tree. Discover verify commands from the project. Do not invent a toolchain. You work with what your team already uses.

You want a clean structure for your TypeScript applications. You set it up now. You thank yourself later when your team can still read your code.

---

## Project Structure

```
project/
├── src/
│   ├── lib/            # Business logic (domain types + rules)
│   ├── api/            # HTTP clients (I/O at the boundary)
│   ├── config.ts      # Typed, validated environment config
│   └── utils/          # Helpers
├── tests/
├── .env.example       # Documented env vars (committed; real .env is gitignored)
├── package.json
└── tsconfig.json
```

You organize `src/` by **domain**, not by type, once it grows. A `users/` folder holding its own logic, API calls, and types beats parallel `lib/` / `api/` trees you have to jump between. You keep it flat until that hurts. Why split what still fits together? You split when your team feels the pain.

---

## Principles

**Type everything**
You use the type system fully. An untyped boundary is a lie you tell your team. You do not ship lies.

**Single responsibility**
Each module does one thing well. If it does two, you split it. You keep each piece honest.

**Explicit dependencies**
You import what you need. No globals. Globals hide who depends on what. You make your debts visible.

**Strict mode**
You enable all strict checks. No shortcuts. Shortcuts bill you later. Would you rather pay now or pay more later?

---

## Business Logic

**lib/user.ts**
```typescript
export interface User {
  id: string;
  name: string;
  age: number;
}

export class ValidationError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'ValidationError';
  }
}

export function createUser(name: string, age: number): User {
  if (!name) {
    throw new ValidationError('Name required');
  }

  if (!isValidAge(age)) {
    throw new ValidationError('Invalid age');
  }

  return {
    id: crypto.randomUUID(),
    name,
    age,
  };
}

function isValidAge(age: number): boolean {
  return age >= 0 && age <= 150;
}
```

> `crypto.randomUUID()` is collision-free and it runs in Node 19+, Bun, Deno, and browsers. Never mint ids with `Date.now()`. Two calls in the same millisecond collide. In a real app your database (or `ulid`/`uuid`) usually owns id generation. You let the right owner make the id.

---

## API Layer

Your base URL comes from your typed config (see [Configuration](#configuration)). You never hard-code a host. Your errors carry the operation and status so a 3 a.m. log tells you what broke (`../standards/Principles.md` §5.3). Will you remember the context six months from now? Your log should. You write it for your tired self.

**api/users.ts**
```typescript
import { User } from '../lib/user';
import { config } from '../config';

export class ApiError extends Error {
  constructor(message: string, readonly status: number) {
    super(message);
    this.name = 'ApiError';
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${config.apiUrl}${path}`, init);
  if (!response.ok) {
    throw new ApiError(`${init?.method ?? 'GET'} ${path} failed`, response.status);
  }
  return response.json() as Promise<T>;
}

export function fetchUsers(): Promise<User[]> {
  return request<User[]>('/users');
}

export function saveUser(user: User): Promise<User> {
  return request<User>('/users', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(user),
  });
}

export async function deleteUser(id: string): Promise<void> {
  await request<void>(`/users/${id}`, { method: 'DELETE' });
}
```

One `request` helper wraps `fetch` so the URL, error shape, and JSON parsing live in one place. When you add auth headers or a retry later, you edit a single function, not three. That is the whole point. You fix it once. Your team thanks you.

---

## Error Handling

**Try-catch for async operations**

You branch on your own error types. Your typed `ApiError` and `ValidationError` carry enough for you to react differently. You translate them into a user-facing message at the boundary (see `skills/engineering/errors/SKILL.md` for the what/why/action rules). You never show your insides to your user.

```typescript
import { ApiError } from '../api/users';
import { ValidationError } from '../lib/user';

async function loadData() {
  try {
    const data = await fetchUsers();
    processData(data);
  } catch (err) {
    if (err instanceof ValidationError) {
      showError('Please check the form and try again.');
    } else if (err instanceof ApiError && err.status === 404) {
      showError('We couldn’t find those users.');
    } else {
      showError('Something went wrong loading your data. Try again in a moment.');
    }
  }
}
```

---

## Type Safety

**Use strict types**

```typescript
// Bad - any
function process(data: any) {
  return data.value;
}

// Good - specific type
interface Data {
  value: string;
}

function process(data: Data) {
  return data.value;
}
```

**Union types for variants**

```typescript
type Status = 'idle' | 'loading' | 'success' | 'error';

interface State {
  status: Status;
  data: User[] | null;
  error: string | null;
}
```

**Discriminated unions**

```typescript
type Result =
  | { success: true; data: User[] }
  | { success: false; error: string };

function handle(result: Result) {
  if (result.success) {
    console.log(result.data);  // TypeScript knows data exists
  } else {
    console.error(result.error);  // TypeScript knows error exists
  }
}
```

---

## Naming

These conventions match the wider ecosystem and `../standards/Principles.md` §1. You follow them so your team reads your code without friction. You remove one small tax your readers would pay.

```typescript
// Types & interfaces, PascalCase nouns
interface User {}
type Status = 'idle' | 'loading' | 'ready';

// Functions, camelCase verbs
function saveUser() {}
function parseConfig() {}

// Booleans, read like questions
const isActive = true;
const hasPermission = false;

// Constants, SCREAMING_SNAKE_CASE for true constants
const MAX_RETRIES = 3;

// Files, kebab-case, matching the concept
// user-service.ts, api-client.ts
```

- **No `I` prefix on interfaces** (`User`, not `IUser`). Your ecosystem dropped it. You drop it too.
- **No Hungarian notation** (`strName`, `bActive`). Your type system already knows. You trust it.
- **Domain words over generic ones**, `order`, not `data`. `notify`, not `handler`.
  See `skills/engineering/craft/SKILL.md` for naming and comment quality. Name it for what it means to your team. Your names teach your readers.

---

## Testing

**Unit tests**

```typescript
import { createUser, ValidationError } from './lib/user';

test('creates user with valid data', () => {
  const user = createUser('Alice', 30);
  
  expect(user.name).toBe('Alice');
  expect(user.age).toBe(30);
});

test('throws on empty name', () => {
  expect(() => createUser('', 30)).toThrow(ValidationError);
});

test('throws on invalid age', () => {
  expect(() => createUser('Bob', -5)).toThrow(ValidationError);
});
```

---

## Configuration

**Environment config, parse once, at the boundary**

Read every env var in one place, validate it, and export a typed object. The rest of your app imports `config` and trusts it. You put no `process.env.FOO` scattered through your codebase. You leave no `string | undefined` to guard at every use (`../standards/Principles.md` §15.1). You do the hard work once at the edge.

**src/config.ts**
```typescript
function required(name: string): string {
  const value = process.env[name];
  if (!value) {
    throw new Error(`Missing required env var: ${name}`);
  }
  return value;
}

export const config = {
  apiUrl: required('API_URL'),
  port: Number(process.env.PORT ?? 3000),
  debug: process.env.DEBUG === 'true',
} as const;
```

**.env.example** (commit this. The real `.env` is gitignored)
```
API_URL=http://localhost:3000
PORT=3000
DEBUG=false
```

You fail fast on startup if a required var is missing. A clear boot error beats a `fetch(undefined)` deep in your request handler. Would you rather find out at boot or from your users? You want the machine to tell you early.

**tsconfig.json**
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "lib": ["ES2020", "DOM"],
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true
  },
  "include": ["src"]
}
```

---

## Summary

You type everything with TypeScript. You keep your modules small and focused. You keep your business logic separate from presentation. You use strict mode and you allow no shortcuts. You handle your errors explicitly. That is your discipline. Your team can see it in your code.

---

## Project Prompt

You write TypeScript against the structure and rules above. Where they disagree with your defaults, this file wins. Listen. Your defaults do not matter here. This contract does.

You read `../standards/Principles.md` alongside this file before starting. You ground yourself first. Then you build.

**Type Safety**
- You type everything, no `any`. You say what you mean.
- You use interfaces for contracts. Your team codes against promises, not guesses.
- You keep strict mode enabled. You let the compiler catch you early.
- You use discriminated unions for state. You make impossible states unrepresentable.

**Error Handling**
- You use custom error classes for domain errors (carry context: operation, status, ids). You give your caller what they need to act.
- You use try-catch for async operations. You face failure where it happens.
- You never swallow errors silently. Hiding a failure is lying to your team.

**Configuration**
- You parse and validate all env vars once in `config.ts`, exported typed. You do it once at the edge.
- You fail fast on a missing required var. You allow no `process.env` reads elsewhere. One source keeps you sane.
- You commit `.env.example`, your real `.env` stays gitignored. You show the shape. You hide the secrets.

**Testing**
- You write unit tests for all business logic. You prove your rules hold.
- You mock external dependencies. You test your code, not the network.
- You test all error paths. Your failures get the same care as your happy path.

### Setup

```bash
npm init -y
npm install typescript
npm install -D @types/node      # process, crypto, etc.
npx tsc --init
```

### Deliverables

1. Complete project following architecture structure above. You show the whole shape working.
2. Type-safe modules with interfaces. Your contracts are plain to read.
3. Business logic separated from I/O. Your rules do not know about the wire.
4. Typed, validated `config.ts` + `.env.example`. Your settings come from one trusted place.
5. Custom error classes that carry operation, status, and ids. Your failures explain themselves.
6. README with setup instructions. Your teammate can boot it without asking you.
7. Basic test suite. You prove your code works. That is your craft.

### Validation Checklist

- [ ] Verify commands from project AGENTS.md / README run (or honest manual checks listed). You do not claim a green build you never ran.
- [ ] No secrets committed. Env examples use placeholders only. You keep real keys out of history.
- [ ] Your functions are small and single-purpose. You extract when a second concern appears (see Principles / skills/engineering/craft/SKILL.md). One job keeps you honest.
- [ ] No `any` types. You say what you take and what you return.
- [ ] You type all function signatures. You leave nothing vague at the edge.
- [ ] Custom error classes for domain errors. Your errors teach your caller.
- [ ] No hard-coded hosts/URLs, all config via `config.ts`. Your code runs anywhere your config points it.
- [ ] You generate ids with `crypto.randomUUID()` / DB, never `Date.now()`. You do not risk a collision.
- [ ] Your names match domain and local convention (skills/engineering/craft/SKILL.md). Your team hears its own language.
- [ ] TypeScript compiles with no errors. You ship a clean build.

### Pre-Delivery

```bash
npm run build
npm run type-check
npm test
```
