export interface User {
  _id: string;
  email: string;
  firstName?: string;
  lastName?: string;
  role: "user" | "admin";
  isActive: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface Product {
  _id: string;
  name: string;
  description: string;
  price: number;
  imageUrl: string;
  images: string[];
  stock: number;
  category: string;
  tags: string[];
  rating: number;
  numReviews: number;
  createdAt: string;
  updatedAt: string;
}

export interface ProductReview {
  _id: string;
  user: User;
  product: string;
  rating: number;
  comment: string;
  createdAt: string;
}

export interface CartItem {
  product: Product;
  quantity: number;
}

export interface Cart {
  items: CartItem[];
  total: number;
  subtotal: number;
  tax: number;
  shipping: number;
}

export interface ShippingAddress {
  firstName: string;
  lastName: string;
  street: string;
  city: string;
  state: string;
  zip: string;
  country: string;
  phone: string;
}

export interface OrderItem extends CartItem {
  price: number;
}

export type OrderStatus =
  | "pending"
  | "processing"
  | "shipped"
  | "delivered"
  | "cancelled";

export interface Order {
  _id: string;
  user: User;
  items: OrderItem[];
  shippingAddress: ShippingAddress;
  paymentMethod: "card" | "paypal";
  paymentDetails: {
    id: string;
    status: string;
    updateTime: string;
  };
  itemsPrice: number;
  taxPrice: number;
  shippingPrice: number;
  totalPrice: number;
  status: OrderStatus;
  trackingNumber?: string;
  notes?: string;
  createdAt: string;
  updatedAt: string;
}

export interface SalesData {
  date: string;
  revenue: number;
  orders: number;
  averageOrderValue: number;
}

export interface ProductPerformance {
  product: Product;
  totalSales: number;
  totalRevenue: number;
  totalUnits: number;
}

export interface UserMetrics {
  totalUsers: number;
  activeUsers: number;
  newUsers: number;
  returningUsers: number;
}

export interface AnalyticsDashboard {
  summary: {
    totalRevenue: number;
    totalOrders: number;
    averageOrderValue: number;
    totalProducts: number;
    totalCustomers: number;
  };
  salesTrends: SalesData[];
  topProducts: ProductPerformance[];
  userMetrics: UserMetrics;
  lowStockProducts: Product[];
  recentOrders: Order[];
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  limit: number;
  totalPages: number;
}

export interface ApiResponse<T> {
  success: boolean;
  data: T;
  message?: string;
}

export interface ApiError {
  success: boolean;
  message: string;
  errors?: Record<string, string[]>;
}

export interface FilterParams {
  search?: string;
  category?: string;
  minPrice?: number;
  maxPrice?: number;
  inStock?: boolean;
  rating?: number;
}

export interface SortParams {
  field: string;
  order: "asc" | "desc";
}

export interface PaginationParams {
  page: number;
  limit: number;
}

export interface PaymentIntent {
  clientSecret: string;
  amount: number;
  currency: string;
}

export interface PaymentMethod {
  id: string;
  type: "card" | "paypal";
  card?: {
    brand: string;
    last4: string;
    expiryMonth: number;
    expiryYear: number;
  };
}

export interface Notification {
  _id: string;
  user: string;
  type: "order" | "payment" | "shipping" | "system";
  title: string;
  message: string;
  read: boolean;
  createdAt: string;
}
