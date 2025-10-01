import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import '@testing-library/jest-dom';
import ApplicationContainer from './ApplicationContainer'; 
import { FaDog, FaFire, FaInfoCircle } from 'react-icons/fa';
//"test": "react-scripts test --env=jsdom",

const mockNavigate = jest.fn();
const mockUseLocation = jest.fn();

const mockApplications = [
    { id: 'app-a', formId: 1, status: 'PENDING', applicationID: 'app-a' },
    { id: 'app-b', formId: 2, status: 'APPROVED', applicationID: 'app-b' },
    { id: 'app-c', formId: 3, status: 'REJECTED' }, 
    { id: 'app-d', formId: 99, status: 'UNKNOWN' }, 
  ];
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


  beforeEach(() => {
    jest.clearAllMocks();
    mockUseLocation.mockReturnValue({ pathname: '/default' });
  });
  
  describe('ApplicationContainer', () => {

    it('1. Renders the custom title correctly', () => {
      mockUseQuery.mockReturnValue({
          data: null,
          isLoading: false,
          error: null,
      });
  
      renderWithQueryClient(
        <ApplicationContainer title="Custom Test Title" applications={[]} />
      );
  
      expect(screen.getByText('Custom Test Title')).toBeInTheDocument();
    });
  
    it('2. Displays Loading state when query is loading', () => {
      mockUseQuery.mockReturnValue({
        data: null,
        isLoading: true,
        error: null,
      });
      
      renderWithQueryClient(<ApplicationContainer />);
  
      expect(screen.getByText('Loading applications...')).toBeInTheDocument();
    });
  
    it('3. Displays fetched data when query is successful', () => {
      mockUseQuery.mockReturnValue({
        data: mockApplications,
        isLoading: false,
        error: null,
      });
    })
})




