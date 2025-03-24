import "@testing-library/cypress/add-commands";

// Cypress custom commands
declare global {
  namespace Cypress {
    interface Chainable {
      // Add custom commands here if needed
    }
  }
}

beforeEach(() => {
  // Clear localStorage before each test
  cy.clearLocalStorage();
});
