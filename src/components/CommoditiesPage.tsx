// app/home/commodities/page.tsx
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

interface Commodity {
  id: string;
  name: string;
  description: string;
  created_at: string;
}

export default function CommoditiesPage() {
  const [commodities, setCommodities] = useState<Commodity[]>([]);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [newCommodity, setNewCommodity] = useState({
    name: "",
    description: "",
  });
  const [editingCommodity, setEditingCommodity] = useState<Commodity | null>(
    null
  );
  const token =
    typeof window !== "undefined" ? localStorage.getItem("token") : null;

  console.log("token", token)
  // Fetch commodities
  useEffect(() => {
    fetchCommodities();
  }, []);

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

  const handleAddCommodity = async () => {
    try {
      console.log(newCommodity)
      await axios.post("/api/commodities/create", newCommodity, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setNewCommodity({ name: "", description: "" });
      setIsDialogOpen(false);
      fetchCommodities();
    } catch (error) {
      console.error("Error adding commodity:", error);
    }
  };

  const handleEditCommodity = async () => {
    if (!editingCommodity) return;
    try {
      await axios.put(
        `/api/commodities/${editingCommodity.id}`,
        {
          name: editingCommodity.name,
          description: editingCommodity.description,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      setEditingCommodity(null);
      fetchCommodities();
    } catch (error) {
      console.error("Error updating commodity:", error);
    }
  };

  const handleDeleteCommodity = async (id: string) => {
    try {
      await axios.delete(`/api/commodities/${id}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      fetchCommodities();
    } catch (error) {
      console.error("Error deleting commodity:", error);
    }
  };

  return (
    <div>
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-semibold">Commodities</h1>
        <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
          <DialogTrigger asChild>
            <Button>
              <Plus className="mr-2 h-4 w-4" />
              Add Commodity
            </Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Add Commodity</DialogTitle>
              <DialogDescription>
                Enter the details of the new commodity.
              </DialogDescription>
            </DialogHeader>
            <div className="space-y-4 py-2 pb-4">
              <Input
                placeholder="Name"
                value={newCommodity.name}
                onChange={(e) =>
                  setNewCommodity({ ...newCommodity, name: e.target.value })
                }
              />
              <Input
                placeholder="Description"
                value={newCommodity.description}
                onChange={(e) =>
                  setNewCommodity({
                    ...newCommodity,
                    description: e.target.value,
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
              <Button onClick={handleAddCommodity}>Add</Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
      </div>
      {/* Commodity List */}
      <div className="mt-4">
        {commodities.length === 0 ? (
          <p>No commodities found.</p>
        ) : (
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Name</TableHead>
                <TableHead>Description</TableHead>
                <TableHead>Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {commodities.map((commodity) => (
                <TableRow key={commodity.id}>
                  <TableCell>{commodity.name}</TableCell>
                  <TableCell>{commodity.description}</TableCell>
                  <TableCell>
                    <div className="flex items-center">
                      <Button
                        variant="outline"
                        size="icon"
                        onClick={() => setEditingCommodity(commodity)}
                      >
                        <Edit2 className="h-4 w-4" />
                      </Button>
                      <Button
                        variant="outline"
                        size="icon"
                        className="ml-2"
                        onClick={() => handleDeleteCommodity(commodity.id)}
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        )}
      </div>

      {/* Edit Commodity Dialog */}
      <Dialog
        open={editingCommodity !== null}
        onOpenChange={() => setEditingCommodity(null)}
      >
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Edit Commodity</DialogTitle>
            <DialogDescription>
              Update the details of the commodity.
            </DialogDescription>
          </DialogHeader>
          {editingCommodity && (
            <div className="space-y-4 py-2 pb-4">
              <Input
                placeholder="Name"
                value={editingCommodity.name}
                onChange={(e) =>
                  setEditingCommodity({
                    ...editingCommodity,
                    name: e.target.value,
                  })
                }
              />
              <Input
                placeholder="Description"
                value={editingCommodity.description}
                onChange={(e) =>
                  setEditingCommodity({
                    ...editingCommodity,
                    description: e.target.value,
                  })
                }
              />
            </div>
          )}
          <DialogFooter>
            <Button
              variant="secondary"
              onClick={() => setEditingCommodity(null)}
            >
              Cancel
            </Button>
            <Button onClick={handleEditCommodity}>Update</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
