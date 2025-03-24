describe("Authentication Flow", () => {
  beforeEach(() => {
    cy.intercept("POST", "/api/auth/login").as("loginRequest");
    cy.intercept("POST", "/api/auth/register").as("registerRequest");
  });

  describe("Login", () => {
    it("should successfully log in with valid credentials", () => {
      cy.visit("/login");

      cy.findByLabelText(/email/i).type("test@example.com");
      cy.findByLabelText(/password/i).type("password123");
      cy.findByRole("button", { name: /sign in/i }).click();

      cy.wait("@loginRequest").its("response.statusCode").should("eq", 200);
      cy.url().should("eq", Cypress.config().baseUrl + "/");
      cy.findByText(/welcome/i).should("be.visible");
    });

    it("should show error message with invalid credentials", () => {
      cy.visit("/login");

      cy.findByLabelText(/email/i).type("wrong@example.com");
      cy.findByLabelText(/password/i).type("wrongpass");
      cy.findByRole("button", { name: /sign in/i }).click();

      cy.wait("@loginRequest").its("response.statusCode").should("eq", 401);
      cy.findByText(/invalid credentials/i).should("be.visible");
    });

    it("should validate required fields", () => {
      cy.visit("/login");

      cy.findByRole("button", { name: /sign in/i }).click();

      cy.findByText(/email is required/i).should("be.visible");
      cy.findByText(/password is required/i).should("be.visible");
    });
  });

  describe("Registration", () => {
    it("should successfully register a new user", () => {
      cy.visit("/register");

      cy.findByLabelText(/name/i).type("Test User");
      cy.findByLabelText(/email/i).type("newuser@example.com");
      cy.findByLabelText(/password/i).type("password123");
      cy.findByLabelText(/confirm password/i).type("password123");
      cy.findByRole("button", { name: /sign up/i }).click();

      cy.wait("@registerRequest").its("response.statusCode").should("eq", 201);
      cy.url().should("eq", Cypress.config().baseUrl + "/");
      cy.findByText(/welcome/i).should("be.visible");
    });

    it("should show error when registering with existing email", () => {
      cy.visit("/register");

      cy.findByLabelText(/name/i).type("Existing User");
      cy.findByLabelText(/email/i).type("existing@example.com");
      cy.findByLabelText(/password/i).type("password123");
      cy.findByLabelText(/confirm password/i).type("password123");
      cy.findByRole("button", { name: /sign up/i }).click();

      cy.wait("@registerRequest").its("response.statusCode").should("eq", 400);
      cy.findByText(/user already exists/i).should("be.visible");
    });

    it("should validate password match", () => {
      cy.visit("/register");

      cy.findByLabelText(/name/i).type("Test User");
      cy.findByLabelText(/email/i).type("test@example.com");
      cy.findByLabelText(/password/i).type("password123");
      cy.findByLabelText(/confirm password/i).type("differentpass");
      cy.findByRole("button", { name: /sign up/i }).click();

      cy.findByText(/passwords do not match/i).should("be.visible");
    });
  });

  describe("Navigation", () => {
    it("should navigate between login and register pages", () => {
      cy.visit("/login");
      cy.findByText(/create an account/i).click();
      cy.url().should("include", "/register");

      cy.findByText(/already have an account/i).click();
      cy.url().should("include", "/login");
    });
  });
});
