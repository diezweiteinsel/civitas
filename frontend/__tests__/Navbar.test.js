import { render, screen, fireEvent } from '@testing-library/react';
import { MemoryRouter, NavLink } from 'react-router-dom';
import userEvent from '@testing-library/user-event';
import Navbar from './Navbar';
import { Role } from '../utils/const';

describe('Navbar', () => {

  
    test.each([
      [Role.APPLICANT, '/applicant'],
      [Role.REPORTER, '/reporter'],
      [Role.ADMIN, '/admin'],
      [Role.EMPTY, '/applicant'], 
    ])
  
  
    test('dropdown button is not visible when role is EMPTY', () => {
      renderNavbar(Role.EMPTY);
      expect(screen.queryByRole('button', { name: /toggle dropdown/i })).not.toBeInTheDocument();
      expect(screen.getByRole('navigation').querySelector('.dropdown')).toHaveClass('hidden');
    });
  
    test('dropdown button is visible for non-EMPTY roles', () => {
      renderNavbar(Role.APPLICANT);
      expect(screen.getByRole('button')).toBeInTheDocument();
    });
  
  
    test('toggles the dropdown menu on button click', async () => {
      renderNavbar(Role.APPLICANT);
      const toggleButton = screen.getByRole('button');

      await userEvent.click(toggleButton);
      expect(screen.getByText('Abmelden')).toBeInTheDocument();
      expect(toggleButton).toHaveAttribute('aria-expanded', 'true');
      await userEvent.click(toggleButton);
      expect(screen.queryByText('Abmelden')).not.toBeInTheDocument();
      expect(toggleButton).toHaveAttribute('aria-expanded', 'false');
    });

  
    test('renders correct links for ADMIN role', async () => {
      renderNavbar(Role.ADMIN);
      await userEvent.click(screen.getByRole('button'));
  
      const adminLinks = [
        { text: 'Startseite', to: '/admin' },
        { text: 'Öffentliche Anträge', to: '/admin/public?from=admin' },
        { text: 'Formular erstellen', to: '/admin/create-forms' },
        { text: 'Admin registrieren', to: '/admin/admin-registration' },
        { text: 'Reporter registrieren', to: '/admin/reporter-registration' },
      ];
  
      adminLinks.forEach(link => {
        const linkElement = screen.getByText(link.text);
        expect(linkElement).toBeInTheDocument();
        expect(linkElement).toHaveAttribute('href', link.to);
      });
  
      expect(screen.queryByText('Antrag einreichen')).not.toBeInTheDocument();
    });
  
    test('renders correct links for APPLICANT role', async () => {
      renderNavbar(Role.APPLICANT);
      await userEvent.click(screen.getByRole('button'));
  
      const applicantLinks = [
        { text: 'Startseite', to: '/applicant' },
        { text: 'Öffentliche Anträge', to: '/applicant/public?from=applicant' },
        { text: 'Antrag einreichen', to: '/applicant/submit' },
      ];
  
      applicantLinks.forEach(link => {
        const linkElement = screen.getByText(link.text);
        expect(linkElement).toBeInTheDocument();
        expect(linkElement).toHaveAttribute('href', link.to);
      });
  
      expect(screen.queryByText('Admin registrieren')).not.toBeInTheDocument();
    });
  
    test('renders correct links for REPORTER role', async () => {
      renderNavbar(Role.REPORTER);
      await userEvent.click(screen.getByRole('button')); 
  
      const reporterLinks = [
        { text: 'Startseite', to: '/reporter' },
        { text: 'Ausstehende Anträge', to: '/reporter/pending' },
        { text: 'Genehmigte Anträge', to: '/reporter/approved' },
        { text: 'Abgelehnte Anträge', to: '/reporter/rejected' },
      ];
  
      reporterLinks.forEach(link => {
        const linkElement = screen.getByText(link.text);
        expect(linkElement).toBeInTheDocument();
        expect(linkElement).toHaveAttribute('href', link.to);
      });
  
    });
  
    test('renders "Abmelden" link for all non-EMPTY roles', async () => {
      renderNavbar(Role.ADMIN);
      await userEvent.click(screen.getByRole('button')); 
      const logoutLink = screen.getByText('Abmelden');
      expect(logoutLink).toBeInTheDocument();
      expect(logoutLink).toHaveAttribute('href', '/');
    })
  
    test('clicking a dropdown link closes the dropdown', async () => {
      renderNavbar(Role.APPLICANT);
      await userEvent.click(screen.getByRole('button')); 
      expect(screen.getByText('Startseite')).toBeInTheDocument(); 
  
      await userEvent.click(screen.getByText('Startseite'));
  
      expect(screen.queryByText('Startseite')).not.toBeInTheDocument();
      expect(screen.getByRole('button')).toHaveAttribute('aria-expanded', 'false');
    });
  
    test('clicking outside the dropdown closes the dropdown', async () => {
      renderNavbar(Role.APPLICANT);
      const toggleButton = screen.getByRole('button');
      await userEvent.click(toggleButton); 
      expect(screen.getByText('Abmelden')).toBeInTheDocument(); 
  
      fireEvent.mouseDown(document.body);
  
      expect(screen.queryByText('Abmelden')).not.toBeInTheDocument();
      expect(toggleButton).toHaveAttribute('aria-expanded', 'false');
    });
  
    test('clicking inside the dropdown does NOT close the dropdown', async () => {
      renderNavbar(Role.APPLICANT);
      const toggleButton = screen.getByRole('button');
      await userEvent.click(toggleButton); 
      const logoutLink = screen.getByText('Abmelden');
      
      fireEvent.mouseDown(logoutLink.closest('.dropdown-item'));
  
      expect(screen.getByText('Abmelden')).toBeInTheDocument();
      expect(toggleButton).toHaveAttribute('aria-expanded', 'true');
    });
  });