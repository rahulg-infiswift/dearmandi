import React from "react";
import Navbar from "@/app/components/Navbar";
import CashPurchase from "@/app/components/CashPurchase";

const Purchases = () => {
  return (
    <div className="flex min-h-screen">
      <Navbar />
      <div className="flex-auto mt-10 px-4">
        <CashPurchase />
      </div>
    </div>
  );
};

export default Purchases;
