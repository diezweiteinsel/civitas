import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import ApplicationContainer from './ApplicationContainer'; 
import { FaDog, FaFire, FaInfoCircle } from 'react-icons/fa';

const mockNavigate = jest.fn();
const mockUseLocation = jest.fn();

jest.mock('react-router-dom', () => ({
    useNavigate: () => mockNavigate,
    useLocation: () => mockUseLocation(),
  }));

const mockUseQuery = jest.fn();
jest.mock('@tanstack/react-query', () => ({
  ...jest.requireActual('@tanstack/react-query'),
  useQuery: (options) => mockUseQuery(options),
}));

jest.mock('react-icons/fa', () => ({
    FaDog: () => <div data-testid="icon-dog" />,
    FaFire: () => <div data-testid="icon-fire" />,
    FaInfoCircle: () => <div data-testid="icon-info" />,
  }))