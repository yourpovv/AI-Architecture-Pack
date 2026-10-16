# React / Tailwind Architecture

> **Agent load:** Open Project Structure, Principles, Error Handling, Configuration, and Project Prompt / Validation first. Open other sections only when the task needs them. Read the project's `AGENTS.md`. Coding standards come from `../standards/Clean-Code/`. Reviews: `skills/review/audit/SKILL.md`. Craft: `skills/engineering/craft/SKILL.md`. Prefer extending an existing repo over scaffolding a parallel tree.

Framework patterns for web applications built with React, TypeScript, and Tailwind CSS 4. The
Clean-Code lessons define the coding standard; this file covers what React and Tailwind change.

---

## Project Structure

```
project/
├── src/
│   ├── components/     # UI components
│   ├── hooks/          # React hooks
│   ├── context/        # Context providers
│   ├── lib/            # Business logic, framework-free
│   ├── api/            # HTTP clients, one module per external service
│   └── index.css       # Tailwind entry: @import "tailwindcss";
├── public/             # Static assets
├── tests/
├── package.json
├── tsconfig.json
└── vite.config.ts
```

There is no `utils/` folder. A helper belongs to the module whose knowledge it encodes
(Clean-Code 14).

---

## Principles

**TypeScript in strict mode**
`"strict": true` in `tsconfig.json`, no `any`, and every prop and state shape typed
(Clean-Code 25).

**Composition over inheritance**
Build complex UIs from small components.

**Single responsibility**
Each component does one thing and has one reason to change. Split when UI, data fetching, and
business rules share one file (Clean-Code `solid/01`).

**Props, not global state**
Pass data explicitly where you can, so a component's dependencies are visible at the call site.

**Context sparingly**
Use context only for truly app-wide state such as auth or theme. Most state is not global.

**Tailwind for styles**
Use utility classes rather than custom CSS. Repeated class groups become components.

**Business logic outside components**
Rules and calculations live in `lib/` as plain functions that can be tested without React.
Components and hooks call them (Clean-Code `classes/04`).

---

## Component Structure

### Simple Component

**Button.tsx**
```typescript
interface ButtonProps {
  label: string;
  onClick: () => void;
  disabled?: boolean;
}

export function Button({ label, onClick, disabled = false }: ButtonProps) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
    >
      {label}
    </button>
  );
}
```

### Component with State

**Counter.tsx**
```typescript
import { useState } from 'react';

export function Counter() {
  const [count, setCount] = useState(0);

  function increment() {
    setCount(previous => previous + 1);
  }

  function reset() {
    setCount(0);
  }

  return (
    <div className="p-4 border rounded">
      <p className="text-lg font-medium">Count: {count}</p>
      <div className="flex gap-2 mt-2">
        <button onClick={increment} className="px-3 py-1 bg-green-600 text-white rounded">
          Increment
        </button>
        <button onClick={reset} className="px-3 py-1 bg-gray-600 text-white rounded">
          Reset
        </button>
      </div>
    </div>
  );
}
```

### List Component

**UserList.tsx**
```typescript
interface User {
  id: number;
  name: string;
  email: string;
}

interface UserListProps {
  users: User[];
  onSelect: (user: User) => void;
}

export function UserList({ users, onSelect }: UserListProps) {
  if (users.length === 0) {
    return <p className="text-gray-500">No users yet.</p>;
  }

  return (
    <ul className="space-y-2">
      {users.map(user => (
        <UserItem key={user.id} user={user} onSelect={onSelect} />
      ))}
    </ul>
  );
}

interface UserItemProps {
  user: User;
  onSelect: (user: User) => void;
}

function UserItem({ user, onSelect }: UserItemProps) {
  return (
    <li>
      <button
        onClick={() => onSelect(user)}
        className="w-full text-left p-3 border rounded hover:bg-gray-50"
      >
        <p className="font-medium">{user.name}</p>
        <p className="text-sm text-gray-600">{user.email}</p>
      </button>
    </li>
  );
}
```

---

## Custom Hooks

Model async state as a discriminated union of the states the UI actually renders. This is UI
data, not an error channel, so it does not conflict with Clean-Code 03: the API client still
throws, and the hook is the boundary that catches.

**hooks/useUsers.ts**
```typescript
import { useCallback, useEffect, useState } from 'react';
import { User } from '../lib/user';
import { fetchUsers } from '../api/users';

type UsersState =
  | { status: 'loading' }
  | { status: 'ready'; users: User[] }
  | { status: 'failed' };

export function useUsers() {
  const [state, setState] = useState<UsersState>({ status: 'loading' });

  const reload = useCallback(async () => {
    setState({ status: 'loading' });
    try {
      setState({ status: 'ready', users: await fetchUsers() });
    } catch (error) {
      console.error('useUsers: fetchUsers failed', error);
      setState({ status: 'failed' });
    }
  }, []);

  useEffect(() => {
    reload();
  }, [reload]);

  return { state, reload };
}
```

