import { api } from "../lib/api";

export interface Product {
  _id: string;
  name: string;
  description: string;
  price: number;
  imageUrl: string;
  stock: number;
  category: string;
  createdAt: string;
  updatedAt: string;
}

interface ProductsResponse {
  products: Product[];
  total: number;
}

interface ProductResponse {
  product: Product;
}

export const productService = {
  // Get products with pagination and filters
  getProducts: async (params: {
    page?: number;
    limit?: number;
    search?: string;
    category?: string;
    sortBy?: string;
    sortOrder?: "asc" | "desc";
  }) => {
    const response = await api.get<ProductsResponse>("/products", { params });
    return response.data;
  },

  // Get a single product by ID
  getProduct: async (id: string) => {
    const response = await api.get<ProductResponse>(`/products/${id}`);
    return response.data.product;
  },

  // Create a new product (admin only)
  createProduct: async (productData: FormData) => {
    const response = await api.post<ProductResponse>("/products", productData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    return response.data.product;
  },

  // Update a product (admin only)
  updateProduct: async (id: string, productData: FormData) => {
    const response = await api.put<ProductResponse>(
      `/products/${id}`,
      productData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      }
    );
    return response.data.product;
  },

  // Delete a product (admin only)
  deleteProduct: async (id: string) => {
    await api.delete(`/products/${id}`);
  },
};
