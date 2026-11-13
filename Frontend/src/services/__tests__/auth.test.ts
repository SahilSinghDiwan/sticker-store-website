/**
 * @jest-environment node
 */
import { http, HttpResponse } from "msw";
import { setupServer } from "msw/node";
import axios from "axios";
import { authService } from "../auth";

// Node has no page origin, so give axios one for relative /api URLs.
axios.defaults.baseURL = "http://localhost";

interface LoginRequest {
  email: string;
  password: string;
}

interface RegisterRequest extends LoginRequest {
  firstName: string;
  lastName: string;
  phoneNumber: string;
}

interface AuthResponse {
  token: string;
  user: {
    _id: string;
    email: string;
    firstName: string;
    lastName: string;
    phoneNumber: string;
    role: "user" | "admin";
  };
}

const server = setupServer(
  // Mock login endpoint
  http.post("http://localhost/api/auth/login", async ({ request }) => {
    const body = (await request.json()) as LoginRequest;

    if (body.email === "test@example.com" && body.password === "password123") {
      return HttpResponse.json<AuthResponse>(
        {
          token: "fake-jwt-token",
          user: {
            _id: "1",
            email: "test@example.com",
            firstName: "Test",
            lastName: "User",
            phoneNumber: "1234567890",
            role: "user",
          },
        },
        { status: 200 }
      );
    }

    return HttpResponse.json(
      { message: "Invalid credentials" },
      { status: 401 }
    );
  }),

  // Mock register endpoint
  http.post("http://localhost/api/auth/register", async ({ request }) => {
    const body = (await request.json()) as RegisterRequest;

    if (body.email === "existing@example.com") {
      return HttpResponse.json(
        { message: "User already exists" },
        { status: 400 }
      );
    }

    return HttpResponse.json<AuthResponse>(
      {
        token: "fake-jwt-token",
        user: {
          _id: "2",
          email: body.email,
          firstName: body.firstName,
          lastName: body.lastName,
          phoneNumber: body.phoneNumber,
          role: "user",
        },
      },
      { status: 201 }
    );
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe("Auth Service", () => {
  describe("login", () => {
    it("should successfully login with valid credentials", async () => {
      const response = await authService.login({
        email: "test@example.com",
        password: "password123",
      });

      expect(response.token).toBe("fake-jwt-token");
      expect(response.user).toEqual({
        _id: "1",
        email: "test@example.com",
        firstName: "Test",
        lastName: "User",
        phoneNumber: "1234567890",
        role: "user",
      });
    });

    it("should throw error with invalid credentials", async () => {
      await expect(
        authService.login({
          email: "wrong@example.com",
          password: "wrongpass",
        })
      ).rejects.toThrow("Invalid credentials");
    });
  });

  describe("register", () => {
    it("should successfully register a new user", async () => {
      const userData = {
        email: "new@example.com",
        password: "password123",
        firstName: "New",
        lastName: "User",
        phoneNumber: "1234567890",
      };

      const response = await authService.register(userData);

      expect(response.token).toBe("fake-jwt-token");
      expect(response.user).toEqual({
        _id: "2",
        email: userData.email,
        firstName: userData.firstName,
        lastName: userData.lastName,
        phoneNumber: userData.phoneNumber,
        role: "user",
      });
    });

    it("should throw error when registering existing email", async () => {
      await expect(
        authService.register({
          email: "existing@example.com",
          password: "password123",
          firstName: "Existing",
          lastName: "User",
          phoneNumber: "1234567890",
        })
      ).rejects.toThrow("User already exists");
    });
  });
});
