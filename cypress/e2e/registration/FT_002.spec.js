/// <reference types="cypress" />
import Chance from 'chance';

const chance = new Chance();

describe('Verify that new user can register successfully.', () => {
  it('Check if home page URL is correct.', () => {
    cy.url().then(url => cy.wrap(url).should('eq', 'http://localhost:8111/'));
  });

  describe('Check that initial home page content is valid.', () => {
    it('Check navbar text content and buttons visibility.', () => {
      cy.get('a.navbar-brand')
        .should('be.visible')
        .and('contain.text', 'Some Company - Your ultimate place with job offers.');
      cy.get('nav').find('a.btn').as('navbarButtons').should('have.length', 3);
      cy.get('@navbarButtons').then($navbarButtons => {
        cy.wrap($navbarButtons).eq(0).should('be.visible').and('contain.text', 'Home');
        cy.wrap($navbarButtons).eq(1).should('be.visible').and('contain.text', 'Login');
        cy.wrap($navbarButtons).eq(2).should('be.visible').and('contain.text', 'Register');
      });
    });

    it('Verify that banner image exists and is visible.', () => {
      cy.get('img#banner').should('exist').and('be.visible');
    });

    it('Verify that heading text on the home page is correct.', () => {
      cy.get('h1').should('be.visible').and('contain.text', 'Some Company');
    });

    it('Verify that lead paragraph text is correct.', () => {
      cy.get('p.lead').then($p =>
        expect($p.get(0).innerText).to.eq(
          'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
        )
      );
    });

    it('Verify that second image with a person is displayed on the home page.', () => {
      cy.get('img[src*=person]').should('exist').and('be.visible');
    });

    it('Check if job offerings header is displayed correctly.', () => {
      cy.get('h2').should('be.visible').and('contain.text', 'Job Offers');
    });

    it('Verify that stock job offerings are visible and contain valid buttons.', () => {
      cy.get('div.border-bottom.row').as('jobOfferingRows').should('have.length.at.least', 6);
      cy.get('@jobOfferingRows').each($row => {
        cy.wrap($row).within(() => {
          cy.get('h4').should('have.length.at.least', 1);
          cy.contains('div', 'Location');
          cy.contains('div', 'Salary');
          cy.get('a.btn').eq(0).should('exist').and('be.visible').and('not.be.disabled').and('contain.text', 'Details');
          cy.get('a.btn').eq(1).should('exist').and('be.visible').and('not.be.disabled').and('contain.text', 'Ask');
        });
      });
    });

    it('Check if "Contact Us" button is visible and not disabled.', () => {
      cy.contains('a.btn', 'Contact Us')
        .should('exist')
        .and('be.visible')
        .and('not.be.disabled')
        .and('contain.text', 'Contact Us');
    });

    it('Verify navlinks are visible and contain correct content at the bottom of home page.', () => {
      cy.get('a.nav-link').then($navLinks => {
        cy.wrap($navLinks).eq(0).should('exist').and('be.visible').and('not.be.disabled').and('contain.text', 'Home');
        cy.wrap($navLinks).eq(1).should('exist').and('be.visible').and('not.be.disabled').and('contain.text', 'About');
      });
    });

    it('Verify that footer at the most bottom of the page is visible.', () => {
      cy.get('footer > p').should('exist').and('be.visible').and('contain.text', '© 2024 Some Company, Inc');
    });
  });

  describe('Check that register page is displayed correctly.', () => {
    it('Click on the "Register" navbar button.', () => {
      cy.intercept('GET', '**/register').as('getRegister');
      cy.get('nav').contains('Register').click();
      cy.wait('@getRegister');
      cy.url().then(url => cy.wrap(url).should('eq', 'http://localhost:8111/register'));
    });

    it('Check if navbar button of "Register" is no longer available.', () => {
      cy.get('a.navbar-brand')
        .should('be.visible')
        .and('contain.text', 'Some Company - Your ultimate place with job offers.');
      cy.get('nav').find('a.btn').contains('Register').should('not.exist');
    });

    it('Check "Register" header.', () => {
      cy.get('h2').should('contain.text', 'Register');
    });

    it('Check form fields, labels and Register button.', () => {
      cy.get('form > div')
        .as('formDiv')
        .eq(0)
        .within(() => {
          cy.get('label').should('be.visible').and('contain.text', 'First Name*');
          cy.get('input').should('be.visible').and('not.be.disabled').and('have.attr', 'required');
        });
      cy.get('@formDiv')
        .eq(1)
        .within(() => {
          cy.get('label').should('be.visible').and('contain.text', 'Last Name*');
          cy.get('input').should('be.visible').and('not.be.disabled').and('have.attr', 'required');
        });
      cy.get('@formDiv')
        .eq(2)
        .within(() => {
          cy.get('label').should('be.visible').and('contain.text', 'Email*');
          cy.get('input').should('be.visible').and('not.be.disabled').and('have.attr', 'required');
        });
      cy.get('@formDiv')
        .eq(3)
        .within(() => {
          cy.get('label').should('be.visible').and('contain.text', 'Password*');
          cy.get('input').should('be.visible').and('not.be.disabled').and('have.attr', 'required');
        });
      cy.get('@formDiv')
        .last()
        .should('exist')
        .and('be.visible')
        .and('not.be.disabled')
        .and('contain.text', 'Register');
    });
  });

  describe('Provide new user credentials and click on the Register button.', () => {
    const userData = {
      firstName: chance.first({ nationality: 'en' }),
      lastName: chance.last({ nationality: '*' }),
      email: chance.email({ length: 15, domain: 'example.com' }),
      password: chance.string({
        length: 20,
        pool: 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()',
      }),
    };

    it('Provide first name of the user in the First Name input field.', () => {
      cy.get('input#first_name').type(userData.firstName);
    });

    it('Provide last name of the user in the Last Name input field.', () => {
      cy.get('input#last_name').type(userData.lastName);
    });

    it('Provide email address of the user in the Email input field.', () => {
      cy.get('input[type=email]').type(userData.email);
    });

    it('Provide password of the user in Password input field.', () => {
      cy.get('input[type=password]').type(userData.password);
    });

    it('Click on the Register button.', () => {
      cy.intercept('POST', '**/register').as('postRegister');
      cy.contains('button', 'Register').click();
      cy.wait('@postRegister').its('response.statusCode').should('eq', 302);
      cy.url().then(url => cy.wrap(url).should('eq', 'http://localhost:8111/'));
    });
  });

  describe('Check navbar content after user has been enrolled.', () => {
    it('Verify post-register alert visibility and message content.', () => {
      cy.get('div.alert')
        .contains('Account has been registered.')
        .should('exist')
        .and('be.visible')
        .and('have.class', 'alert-success');
    });

    it('Close alert message and assert inexistence afterwards.', () => {
      cy.get('div.alert').as('alert').find('button.btn-close').click();
      cy.get('@alert').should('not.exist');
    });

    it('Check if the following buttons: "Home", "Profile" and "Logout" are properly displayed and clickable within navbar.', () => {
      cy.get('a.navbar-brand')
        .should('be.visible')
        .and('contain.text', 'Some Company - Your ultimate place with job offers.');
      cy.get('nav').find('a.btn').as('navbarButtons').should('have.length', 3);
      cy.get('@navbarButtons').then($navbarButtons => {
        cy.wrap($navbarButtons).contains('Login').should('not.exist');
        cy.wrap($navbarButtons).eq(0).should('be.visible').and('not.be.disabled').and('contain.text', 'Home');
        cy.wrap($navbarButtons).eq(1).should('be.visible').and('not.be.disabled').and('contain.text', 'Profile');
        cy.wrap($navbarButtons).eq(2).should('be.visible').and('not.be.disabled').and('contain.text', 'Logout');
      });
    });
  });

  describe('Verify that user can successfully logout out of the site after being enrolled.', () => {
    it('Click on the "Logout" navbar button.', () => {
      cy.intercept('GET', '**/logout').as('getLogout');
      cy.get('nav').contains('Logout').click();
      cy.wait('@getLogout').its('response.statusCode').should('eq', 302);
      cy.url().then(url => cy.wrap(url).should('eq', 'http://localhost:8111/'));
    });

    it('Verify post-logout alert visibility and message content.', () => {
      cy.get('div.alert')
        .contains("You've been logged out.")
        .should('exist')
        .and('be.visible')
        .and('have.class', 'alert-primary');
    });

    it('Close alert message and assert inexistence afterwards.', () => {
      cy.get('div.alert').as('alert').find('button.btn-close').click();
      cy.get('@alert').should('not.exist');
    });

    it('Check navbar text content and buttons after successful logout operation.', () => {
      cy.get('a.navbar-brand')
        .should('be.visible')
        .and('contain.text', 'Some Company - Your ultimate place with job offers.');
      cy.get('nav').find('a.btn').as('navbarButtons').should('have.length', 3);
      cy.get('@navbarButtons').then($navbarButtons => {
        cy.wrap($navbarButtons).contains('Applications').should('not.exist');
        cy.wrap($navbarButtons).contains('Profile').should('not.exist');
        cy.wrap($navbarButtons).contains('Logout').should('not.exist');
        cy.wrap($navbarButtons).eq(0).should('be.visible').and('contain.text', 'Home');
        cy.wrap($navbarButtons).eq(1).should('be.visible').and('contain.text', 'Login');
        cy.wrap($navbarButtons).eq(2).should('be.visible').and('contain.text', 'Register');
      });
    });
  });
});
