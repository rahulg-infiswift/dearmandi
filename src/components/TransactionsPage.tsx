// app/home/transactions/page.tsx
"use client";

import React, { useEffect, useState } from "react";
import { Plus, Edit2, Trash2 } from "lucide-react";
import axios from "axios";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

interface Transaction {
  id: string;
  commodity_id: string;
  counterparty_id: string;
  quantity: number;
  price: number;
  transaction_type: string;
  date: string;
  notes: string;
}

interface Commodity {
  id: string;
  name: string;
}

interface Counterparty {
  id: string;
  name: string;
}

export default function TransactionsPage() {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [commodities, setCommodities] = useState<Commodity[]>([]);
  const [counterparties, setCounterparties] = useState<Counterparty[]>([]);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [newTransaction, setNewTransaction] = useState({
    commodity_id: "",
    counterparty_id: "",
    quantity: "",
    price: "",
    transaction_type: "PURCHASE",
    date: "",
    notes: "",
  });
  const token =
    typeof window !== "undefined" ? localStorage.getItem("token") : null;

  // Fetch data
  useEffect(() => {
    fetchTransactions();
    fetchCommodities();
    fetchCounterparties();
  }, []);

  const fetchTransactions = async () => {
    try {
      const response = await axios.get("/api/transactions/", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setTransactions(response.data);
    } catch (error) {
      console.error("Error fetching transactions:", error);
    }
  };

  const fetchCommodities = async () => {
    try {
      const response = await axios.get("/api/commodities/", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setCommodities(response.data);
    } catch (error) {
      console.error("Error fetching commodities:", error);
    }
  };

  const fetchCounterparties = async () => {
    try {
      const response = await axios.get("/api/counterparties/", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setCounterparties(response.data);
    } catch (error) {
      console.error("Error fetching counterparties:", error);
    }
  };

  const handleAddTransaction = async () => {
    try {
      await axios.post("/api/transactions/", newTransaction, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setNewTransaction({
        commodity_id: "",
        counterparty_id: "",
        quantity: "",
        price: "",
        transaction_type: "PURCHASE",
        date: "",
        notes: "",
      });
      setIsDialogOpen(false);
      fetchTransactions();
    } catch (error) {
      console.error("Error adding transaction:", error);
    }
  };

  // Similar edit and delete functions can be implemented

  return (
    <div>
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-semibold">Transactions</h1>
        <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
          <DialogTrigger asChild>
            <Button>
              <Plus className="mr-2 h-4 w-4" />
              Add Transaction
            </Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Add Transaction</DialogTitle>
              <DialogDescription>
                Enter the details of the new transaction.
              </DialogDescription>
            </DialogHeader>
            <div className="space-y-4 py-2 pb-4">
              <Select
                onValueChange={(value) =>
                  setNewTransaction({ ...newTransaction, commodity_id: value })
                }
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select Commodity" />
                </SelectTrigger>
                <SelectContent>
                  {commodities.map((commodity) => (
                    <SelectItem key={commodity.id} value={commodity.id}>
                      {commodity.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <Select
                onValueChange={(value) =>
                  setNewTransaction({
                    ...newTransaction,
                    counterparty_id: value,
                  })
                }
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select Counterparty" />
                </SelectTrigger>
                <SelectContent>
                  {counterparties.map((counterparty) => (
                    <SelectItem key={counterparty.id} value={counterparty.id}>
                      {counterparty.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <Input
                placeholder="Quantity"
                type="number"
                value={newTransaction.quantity}
                onChange={(e) =>
                  setNewTransaction({
                    ...newTransaction,
                    quantity: e.target.value,
                  })
                }
              />
              <Input
                placeholder="Price"
                type="number"
                value={newTransaction.price}
                onChange={(e) =>
                  setNewTransaction({
                    ...newTransaction,
                    price: e.target.value,
                  })
                }
              />
              <Select
                onValueChange={(value) =>
                  setNewTransaction({
                    ...newTransaction,
                    transaction_type: value,
                  })
                }
                value={newTransaction.transaction_type}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select Transaction Type" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="PURCHASE">Purchase</SelectItem>
                  <SelectItem value="SALE">Sale</SelectItem>
                </SelectContent>
              </Select>
              <Input
                placeholder="Date"
                type="date"
                value={newTransaction.date}
                onChange={(e) =>
                  setNewTransaction({
                    ...newTransaction,
                    date: e.target.value,
                  })
                }
              />
              <Input
                placeholder="Notes"
                value={newTransaction.notes}
                onChange={(e) =>
                  setNewTransaction({
                    ...newTransaction,
                    notes: e.target.value,
                  })
                }
              />
            </div>
            <DialogFooter>
              <Button
                variant="secondary"
                onClick={() => setIsDialogOpen(false)}
              >
                Cancel
              </Button>
              <Button onClick={handleAddTransaction}>Add</Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
      </div>
      {/* Transactions List */}
      <div className="mt-4">
        {transactions.length === 0 ? (
          <p>No transactions found.</p>
        ) : (
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Commodity</TableHead>
                <TableHead>Counterparty</TableHead>
                <TableHead>Quantity</TableHead>
                <TableHead>Price</TableHead>
                <TableHead>Type</TableHead>
                <TableHead>Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {transactions.map((transaction) => (
                <TableRow key={transaction.id}>
                  <TableCell>
                    {
                      commodities.find(
                        (commodity) => commodity.id === transaction.commodity_id
                      )?.name
                    }
                  </TableCell>
                  <TableCell>
                    {
                      counterparties.find(
                        (counterparty) =>
                          counterparty.id === transaction.counterparty_id
                      )?.name
                    }
                  </TableCell>
                  <TableCell>{transaction.quantity}</TableCell>
                  <TableCell>{transaction.price}</TableCell>
                  <TableCell>{transaction.transaction_type}</TableCell>
                  <TableCell>
                    {/* Add Edit and Delete Buttons if needed */}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        )}
      </div>
    </div>
  );
}
