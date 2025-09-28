// Minimal CommonJS mock for react-router-dom used in tests.
let _navigate = () => {};

function MemoryRouter({ children }) {
  return children;
}

function useNavigate() {
  return _navigate;
}

function NavLink({ to, children }) {
  return children;
}

function __setMockNavigate(fn) {
  _navigate = fn;
}

module.exports = {
  MemoryRouter,
  useNavigate,
  NavLink,
  __setMockNavigate,
};
