import { api } from "../lib/api";
import { User } from "../types";

interface UsersResponse {
  users: User[];
  total: number;
}

interface UserResponse {
  user: User;
}

export const userService = {
  // Get all users with pagination and filters (admin only)
  getUsers: async (params: {
    page?: number;
    limit?: number;
    search?: string;
    role?: User["role"];
    sortBy?: string;
    sortOrder?: "asc" | "desc";
  }) => {
    const response = await api.get<UsersResponse>("/admin/users", { params });
    return response.data;
  },

  // Get a single user by ID (admin only)
  getUser: async (id: string) => {
    const response = await api.get<UserResponse>(`/admin/users/${id}`);
    return response.data.user;
  },

  // Update user role (admin only)
  updateUserRole: async (id: string, role: User["role"]) => {
    const response = await api.patch<UserResponse>(`/admin/users/${id}/role`, {
      role,
    });
    return response.data.user;
  },

  // Update user active status (admin only)
  updateUserStatus: async (id: string, isActive: boolean) => {
    const response = await api.patch<UserResponse>(
      `/admin/users/${id}/status`,
      {
        isActive,
      }
    );
    return response.data.user;
  },

  // Delete user (admin only)
  deleteUser: async (id: string) => {
    await api.delete(`/admin/users/${id}`);
  },
};
