import { useState, useEffect } from "react";
import { api } from "../lib/api";
import { Button } from "./ui/button";
import { useSnackbar } from "notistack";

interface Product {
  _id: string;
  name: string;
  description: string;
  price: number;
  imageUrl: string;
  stock: number;
}

export default function Home() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const { enqueueSnackbar } = useSnackbar();

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      const response = await api.get("/products");
      const data = response.data as { products: Product[] };
      setProducts(data.products);
    } catch (error) {
      console.error("Failed to fetch products:", error);
      enqueueSnackbar("Failed to load products", { variant: "error" });
    } finally {
      setLoading(false);
    }
  };

  const addToCart = async (productId: string) => {
    try {
      await api.post("/cart/items", { productId, quantity: 1 });
      enqueueSnackbar("Added to cart", { variant: "success" });
    } catch (error) {
      console.error("Failed to add to cart:", error);
      enqueueSnackbar("Failed to add to cart", { variant: "error" });
    }
  };

  if (loading) {
    return (
      <div className="grid gap-6">
        <div className="h-10 w-48 rounded-[var(--radius-card)] bg-[var(--color-paper-2)]" />
        <div className="product-grid">
          {Array.from({ length: 8 }).map((_, i) => (
            <div key={i} className="product-tile">
              <div className="product-media bg-[var(--color-paper-2)]" />
              <div className="h-4 w-3/4 rounded bg-[var(--color-paper-2)]" />
              <div className="h-3 w-1/2 rounded bg-[var(--color-paper-2)]" />
            </div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div>
      <header className="mb-[var(--space-xl)] max-w-2xl">
        <p className="font-mono text-[var(--text-xs)] uppercase tracking-[0.08em] text-[var(--color-ink-2)] mb-[var(--space-2xs)]">
          Collection
        </p>
        <h1 className="font-display text-[length:var(--text-display)] leading-[1.05] m-0">
          Sticker Shop
        </h1>
        <p className="mt-[var(--space-sm)] text-[var(--text-md)] text-[var(--color-ink-2)] max-w-prose">
          Vinyl stickers from the print studio — peel, stick, claim a surface.
        </p>
      </header>

      <div className="product-grid">
        {products.map((product) => (
          <article key={product._id} className="product-tile">
            <div className="product-media">
              <img
                src={product.imageUrl}
                alt={product.name}
                loading="lazy"
              />
            </div>
            <div className="min-w-0">
              <h2 className="font-display text-[length:var(--text-lg)] m-0 leading-tight truncate">
                {product.name}
              </h2>
              <p className="mt-[var(--space-3xs)] text-[var(--color-ink-2)] text-[var(--text-sm)] line-clamp-2">
                {product.description}
              </p>
            </div>
            <div className="mt-auto flex items-center justify-between gap-[var(--space-2xs)]">
              <span className="price text-[var(--text-md)] font-medium">
                ${product.price.toFixed(2)}
              </span>
              <Button
                size="sm"
                onClick={() => addToCart(product._id)}
                disabled={product.stock === 0}
              >
                {product.stock === 0 ? "Sold out" : "Add"}
              </Button>
            </div>
            {product.stock < 5 && product.stock > 0 && (
              <p className="font-mono text-[var(--text-xs)] text-[var(--color-accent)] m-0">
                {product.stock} left
              </p>
            )}
          </article>
        ))}
      </div>

      {products.length === 0 && (
        <div className="py-[var(--space-2xl)]">
          <p className="text-[var(--color-ink-2)] m-0">
            No stickers in the rack yet.
          </p>
        </div>
      )}
    </div>
  );
}
