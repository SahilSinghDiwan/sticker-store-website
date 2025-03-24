const ADMIN_CREDENTIALS = btoa("admin:admin123"); // Base64 encode credentials

const adminApi = {
  async getProducts() {
    const response = await fetch("/admin/products", {
      headers: {
        Authorization: `Basic ${ADMIN_CREDENTIALS}`,
      },
    });
    if (!response.ok) throw new Error("Failed to fetch products");
    return response.json();
  },

  async getUsers() {
    const response = await fetch("/admin/users", {
      headers: {
        Authorization: `Basic ${ADMIN_CREDENTIALS}`,
      },
    });
    if (!response.ok) throw new Error("Failed to fetch users");
    return response.json();
  },

  async addProduct(formData: FormData) {
    const response = await fetch("/admin/products", {
      method: "POST",
      headers: {
        Authorization: `Basic ${ADMIN_CREDENTIALS}`,
      },
      body: formData,
    });
    if (!response.ok) throw new Error("Failed to add product");
    return response.json();
  },

  async updateProduct(productId: string, formData: FormData) {
    const response = await fetch(`/admin/products/${productId}`, {
      method: "PUT",
      headers: {
        Authorization: `Basic ${ADMIN_CREDENTIALS}`,
      },
      body: formData,
    });
    if (!response.ok) throw new Error("Failed to update product");
    return response.json();
  },

  async deleteProduct(productId: string) {
    const response = await fetch(`/admin/products/${productId}`, {
      method: "DELETE",
      headers: {
        Authorization: `Basic ${ADMIN_CREDENTIALS}`,
      },
    });
    if (!response.ok) throw new Error("Failed to delete product");
    return response.json();
  },

  async getSalesAnalytics() {
    const response = await fetch("/admin/analytics/sales", {
      headers: {
        Authorization: `Basic ${ADMIN_CREDENTIALS}`,
      },
    });
    if (!response.ok) throw new Error("Failed to fetch sales analytics");
    return response.json();
  },

  async getOrders() {
    const response = await fetch("/admin/orders", {
      headers: {
        Authorization: `Basic ${ADMIN_CREDENTIALS}`,
      },
    });
    if (!response.ok) throw new Error("Failed to fetch orders");
    return response.json();
  },

  async updateOrderShipping(orderId: string, status: string) {
    const response = await fetch(`/admin/orders/${orderId}/shipping`, {
      method: "PUT",
      headers: {
        Authorization: `Basic ${ADMIN_CREDENTIALS}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ status }),
    });
    if (!response.ok) throw new Error("Failed to update shipping status");
    return response.json();
  },
};

export default adminApi;
