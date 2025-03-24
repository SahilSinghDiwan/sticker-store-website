import { api } from "../lib/api";
import { Product } from "./product.service";

export interface CartItem {
  product: Product;
  quantity: number;
}

interface CartResponse {
  items: CartItem[];
  total: number;
}

export const cartService = {
  // Get cart contents
  getCart: async () => {
    const response = await api.get<CartResponse>("/cart");
    return response.data;
  },

  // Add item to cart
  addToCart: async (productId: string, quantity: number = 1) => {
    const response = await api.post<CartResponse>("/cart/items", {
      productId,
      quantity,
    });
    return response.data;
  },

  // Update item quantity
  updateQuantity: async (productId: string, quantity: number) => {
    const response = await api.patch<CartResponse>(`/cart/items/${productId}`, {
      quantity,
    });
    return response.data;
  },

  // Remove item from cart
  removeFromCart: async (productId: string) => {
    const response = await api.delete<CartResponse>(`/cart/items/${productId}`);
    return response.data;
  },

  // Clear cart
  clearCart: async () => {
    const response = await api.delete<CartResponse>("/cart");
    return response.data;
  },
};
