import React, { useState, useEffect } from "react";
import {
  Box,
  Button,
  Chip,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  FormControl,
  InputLabel,
  MenuItem,
  Paper,
  Select,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TablePagination,
  TableRow,
  TextField,
  Typography,
} from "@mui/material";
import { useSnackbar } from "notistack";
import { api } from "../../utils/api";

interface OrderItem {
  product_id: string;
  product_details: {
    name: string;
    price: number;
  };
  quantity: number;
  price: number;
}

interface ShippingAddress {
  street: string;
  city: string;
  state: string;
  zip: string;
  country: string;
}

interface Order {
  _id: string;
  user_id: string;
  user_email: string;
  items: OrderItem[];
  total: number;
  status: string;
  tracking_number?: string;
  shipping_address: ShippingAddress;
  created_at: string;
}

const ORDER_STATUSES = [
  "pending",
  "processing",
  "shipped",
  "delivered",
  "cancelled",
];

export default function OrderManagement() {
  const [orders, setOrders] = useState<Order[]>([]);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [totalOrders, setTotalOrders] = useState(0);
  const [selectedOrder, setSelectedOrder] = useState<Order | null>(null);
  const [openDialog, setOpenDialog] = useState(false);
  const [trackingNumber, setTrackingNumber] = useState("");
  const [orderStatus, setOrderStatus] = useState("");
  const { enqueueSnackbar } = useSnackbar();

  const fetchOrders = async () => {
    try {
      const response = await api.get(
        `/admin/orders?skip=${page * rowsPerPage}&limit=${rowsPerPage}`
      );
      const data = response.data as { orders: Order[]; total: number };
      setOrders(data.orders);
      setTotalOrders(data.total);
    } catch (error) {
      enqueueSnackbar("Failed to fetch orders", { variant: "error" });
    }
  };

  useEffect(() => {
    fetchOrders();
  }, [page, rowsPerPage]);

  const handleChangePage = (event: unknown, newPage: number) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const handleOpenDialog = (order: Order) => {
    setSelectedOrder(order);
    setTrackingNumber(order.tracking_number || "");
    setOrderStatus(order.status);
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setSelectedOrder(null);
    setTrackingNumber("");
    setOrderStatus("");
  };

  const handleUpdateOrder = async () => {
    if (!selectedOrder) return;

    try {
      await api.put(`/admin/orders/${selectedOrder._id}`, {
        status: orderStatus,
        tracking_number: trackingNumber || undefined,
      });
      enqueueSnackbar("Order updated successfully", { variant: "success" });
      handleCloseDialog();
      fetchOrders();
    } catch (error) {
      enqueueSnackbar("Failed to update order", { variant: "error" });
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "pending":
        return "warning";
      case "processing":
        return "info";
      case "shipped":
        return "primary";
      case "delivered":
        return "success";
      case "cancelled":
        return "error";
      default:
        return "default";
    }
  };

  return (
    <Box>
      <Typography variant="h4" component="h1" sx={{ mb: 4 }}>
        Orders
      </Typography>

      <Paper>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Order ID</TableCell>
                <TableCell>Customer</TableCell>
                <TableCell>Items</TableCell>
                <TableCell>Total</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>Date</TableCell>
                <TableCell>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {orders.map((order) => (
                <TableRow key={order._id}>
                  <TableCell>{order._id}</TableCell>
                  <TableCell>{order.user_email}</TableCell>
                  <TableCell>
                    {order.items.map((item) => (
                      <div key={item.product_id}>
                        {item.product_details.name} x {item.quantity}
                      </div>
                    ))}
                  </TableCell>
                  <TableCell>${order.total.toFixed(2)}</TableCell>
                  <TableCell>
                    <Chip
                      label={order.status}
                      color={getStatusColor(order.status)}
                      size="small"
                    />
                  </TableCell>
                  <TableCell>
                    {new Date(order.created_at).toLocaleDateString()}
                  </TableCell>
                  <TableCell>
                    <Button
                      variant="outlined"
                      size="small"
                      onClick={() => handleOpenDialog(order)}
                    >
                      Manage
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
        <TablePagination
          rowsPerPageOptions={[5, 10, 25]}
          component="div"
          count={totalOrders}
          rowsPerPage={rowsPerPage}
          page={page}
          onPageChange={handleChangePage}
          onRowsPerPageChange={handleChangeRowsPerPage}
        />
      </Paper>

      <Dialog
        open={openDialog}
        onClose={handleCloseDialog}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Manage Order</DialogTitle>
        <DialogContent>
          {selectedOrder && (
            <Box sx={{ mt: 2 }}>
              <Typography variant="subtitle2" gutterBottom>
                Order Details
              </Typography>
              <Typography variant="body2" gutterBottom>
                Order ID: {selectedOrder._id}
              </Typography>
              <Typography variant="body2" gutterBottom>
                Customer: {selectedOrder.user_email}
              </Typography>
              <Typography variant="body2" gutterBottom>
                Total: ${selectedOrder.total.toFixed(2)}
              </Typography>

              <FormControl fullWidth sx={{ mt: 2 }}>
                <InputLabel>Status</InputLabel>
                <Select
                  value={orderStatus}
                  label="Status"
                  onChange={(e) => setOrderStatus(e.target.value)}
                >
                  {ORDER_STATUSES.map((status) => (
                    <MenuItem key={status} value={status}>
                      {status.charAt(0).toUpperCase() + status.slice(1)}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>

              <TextField
                margin="normal"
                fullWidth
                label="Tracking Number"
                value={trackingNumber}
                onChange={(e) => setTrackingNumber(e.target.value)}
              />

              <Typography variant="subtitle2" sx={{ mt: 2 }} gutterBottom>
                Shipping Address
              </Typography>
              <Typography variant="body2">
                {selectedOrder.shipping_address.street}
                <br />
                {selectedOrder.shipping_address.city},{" "}
                {selectedOrder.shipping_address.state}{" "}
                {selectedOrder.shipping_address.zip}
                <br />
                {selectedOrder.shipping_address.country}
              </Typography>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button
            onClick={handleUpdateOrder}
            variant="contained"
            color="primary"
          >
            Update Order
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
