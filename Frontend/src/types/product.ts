export interface Product {
  _id: string;
  name: string;
  price: number;
  description: string;
  images: {
    regular: {
      url: string;
    };
    thumbnail: {
      url: string;
    };
    preview: {
      url: string;
    };
  };
}

export interface CartItem {
  product_id: string;
  quantity: number;
  product?: Product;
}