**hooks/useForm.ts**
```typescript
import { useState } from 'react';

export function useForm<T>(initial: T) {
  const [values, setValues] = useState<T>(initial);

  function update<K extends keyof T>(field: K, value: T[K]) {
    setValues(previous => ({ ...previous, [field]: value }));
  }

  function reset() {
    setValues(initial);
  }

  return { values, update, reset };
}
```

---

## Error Handling

React code fails in two distinct ways, and each needs its own handling:

- **Render errors:** an **error boundary** catches them and shows fallback UI instead of
  unmounting the whole tree.
- **Async and event errors** (fetches, handlers): boundaries do not catch these. Catch them at
  the hook or handler, log the technical detail, and render a user-facing state. Message copy
  follows `skills/engineering/errors/SKILL.md` Part B: what happened, why, and what to do.
  Never render a raw exception message.

**Error boundary** (catches render-time errors):

```typescript
import { Component, ErrorInfo, ReactNode } from 'react';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
}

export class ErrorBoundary extends Component<Props, State> {
  state = { hasError: false };

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    console.error('Render error caught by ErrorBoundary:', error, info.componentStack);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="p-4 bg-red-50 border border-red-200 rounded" role="alert">
          <p className="font-medium text-red-800">This page couldn't be displayed.</p>
          <p className="text-red-700">Part of the page failed to load. Refresh to try again.</p>
        </div>
      );
    }

    return this.props.children;
  }
}
```

