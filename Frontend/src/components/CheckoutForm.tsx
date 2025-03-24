import { useState } from "react";
import {
  useStripe,
  useElements,
  PaymentElement,
} from "@stripe/react-stripe-js";
import { Button } from "./ui/button";

interface CheckoutFormProps {
  clientSecret: string;
  total: number;
}

export default function CheckoutForm({
  clientSecret,
  total,
}: CheckoutFormProps) {
  const stripe = useStripe();
  const elements = useElements();
  const [error, setError] = useState<string | null>(null);
  const [processing, setProcessing] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!stripe || !elements) {
      return;
    }

    setProcessing(true);

    try {
      const { error: submitError } = await elements.submit();
      if (submitError) {
        setError(submitError.message || "An error occurred");
        return;
      }

      const { error: paymentError } = await stripe.confirmPayment({
        elements,
        clientSecret,
        confirmParams: {
          return_url: `${window.location.origin}/order-confirmation`,
        },
      });

      if (paymentError) {
        setError(paymentError.message || "Payment failed");
      }
    } catch (err) {
      setError("An unexpected error occurred");
    } finally {
      setProcessing(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-xl font-semibold mb-4">Payment Details</h2>
        <div className="mb-4">
          <PaymentElement />
        </div>
        {error && <div className="text-red-600 text-sm mb-4">{error}</div>}
        <div className="flex justify-between items-center">
          <span className="text-lg font-semibold">
            Total: ${total.toFixed(2)}
          </span>
          <Button
            type="submit"
            disabled={!stripe || processing}
            className={`${processing ? "opacity-50 cursor-not-allowed" : ""}`}
          >
            {processing ? "Processing..." : "Pay Now"}
          </Button>
        </div>
      </div>
    </form>
  );
}
