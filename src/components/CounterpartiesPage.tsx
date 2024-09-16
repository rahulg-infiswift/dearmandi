// app/home/counterparties/page.tsx
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
import { Checkbox } from "@/components/ui/checkbox";

interface Counterparty {
  id: string;
  name: string;
  contact_info: string;
  roles: string[];
  notes: string;
}

export default function CounterpartiesPage() {
  const [counterparties, setCounterparties] = useState<Counterparty[]>([]);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [newCounterparty, setNewCounterparty] = useState({
    name: "",
    contact_info: "",
    roles: [],
    notes: "",
  });
  const [editingCounterparty, setEditingCounterparty] =
    useState<Counterparty | null>(null);
  const token =
    typeof window !== "undefined" ? localStorage.getItem("token") : null;

  // Fetch counterparties
  useEffect(() => {
    fetchCounterparties();
  }, []);

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

  const handleAddCounterparty = async () => {
    try {
      await axios.post("/api/counterparties/", newCounterparty, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setNewCounterparty({
        name: "",
        contact_info: "",
        roles: [],
        notes: "",
      });
      setIsDialogOpen(false);
      fetchCounterparties();
    } catch (error) {
      console.error("Error adding counterparty:", error);
    }
  };

  // Similar edit and delete functions can be implemented

  return (
    <div>
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-semibold">Counterparties</h1>
        <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
          <DialogTrigger asChild>
            <Button>
              <Plus className="mr-2 h-4 w-4" />
              Add Counterparty
            </Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Add Counterparty</DialogTitle>
              <DialogDescription>
                Enter the details of the new counterparty.
              </DialogDescription>
            </DialogHeader>
            <div className="space-y-4 py-2 pb-4">
              <Input
                placeholder="Name"
                value={newCounterparty.name}
                onChange={(e) =>
                  setNewCounterparty({
                    ...newCounterparty,
                    name: e.target.value,
                  })
                }
              />
              <Input
                placeholder="Contact Info"
                value={newCounterparty.contact_info}
                onChange={(e) =>
                  setNewCounterparty({
                    ...newCounterparty,
                    contact_info: e.target.value,
                  })
                }
              />
              <div>
                <label className="block text-sm font-medium">Roles</label>
                <div className="flex items-center space-x-2 mt-1">
                  <Checkbox
                    checked={newCounterparty.roles.includes("CUSTOMER")}
                    onCheckedChange={(checked) => {
                      if (checked) {
                        setNewCounterparty({
                          ...newCounterparty,
                          roles: [...newCounterparty.roles, "CUSTOMER"],
                        });
                      } else {
                        setNewCounterparty({
                          ...newCounterparty,
                          roles: newCounterparty.roles.filter(
                            (role) => role !== "CUSTOMER"
                          ),
                        });
                      }
                    }}
                  />
                  <label>Customer</label>
                  <Checkbox
                    checked={newCounterparty.roles.includes("SUPPLIER")}
                    onCheckedChange={(checked) => {
                      if (checked) {
                        setNewCounterparty({
                          ...newCounterparty,
                          roles: [...newCounterparty.roles, "SUPPLIER"],
                        });
                      } else {
                        setNewCounterparty({
                          ...newCounterparty,
                          roles: newCounterparty.roles.filter(
                            (role) => role !== "SUPPLIER"
                          ),
                        });
                      }
                    }}
                  />
                  <label>Supplier</label>
                </div>
              </div>
              <Input
                placeholder="Notes"
                value={newCounterparty.notes}
                onChange={(e) =>
                  setNewCounterparty({
                    ...newCounterparty,
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
              <Button onClick={handleAddCounterparty}>Add</Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
      </div>
      {/* Counterparty List */}
      <div className="mt-4">
        {counterparties.length === 0 ? (
          <p>No counterparties found.</p>
        ) : (
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Name</TableHead>
                <TableHead>Contact Info</TableHead>
                <TableHead>Roles</TableHead>
                <TableHead>Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {counterparties.map((counterparty) => (
                <TableRow key={counterparty.id}>
                  <TableCell>{counterparty.name}</TableCell>
                  <TableCell>{counterparty.contact_info}</TableCell>
                  <TableCell>{counterparty.roles.join(", ")}</TableCell>
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