**Async errors** (render the hook's state):

```typescript
function Users() {
  const { state, reload } = useUsers();

  if (state.status === 'loading') {
    return <p className="text-gray-500">Loading users…</p>;
  }

  if (state.status === 'failed') {
    return (
      <div role="alert" className="text-red-800">
        <p>Your user list couldn't load because the server didn't respond.</p>
        <button onClick={reload} className="underline">Try again</button>
      </div>
    );
  }

  return <UserList users={state.users} onSelect={openUser} />;
}
```

---

## Tailwind CSS Patterns

**Component styles**

```typescript
// Bad: inline styles
<div style={{ padding: '16px', backgroundColor: '#fff' }}>

// Good: Tailwind utilities
<div className="p-4 bg-white">
```

**Variant classes**

A `variant` prop is data that selects a look, not a flag that selects a second algorithm, so it
does not break Clean-Code 02. Map variants through a lookup table rather than scattered
conditionals (Clean-Code 24).

```typescript
import clsx from 'clsx';

const VARIANT_CLASSES = {
  primary: 'bg-blue-600 text-white',
  secondary: 'bg-gray-200 text-gray-800',
} as const;

interface ActionButtonProps {
  label: string;
  variant: keyof typeof VARIANT_CLASSES;
  disabled?: boolean;
  onClick: () => void;
}

export function ActionButton({ label, variant, disabled = false, onClick }: ActionButtonProps) {
  return (
    <button
      className={clsx(
        'px-4 py-2 rounded',
        VARIANT_CLASSES[variant],
        disabled && 'opacity-50 cursor-not-allowed'
      )}
      disabled={disabled}
      onClick={onClick}
    >
      {label}
    </button>
  );
}
```

**Reusable class groups**

```typescript
// Bad: the same class group repeated
<div className="p-4 bg-white border rounded shadow">
<div className="p-4 bg-white border rounded shadow">

// Good: extract a component
function Card({ children }: { children: ReactNode }) {
  return <div className="p-4 bg-white border rounded shadow">{children}</div>;
}
```

**Responsive design**

```typescript
<div className="flex flex-col md:flex-row gap-4 p-4 md:p-6 lg:p-8">
  <div className="w-full md:w-1/2">Left</div>
  <div className="w-full md:w-1/2">Right</div>
</div>
```

---

## State Management

**Local state for simple cases**

```typescript
function TodoList() {
  const [todos, setTodos] = useState<Todo[]>([]);

  function addTodo(text: string) {
    setTodos(previous => [...previous, { id: crypto.randomUUID(), text }]);
  }

  function removeTodo(id: string) {
    setTodos(previous => previous.filter(todo => todo.id !== id));
  }

  return <div>{/* ... */}</div>;
}
```

**Context for shared state**

Model "signed out" as its own state rather than a `null` user (Clean-Code 13).

```typescript
import { createContext, useContext, useState, ReactNode } from 'react';

interface User {
  name: string;
  email: string;
}

type Session = { status: 'signedOut' } | { status: 'signedIn'; user: User };

interface AuthContextValue {
  session: Session;
  signIn: (user: User) => void;
  signOut: () => void;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [session, setSession] = useState<Session>({ status: 'signedOut' });

  function signIn(user: User) {
    setSession({ status: 'signedIn', user });
  }

  function signOut() {
    setSession({ status: 'signedOut' });
  }

  return (
    <AuthContext.Provider value={{ session, signIn, signOut }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}
```

---

## Testing

Name tests for the behavior they guard (Clean-Code `unit-tests/05`).

**Component tests**

```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from './Button';

test('shows its label', () => {
  render(<Button label="Save" onClick={() => {}} />);
  expect(screen.getByText('Save')).toBeInTheDocument();
});

test('calls onClick once per click', () => {
  const onClick = vi.fn();
  render(<Button label="Save" onClick={onClick} />);

  fireEvent.click(screen.getByText('Save'));

  expect(onClick).toHaveBeenCalledTimes(1);
});

test('ignores clicks while disabled', () => {
  const onClick = vi.fn();
  render(<Button label="Save" onClick={onClick} disabled />);

  fireEvent.click(screen.getByText('Save'));

  expect(onClick).not.toHaveBeenCalled();
});
```

**Hook tests**

```typescript
import { renderHook, act } from '@testing-library/react';
import { useForm } from './useForm';

test('updates one field without touching the others', () => {
  const { result } = renderHook(() => useForm({ name: '', email: 'a@b.c' }));

  act(() => {
    result.current.update('name', 'Ada');
  });

  expect(result.current.values).toEqual({ name: 'Ada', email: 'a@b.c' });
});
```

---

## Configuration

Tailwind CSS 4 is configured through its Vite plugin and a CSS import; there is no
`tailwind.config.js` by default. Theme customization goes in CSS with `@theme`.

**vite.config.ts**
```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  plugins: [react(), tailwindcss()],
});
```

**src/index.css**
```css
@import "tailwindcss";

@theme {
  --color-brand: #2563eb;
}
```

Environment values are read through `import.meta.env` in one config module and imported from
there. Commit a `.env.example` with placeholder values; never commit `.env`.

---

## Summary

- Small, focused components; business logic in `lib/`.
- Strict TypeScript with no `any`.
- Tailwind utilities instead of custom CSS.
- Reusable logic in custom hooks; async state as a discriminated union.
- Context only for app-wide state.
- Error boundaries for render errors, hook-level boundaries for async errors, and user-facing
  copy that says what, why, and what to do.
- Components and hooks covered by behavior-named tests.

---

## Project Prompt

Build a React and Tailwind frontend against the structure and rules above. This file decides
framework structure and idiom; coding standards come from `../standards/Clean-Code/`, which
wins on any conflict. Open the sections of `../standards/Principles.md` the task needs.

**Styling**
- Tailwind CSS 4 only; custom CSS only where utilities cannot express it
- Utility-first, mobile-first responsive design
- One consistent spacing scale

**Components**
- Composition over inheritance
- Props for data flow; context only for app-wide state
- Split a component when it mixes unrelated concerns
- Error boundaries for render failures

**Performance**
- Memoize expensive calculations when profiling shows a cost
- Lazy-load routes and heavy components
- Virtualize long lists
- Debounce high-frequency event handlers

### Setup

```bash
npm create vite@latest project-name -- --template react-ts
cd project-name
npm install
npm install tailwindcss @tailwindcss/vite
```

Then add the Tailwind plugin to `vite.config.ts` and `@import "tailwindcss";` to
`src/index.css` as shown in Configuration.

### Deliverables

1. A complete project following the structure above
2. Type-safe React components
3. Custom hooks for reusable logic
4. Context providers only where state is truly shared
5. Tailwind styling throughout
6. Routing with React Router
7. Form handling with validation
8. Error boundaries
9. A README with setup instructions
10. A test suite covering components and hooks

### Validation Checklist

- [ ] Verify commands from the project's AGENTS.md or README run (or honest manual checks are listed)
- [ ] No secrets committed; env examples use placeholders only
- [ ] Components split when UI, data fetching, and business rules share one file without need
- [ ] No `any` types
- [ ] All props and state typed
- [ ] No inline styles
- [ ] Reusable logic lives in custom hooks or `lib/`
- [ ] Error boundaries implemented; async failures render a what / why / action message
- [ ] Loading states handled
- [ ] Names match the domain and local convention (Clean-Code 06)
- [ ] TypeScript compiles with no errors

### Pre-Delivery

```bash
npm run build
npm run type-check
npm test
```
