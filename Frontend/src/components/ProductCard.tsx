import React from "react";
import { Button } from "./ui/button";

interface Product {
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
  };
}

interface ProductCardProps {
  product: Product;
  onAddToCart: (productId: string) => void;
}

export default function ProductCard({
  product,
  onAddToCart,
}: ProductCardProps) {
  return (
    <article className="product-tile">
      <div className="product-media">
        <img src={product.images.regular.url} alt={product.name} loading="lazy" />
      </div>
      <h3 className="font-display text-[length:var(--text-lg)] m-0 leading-tight">
        {product.name}
      </h3>
      <p className="text-[var(--color-ink-2)] text-[var(--text-sm)] line-clamp-2 m-0">
        {product.description}
      </p>
      <div className="flex items-center justify-between gap-2 mt-auto">
        <span className="price text-[var(--text-md)] font-medium">
          ${product.price.toFixed(2)}
        </span>
        <Button size="sm" onClick={() => onAddToCart(product._id)}>
          Add
        </Button>
      </div>
    </article>
  );
}
