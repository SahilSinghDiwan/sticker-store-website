import { api } from "../lib/api";
import { Product } from "./product.service";

export interface OrderItem {
  product: Product;
  quantity: number;
  price: number;
}

export interface ShippingAddress {
  street: string;
  city: string;
  state: string;
  zip: string;
  country: string;
}

export interface Order {
  _id: string;
  user: string;
  items: OrderItem[];
  total: number;
  status: "pending" | "processing" | "shipped" | "delivered" | "cancelled";
  shippingAddress: ShippingAddress;
  trackingNumber?: string;
  createdAt: string;
  updatedAt: string;
}

interface OrdersResponse {
  orders: Order[];
  total: number;
}

interface OrderResponse {
  order: Order;
}

export const orderService = {
  // Get orders with pagination and filters (admin gets all, users get their own)
  getOrders: async (params: {
    page?: number;
    limit?: number;
    status?: Order["status"];
    sortBy?: string;
    sortOrder?: "asc" | "desc";
  }) => {
    const response = await api.get<OrdersResponse>("/orders", { params });
    return response.data;
  },

  // Get a single order by ID
  getOrder: async (id: string) => {
    const response = await api.get<OrderResponse>(`/orders/${id}`);
    return response.data.order;
  },

  // Create a new order
  createOrder: async (orderData: {
    items: { productId: string; quantity: number }[];
    shippingAddress: ShippingAddress;
  }) => {
    const response = await api.post<OrderResponse>("/orders", orderData);
    return response.data.order;
  },

  // Update order status (admin only)
  updateOrderStatus: async (
    id: string,
    data: {
      status: Order["status"];
      trackingNumber?: string;
    }
  ) => {
    const response = await api.patch<OrderResponse>(
      `/orders/${id}/status`,
      data
    );
    return response.data.order;
  },

  // Cancel order (user can cancel their pending orders)
  cancelOrder: async (id: string) => {
    const response = await api.post<OrderResponse>(`/orders/${id}/cancel`);
    return response.data.order;
  },
};
